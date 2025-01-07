import assemblyai as aai
import os
from typing import List, Optional

# Initialize AssemblyAI client
api_key = os.environ.get("ASSEMBLYAI_API_KEY")
if not api_key:
    raise ValueError("ASSEMBLYAI_API_KEY not found in environment variables. Please check your .env file.")

aai.settings.api_key = api_key

def process_interview_transcript(
    audio_file_path: str, language_code: str = "fr", word_boost: Optional[List[str]] = ["Chatbot",]
) -> str:
    """
    Process the interview audio using AssemblyAI with speaker diarization
    
    Args:
        audio_file_path: Path to the audio file
        question_context: Optional list of expected questions
    """
    # Configure transcription with speaker diarization
    # define speaker numbers
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speakers_expected=2,
        language_code=language_code,
        word_boost=word_boost,
        boost_param="high",
    )
    
    # Create transcriber and process file
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
        audio_file_path,
        config=config
    )
    
    # Format the transcript with speaker labels
    formatted_transcript = []
    current_speaker = None
    
    for utterance in transcript.utterances:
        speaker = f"Speaker {utterance.speaker}"  # ou utilisez utterance.speaker_name si défini
        timestamp = f"[{utterance.start:.2f} - {utterance.end:.2f}]"
        
        if current_speaker != speaker:
            formatted_transcript.append(f"\n{speaker} {timestamp}:")
            current_speaker = speaker
            
        formatted_transcript.append(f"    {utterance.text}")
    
    return "\n".join(formatted_transcript)
