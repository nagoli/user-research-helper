from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Set, Any
from enum import Enum


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

def validate_confidence_value(v):
    if v is None:
        return v
    try:
        return Confidence(v)
    except ValueError:
        return None

class Interview(BaseModel):
    """Represents a single interview with its answers and segments"""
    name: str = Field(..., description="Name of the interviewee")
    segments: List[str] = Field(default_factory=list, description="List of normalized segments")
    answers: Dict[str, Optional[str]] = Field(
        default_factory=dict,
        description="Dictionary mapping question IDs to their answers"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "segments": ["adult", "visually_impaired"],
                "answers": {
                    "Q1": "Very positive experience",
                    "Q2": "Some navigation issues"
                }
            }
        }
    }

class Question(BaseModel):
    """Represents a question of the interview"""
    id: str = Field(..., description="Unique identifier of the question")
    text: str = Field(..., description="Text of the question")
    column_index: int = Field(..., description="Index of the column in the Excel file (0-based)")

class InterviewDataset(BaseModel):
    """Represents a collection of interviews with their questions"""
    questions: List[Question] = Field(..., description="List of questions in column order")
    interviews: List[Interview] = Field(..., description="List of interviews")
    segment_set: Set[str] = Field(
        default_factory=set,
        description="Set of all possible segments in the dataset"
    )

    def __init__(self, **data):
        super().__init__(**data)
        self.calculate_segment_set()

    def calculate_segment_set(self):
        """Initialize segment_set from interviews"""
        self.segment_set = set()
        for interview in self.interviews:
            self.segment_set.update(interview.segments)

    @field_validator('segment_set', mode='before')
    def ensure_set(cls, v):
        return set(v) if v is not None else set()

    model_config = {
        "json_schema_extra": {
            "example": {
                "questions": [
                    {
                        "id": "Q1",
                        "text": "What is your experience with the product?",
                        "column_index": 2
                    }
                ],
                "interviews": [
                    {
                        "name": "John Doe",
                        "segments": ["adult", "visually_impaired"],
                        "answers": {
                            "Q1": "Very positive experience",
                            "Q2": "Some navigation issues"
                        }
                    }
                ],
                "segment_set": ["adult", "child", "visually_impaired", "mobility_impaired"]
            }
        }
    }

    def model_dump(self, *args, **kwargs):
        """Override model_dump to convert set to list"""
        data = super().model_dump(*args, **kwargs)
        data['segment_set'] = list(data['segment_set'])
        return data

class SegmentAnswer(BaseModel):
    """Represents an answer for a specific question with summary, quote, and original rough answers"""
    segment_name: str = Field(..., description="Name of the segment this answer relates to")
    question_id: str = Field(..., description="ID of the question this answer relates to")
    answer_summary: Optional[str] = Field(..., description="Summary or main point of the answer")
    rough_answers: List[Optional[str]] = Field(
        default_factory=list,
        description="List of all raw answers for this segment and question"
    )
    summary_confidence: Optional[Confidence] = Field(None, description="Confidence in the summary")
    
    @field_validator('summary_confidence')
    @classmethod
    def validate_confidence(cls, v):
        return validate_confidence_value(v)

    model_config = {
        "json_schema_extra": {
            "example": {
                "segment_name": "accessibility",
                "question_id": "Q1",
                "answer_summary": "Users found the interface easy to navigate with screen readers",
                "rough_answers": [
                    "The screen reader worked perfectly with all elements",
                    "Navigation was straightforward with my screen reader"
                ],
                "summary_confidence": "high"
            }
        }
    }

class SegmentDataset(BaseModel):
    """Represents all segment-related answers organized by question"""
    questions: List[Question] = Field(..., description="List of questions in column order")
    segments: Dict[str, Dict[str, SegmentAnswer]] = Field(
        default_factory=dict,
        description="Dictionary mapping segment names to question with their answers, organized by question ID"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "questions": [
                    {
                        "id": "Q1",
                        "text": "What is your experience with the product?",
                        "column_index": 2
                    },
                    {
                        "id": "Q2",
                        "text": "How easy was it to navigate?",
                        "column_index": 3
                    }
                ],
                "segments": {
                    "accessibility": {
                        "Q1": {
                            "segment_name": "accessibility",
                            "question_id": "Q1",
                            "answer_summary": "Users found the interface easy to navigate with screen readers",
                            "rough_answers": [
                                "The screen reader worked perfectly with all elements",
                                "Navigation was straightforward with my screen reader"
                            ],
                            "summary_confidence": "high"
                        },
                        "Q2": {
                            "segment_name": "accessibility",
                            "question_id": "Q2",
                            "answer_summary": "Navigation was intuitive with assistive technologies",
                            "rough_answers": [
                                "Menu structure was clear with screen reader",
                                "All navigation elements were properly labeled"
                            ],
                            "summary_confidence": "high"
                        }
                    },
                    "mobile": {
                        "Q1": {
                            "segment_name": "mobile",
                            "question_id": "Q1",
                            "answer_summary": "Good mobile experience with some minor layout issues",
                            "rough_answers": [
                                "Works well on my phone",
                                "Some buttons are a bit small on mobile"
                            ],
                            "summary_confidence": "medium"
                        }
                    }
                }
            }
        }
    }

class ResultAnalysis(BaseModel):
    question_id: str = Field(..., description="ID of the question being analyzed")
    question_text: str = Field(..., description="Text of the question being analyzed")
    analysis: str = Field(..., description="Analysis summary across all segments")
    quotes: Optional[str] = Field(default="", description="Quotes postfixed by segments name enclosed in square brackets and parenthesis")
    confidence: Optional[Confidence] = Field(None, description="Confidence in the summary")
    
    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v):
        return validate_confidence_value(v)

    model_config = {
        "json_schema_extra": {
            "example": {
                "question_id": "Q1",
                "question_text": "How did you find the interface?",
                "analysis": "Across all segments, users found the interface intuitive and easy to navigate, with particular appreciation from the accessibility segment",
                "quotes": "Fantastic ! ([segment1]) Cool ! ([segment2])",
                "confidence": "high"
            }
        }
    }
