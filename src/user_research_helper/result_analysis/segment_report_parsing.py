import pandas as pd
import re
from user_research_helper.result_analysis.data import (
     Question, 
    SegmentDataset, SegmentAnswer
)


def parse_segment_report(file_path: str) -> SegmentDataset:
    """
    Charge les données d'un fichier Excel dans la structure SegmentDataset
    
    Args:
        file_path: Chemin vers le fichier Excel
        
    Returns:
        SegmentDataset: Données structurées de l'interview par segment 
    """
    # Charger le fichier Excel
    df = pd.read_excel(file_path)
    
    # Extraire les questions depuis les en-têtes (toutes les colonnes sauf la première)
    questions = [
        Question(
            id=str(i+2),  # Numéro de colonne comme ID (commence à 2 car col1=nom)
            text=str(col_name),
            column_index=i+1
        )
        for i, col_name in enumerate(df.columns[1:])
    ]
    
    # Extraire les segments 
    segments = {}
    
    # Parcourir chaque ligne du DataFrame
    for _, row in df.iterrows():
        segment_name = row.iloc[0]  # Première colonne contient le nom du segment
        segment_answers = {}
        
        # Pour chaque question, créer un SegmentAnswer
        for i, question in enumerate(questions):
            answer_text = row.iloc[i+1]  # +1 car on commence à la 2ème colonne
            if pd.notna(answer_text):  # Vérifier que la réponse n'est pas vide
                segment_answers[question.id] = SegmentAnswer(
                    segment_name=segment_name,
                    question_id=question.id,
                    answer_summary=str(answer_text)
                )
        
        segments[segment_name] = segment_answers
    
    return SegmentDataset(questions=questions, segments=segments)