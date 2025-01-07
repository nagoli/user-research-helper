from typing import List, Dict, Optional
import json
import openai
import os
from user_research_helper.campaign.config import config
from user_research_helper.result_analysis.data import SegmentDataset, SegmentAnswer, Confidence, ResultAnalysis

def generate_question_synthesis(
    question_text: str,
    segment_summaries: Dict[str, str],
) -> Dict[str, str]:
    """
    Generate a synthesis of all segment summaries for a specific question.
    
    Args:
        question_text: The text of the question being analyzed
        segment_summaries: Dictionary mapping segment names to their summaries
        question_id: The ID of the question being analyzed
    """
    openrouter = False
    if openrouter:
        client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.environ.get("OPENROUTER_API_KEY"),
            )
    else : 
        client = openai.OpenAI()
    
    summaries_text = "\n".join([f"- {segment}: {summary}" for segment, summary in segment_summaries.items()])
    
    prompt = f"""
    You are analyzing user research responses. You need to synthesize summaries from different user segments for a specific question.
    
    The analysis was done in {config.get_config('language', 'English')} and the context is:
    {config.get_config('llm_common_context', "")}
    
    Question: 
    {question_text}

    Segment Summaries:
    {summaries_text}
    

    Please provide a concise and precise synthesis of these summaries in {config.get_config('language', 'English')} language, highlighting:
    1. Identifies common patterns across segments
    2. Highlights key differences between segments
    3. Draws meaningful conclusions about the overall user experience
    
    Here is more context for your synthesis:
    {config.get_config('llm_result_analysis_context', "")}
    
    Be precise and factual. Only include information that is supported by the summaries. Be sure that you do not invent anything by checking that all the elements of your synthesis information are in the provided summaries. Check that all the elements of your synthesis are related to the given question. Reformulate and do this process again if necessary until you have something perfect. 
    
    
    You must always respond with this exact JSON structure:
    {{
        "analysis": "your concise and precise synthesis of the summaries in {config.get_config('language', 'English')} language",
        "confidence": "low" or "medium" or "high"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            #model="google/gemini-flash-1.5-8b",
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            response_format={"type": "json_object"}
        )
        parsed_response = json.loads(response.choices[0].message.content)
        
        return parsed_response
    except Exception as e:
        print(f"Error generating synthesis: {str(e)}")
        return {
            "analysis": f"Error generating synthesis : {str(e)}",
            "confidence": "low"
        }


def analyze_question_across_segments(
    segment_dataset: SegmentDataset,
    question_text: str,
    question_id: str
) -> ResultAnalysis:
    """
    Analyzes summaries across all segments for a specific question.
    
    Args:
        segment_dataset: The dataset containing all segment answers
        question_text: The text of the question being analyzed
        question_id: The ID of the question being analyzed
    """
    # Collect summaries from all segments
    segment_summaries = {}
    for segment_name, segment_data in segment_dataset.segments.items():
        if question_id in segment_data:
            answer = segment_data[question_id]
            if answer.answer_summary:  # Only include if there's a summary
                segment_summaries[segment_name] = answer.answer_summary
    
    if (config.should_debug('print_result_analysis_parsing')):
        print (f"Segment summaries for question {question_id}:")
        print(question_text)
        print (segment_summaries)
        print("")
            
    # Generate synthesis of all segment summaries
    parsed_response = generate_question_synthesis(question_text, segment_summaries)
    
    analysis = ResultAnalysis(
            question_id=question_id,
            question_text=question_text,
            analysis=parsed_response["analysis"],
            confidence=Confidence[parsed_response["confidence"].upper()]
        )
    
    if (config.should_debug('print_result_analysis')):
        print (f"Analysis for question {question_id}:")
        print(question_text)
        print (analysis.analysis)
        print (analysis.confidence)
        print("")
    
    return analysis


