from pydantic import BaseModel, Field
from typing import List, Tuple
from enum import Enum
import json
import os
from openai import OpenAI
from user_research_helper.campaign.config import config

class Confidence(str, Enum):
    low = "low"
    medium = "medium" 
    high = "high"

class AnalysisResult(BaseModel):
    found: bool = Field(..., description="Indique si une réponse pertinente a été trouvée")
    answer: str = Field(..., description="La réponse extraite/résumée dans la langue de la question")
    confidence: Confidence = Field(..., description="Niveau de confiance dans la réponse")
    quote: str = Field(..., description="Citation extraite")

class TranscriptAnalyzer:
    def __init__(self, transcript: str):
        """Initialize OpenAI client"""
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
        )
        self.client=OpenAI()
        
        self.transcript = transcript
         # Initialize chat history with system prompt
        self.messages = [
            {
                "role": "system",
                "content": f"""You are a user research specialist analyzing user interviews. Consider the following transcript of an interview:
                {self.transcript}

                Consider also the following keywords that are important and might be mispelled in the transcript : {config.get_config('word_boost', "")}
                """
            }
        ]

    
    def analyze_question(self, question_text: str) -> AnalysisResult:
        """
        Analyze the transcript to find the answer to a specific question using the maintained chat history.
        """
        question_prompt = f"""
        Analyze the transcript to find from the person who is interviewed the answer he gave to some specific question which is in {config.get_config('language', 'English')}:
        Question: {question_text}

        Extract the relevant information that answers this question. Do not invent anything : check that the answer is done by the person who is interviewed. Summarize the answer to contain the important insights in the context of this interview and the question. Be sure that you do not invent anything by checking that the extrated information is in the interview. Check that the extrated information answers the question. Reformulate and do this process again if necessary until you have something perfect. The answer must be in {config.get_config('language', 'English')}.

        Take into account the following context instructions:
        {config.get_config('llm_common_context', "")}
        {config.get_config('llm_answer_extraction_context', "")}



        You must respond with this exact JSON structure:
        {{
            "found": boolean,
            "answer": "string with the extracted answer in {config.get_config('language', 'English')} or empty string if not found",
            "confidence": "low" or "medium" or "high"
            "quote": "if there is a very representative and compact quote (few words), include it here. If there is not such a very interesting quote that could be reused later, leave the field empty"
        }}"""

        # Append the user question to the chat history
        local_messages = self.messages.copy()
        local_messages.append({"role": "user", "content": question_prompt})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                #model="google/gemini-flash-1.5-8b",
                # model="meta-llama/llama-3-70b-instruct",
                # model="openai/gpt-4o-mini",
                messages=local_messages,
                temperature=0.2,
                response_format={"type": "json_object"}  # Force JSON response
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Debug logging
            print(f"Question: {question_text}\nResponse: {response_text}")
            print(f"caching: {response.usage}")
            
            try:
                result = json.loads(response_text)
                analysis_result = AnalysisResult(**result)
            except json.JSONDecodeError as je:
                analysis_result = AnalysisResult(
                    found=False,
                    answer=f"Error parsing JSON response: {str(je)}",
                    confidence=Confidence.low
                )
            
            # Append the assistant's response to the chat history
            self.messages.append({"role": "assistant", "content": response_text})
            
            return analysis_result
                
        except Exception as e:
            return AnalysisResult(
                found=False,
                answer=f"API Error: {str(e)}",
                confidence=Confidence.low
            )   

   
def analyze_transcript_with_questions(
    transcript_path: str,
    questions: List[Tuple[str, str]],
    output_path: str = "analysis_results.json"
) -> dict:
    """Process transcript and analyze with questions"""
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = f.read()
    
    analyzer = TranscriptAnalyzer(transcript)
    
    results = {}
    for question_id, question_text in questions:
        result = analyzer.analyze_question(question_text)
        results[question_id] = {
            "question": question_text,
            "analysis": result.model_dump()
        }
        
        # Save intermediate results
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results