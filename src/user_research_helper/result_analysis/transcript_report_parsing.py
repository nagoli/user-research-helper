import pandas as pd
import re
from user_research_helper.result_analysis.data import (
    InterviewDataset, Question, Interview,
    SegmentDataset, SegmentAnswer
)


def parse_transcript_report(file_path: str) -> InterviewDataset:
    """
    Charge les données d'un fichier Excel dans la structure InterviewDataset
    
    Args:
        file_path: Chemin vers le fichier Excel
        
    Returns:
        InterviewDataset: Données structurées de l'interview
    """
    # Charger le fichier Excel
    df = pd.read_excel(file_path)
    
    # Extraire les questions depuis les en-têtes (toutes les colonnes sauf les 2 premières)
    questions = [
        Question(
            id=str(i+3),  # Numéro de colonne comme ID (commence à 3 car col1=nom, col2=segments)
            text=str(col_name),
            column_index=i+2
        )
        for i, col_name in enumerate(df.columns[2:])
    ]
    
    # Extraire les interviews (toutes les lignes car les interviews commencent à la ligne 0)
    interviews = []
    for _, row in df.iterrows():  # Supprimé le iloc[1:] pour commencer à la ligne 0
        # Extraire et nettoyer les segments
        segments_str = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
        segments = list({s.strip() for s in segments_str.split(',') if s.strip()})
        
        # Créer le dictionnaire des réponses
        answers = {
            q.id: str(row.iloc[q.column_index]) 
            for q in questions
            if pd.notna(row.iloc[q.column_index])
        }
        
        interview = Interview(
            name=str(row.iloc[0]),
            segments=segments,
            answers=answers
        )
        interviews.append(interview)
    

    dataset = InterviewDataset(
        questions=questions,
        interviews=interviews
    )
    
    # Normalize segments if needed
    #dataset = normalize_segments_in_interviewdataset(dataset)   
    
    return dataset


def create_segment_dataset_from_interview_dataset(interview_dataset: InterviewDataset) -> SegmentDataset:
    """
    Creates a SegmentDataset from an InterviewDataset by grouping answers by segment.
    
    Args:
        interview_dataset: The dataset to process
        
    Returns:
        SegmentDataset: A new dataset with answers grouped by segment
    """
    
    # Create a mapping from segment to dict of question answers
    segments = {}
    
    # Process each interview
    for interview in interview_dataset.interviews:
        # For each segment in this interview
        for segment in interview.segments:
            # If we haven't seen this segment before, initialize it
            if segment not in segments:
                segments[segment] = {}
            
            # Add all answers from this interview to the segment
            for question_id, answer in interview.answers.items():
                if answer:  # Only process non-empty answers
                    if question_id not in segments[segment]:
                        segments[segment][question_id] = SegmentAnswer(
                            segment_name=segment,
                            question_id=question_id,
                            answer_summary=answer,
                            rough_answers=[answer]
                        )
                    else:
                        # Append to existing rough answers
                        segments[segment][question_id].rough_answers.append(answer)
                        # Update answer summary (could be enhanced with better summarization)
                        segments[segment][question_id].answer_summary = answer
    
    # Create and return the SegmentDataset
    return SegmentDataset(
        questions=interview_dataset.questions,
        segments=segments
    )
    
    
 