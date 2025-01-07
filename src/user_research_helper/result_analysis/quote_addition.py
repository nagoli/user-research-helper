import pandas as pd
from typing import List
from user_research_helper.result_analysis.data import ResultAnalysis

def add_quotes_from_excel(result_analyses: List[ResultAnalysis], excel_file_path: str) -> List[ResultAnalysis]:
    """
    Add quotes to a list of ResultAnalysis objects from an Excel file.
    
    Args:
        result_analyses: List of ResultAnalysis objects to update with quotes
        excel_file_path: Path to the Excel file containing quotes
        
    Returns:
        List[ResultAnalysis]: Updated list of ResultAnalysis objects with quotes added
    """
    # Read the Excel file
    df = pd.read_excel(excel_file_path)
    
    # Create a mapping of question_id to quotes
    quotes_by_question = {}
    
    # Process each row in the dataframe
    for _, row in df.iterrows():
        # Get the segments for this interview
        segments_str = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
        segments = [s.strip() for s in segments_str.split(',') if s.strip()]
        
        # Process each question (starting from column index 2)
        for col_idx, answer in enumerate(row.iloc[2:], start=2):
            if pd.notna(answer):
                question_id = str(col_idx)  # Convert to 1-based question ID
                quote = str(answer).strip()
                
                # Format quote with segments
                formatted_quote = f"{quote}"
                if segments:
                    segment_str = "(" + ", ".join(segments) + ")"
                    formatted_quote += f" {segment_str}"
                
                # Add to quotes dictionary
                if question_id not in quotes_by_question:
                    quotes_by_question[question_id] = []
                quotes_by_question[question_id].append(formatted_quote)
    
    # Update ResultAnalysis objects with quotes
    for result in result_analyses:
        if result.question_id in quotes_by_question:
            quotes = quotes_by_question[result.question_id]
            result.quotes = "\n".join(quotes)
    
    return result_analyses
