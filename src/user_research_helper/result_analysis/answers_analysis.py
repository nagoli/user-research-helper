from typing import List, Dict, Optional
import json
import openai
import os
from user_research_helper.campaign.config import config

from user_research_helper.result_analysis.data import SegmentDataset, SegmentAnswer, Confidence

def generate_segment_synthesis(
    segment_name: str,
    question_text: str,
    answers: List[str]
) -> dict:
    """
    Generates a synthesis of answers for a specific question and segment.
    
    Args:
        segment_name: Name of the segment being analyzed
        question_text: Text of the question
        answers: List of answers for this question
        llm_answer_analysis_context: Context for LLM analysis
    """
    openrouter = False
    if openrouter:
        client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.environ.get("OPENROUTER_API_KEY"),
            )
    else : 
        client = openai.OpenAI()
    
    
    prompt = f"""
    You are a researcher analyzing user responses to a usage of a product.
    
    The analysis was done in {config.get_config('language', 'English')} and the context is:
    {config.get_config('llm_common_context', "")}
    
    Here is one particular question of the interview you are going to work with :
    {question_text}
    
    
    Here are all the different answers to this question from users in the "{segment_name}" segment:
    {answers}
    
    Please provide a concise and precise synthesis of these answers in {config.get_config('language', 'English')} language, highlighting:
    1. Common themes and patterns, tendencies and frequencies
    2. Notable unique perspectives
    3. Key insights
    
    Here is more contexte for your synthesis:
    {config.get_config('llm_answer_analysis_context', "")}
    
    Be sure that you do not invent anything by checking that all the elements of your synthesis information are in the provided answers. Check that all the elements of your synthesis are related to the question. Reformulate and do this process again if necessary until you have something perfect. 
    
    
    You must always respond with this exact JSON structure:
    {{
        "analysis": "your concise and precise synthesis of the answers in {config.get_config('language', 'English')} language",
        "confidence": "low" or "medium" or "high"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            #model="google/gemini-flash-1.5-8b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        parsed_reponse = json.loads(response.choices[0].message.content)
        print(parsed_reponse)
        return parsed_reponse
    except Exception as e:
        print(f"Error generating synthesis: {str(e)}")
        return {
            "analysis": f"Error generating synthesis: {str(e)}",
            "confidence": "low"
        }

def analyze_segment_answers(
    segment_answer: SegmentAnswer,
    question_text: str
) -> None:
    """
    Analyzes answers for a segment and updates the SegmentAnswer object with the analysis.
    
    Args:
        segment_answer: SegmentAnswer object containing the answers and metadata
        question_text: The text of the question being analyzed
        llm_answer_analysis_context: Context for LLM analysis
    """
    synthesis = generate_segment_synthesis(
        segment_name=segment_answer.segment_name,
        question_text=question_text,
        answers=segment_answer.rough_answers
    )
    
    # Update the SegmentAnswer object with the analysis
    segment_answer.answer_summary = synthesis["analysis"]
    segment_answer.summary_confidence = Confidence[synthesis["confidence"].upper()]
   
   

# Example usage
def main():
    # Create a sample SegmentAnswer object
    segment_answer = SegmentAnswer(
        segment_name="Visually Impaired",
        question_id="Q1",
        rough_answers=["ChatGPT is easy to use", "Navigation is straightforward"],
        answer_summary="",
        quote=None,
        summary_confidence=None
    )
    
    analyze_segment_answers(
        segment_answer=segment_answer,
        question_text="What is your overall experience?",
        llm_answer_analysis_context="You are analyzing visually impaired user responses to the usage of the ChatGPT interface."
    )
    print(f"Updated SegmentAnswer:\n{segment_answer.model_dump_json(indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())