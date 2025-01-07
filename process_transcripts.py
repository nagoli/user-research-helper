import os
import shutil
from typing import List, Tuple
from dotenv import load_dotenv

# Load environment variables first
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
load_dotenv(env_path)



# Import other modules after loading environment variables
from user_research_helper.campaign.question_parsing import parse_questions
from user_research_helper.transcript.transcript_builder import process_interview_transcript
from user_research_helper.transcript.transcript_analysis import analyze_transcript_with_questions
from user_research_helper.transcript.transcript_report_builder import create_excel_report
from user_research_helper.campaign.config import config

def process_interview(
    audio_file: str,
    questions: List[Tuple[str, str]],
) -> None:
    """
    Process a single interview from audio file to analysis
    
    Args:
        audio_file: Path to the audio file
        questions: List of (question_id, question_text) tuples
    """
    # Create directories if they don't exist
   
    raw_transcript_dir = config.get_path('raw_transcript_dir')
    structured_transcript_dir = config.get_path('structured_transcript_dir')
    os.makedirs(raw_transcript_dir, exist_ok=True)
    os.makedirs(structured_transcript_dir, exist_ok=True)
    
    # Extract interview name from audio file
    interview_name = os.path.splitext(os.path.basename(audio_file))[0]
    
    # Define output files
    raw_transcript_file = os.path.join(raw_transcript_dir, f"{interview_name}_raw.txt")
    structured_transcript_file = os.path.join(structured_transcript_dir, f"{interview_name}_structured.json")
    
    # Step 1: Generate transcript if requested
    if config.get_config('do_transcribe_audio', False):
        # Check if transcript already exists
        if os.path.exists(raw_transcript_file):
            if config.should_debug('verbose'):
                print(f"Skipping transcription for {interview_name} - transcript already exists")
        else:
            if config.should_debug('verbose'):
                print(f"Transcribing {interview_name}...")
            transcript = process_interview_transcript(
                audio_file,
                language_code=config.get_config('language_id'),
                word_boost=config.word_boost
            )
            with open(raw_transcript_file, "w", encoding="utf-8") as f:
                f.write(transcript)
                
            if config.should_debug('print_transcripts'):
                print(f"\nTranscript for {interview_name}:")
                print(transcript)
    
    # Step 2: Analyze transcript if requested
    if config.get_config('do_analyze_audio_transcript', False):
        if not os.path.exists(raw_transcript_file):
            print(f"Error: Cannot analyze {interview_name} - raw transcript not found at {raw_transcript_file}")
        else : 
            # Skip analysis if structured transcript already exists
            if os.path.exists(structured_transcript_file):
                if config.should_debug('verbose'):
                    print(f"Skipping analysis for {interview_name} - structured transcript already exists")
            else:
                print(f"Analyzing {interview_name}...")
                results = analyze_transcript_with_questions(
                    transcript_path=raw_transcript_file,
                    questions=questions,
                    output_path=structured_transcript_file
                )
                if config.should_debug('print_analysis'):
                    print(f"\nAnalysis results for {interview_name}:")
                    print(results)


def process_interview_directory(
    questions: List[Tuple[str, str]],
) -> None:
    """
    Process all audio interviews in a directory
    
    Args:
        questions: List of (question_id, question_text) tuples
    """
    # Get audio directory
    audio_dir = config.get_path('audio_dir')
    
    # Get all audio files
    audio_extensions = {'.m4a', '.mp3', '.wav', '.aac'}
    audio_files = [
        os.path.join(audio_dir, f) 
        for f in os.listdir(audio_dir) 
        if os.path.splitext(f)[1].lower() in audio_extensions
    ]
    
    
    
    if config.should_debug('verbose'):
        print(f"\nFound {len(audio_files)} audio files in {audio_dir}:")
        for f in audio_files:
            print(f"  - {os.path.basename(f)}")
    else:
        print(f"Found {len(audio_files)} audio files to process")
    
    transcript_report_dir = config.get_path('transcript_report_dir')
    os.makedirs(transcript_report_dir, exist_ok=True) 
    report_file = os.path.join(transcript_report_dir, "transcript_analysis_report.xlsx")
    
    analysis_dir = config.get_path('analysis_dir')
    os.makedirs(analysis_dir, exist_ok=True) 
    analysis_report_file = os.path.join(analysis_dir, "transcript_analysis_report.xlsx")
    
    
    # Process each audio file
    for audio_file in audio_files:
        try:
            process_interview(
                audio_file=audio_file,
                questions=questions,
            )
        except Exception as e:
            print(f"Error processing {audio_file}: {str(e)}")
            if config.should_debug('verbose'):
                import traceback
                print(traceback.format_exc())
    
    # Generate report if requested
    if config.get_config('do_make_transcript_report', False):
        if config.should_debug('verbose'):
            print("\nGenerating transcript report...")
        
        # Get all structured transcript files
        structured_transcript_dir = config.get_path('structured_transcript_dir')
        results_files = [
            os.path.join(structured_transcript_dir, f)
            for f in os.listdir(structured_transcript_dir)
            if f.endswith('_structured.json')
        ]
        
        if results_files:
            # Create report
            create_excel_report(questions, results_files, report_file)
            if config.should_debug('verbose'):
                print(f"Report generated: {report_file}")
            if not os.path.exists(analysis_report_file):
                # copy report file if not already existing
                shutil.copy2(report_file, analysis_report_file)
                #copy report quotres if not already existing 
                shutil.copy2(report_file.replace('.xlsx', '_quotes.xlsx'), analysis_report_file.replace('.xlsx', '_quotes.xlsx'))
                if config.should_debug('verbose'):
                    print(f"Copied report file to analysis directory: {analysis_report_file}")
            # Create segment dataset if requested
        else:
            print("No structured transcripts found to generate report")
        

def main(
    root_dir: str = "data"
) -> None:
    """
    Main function to process interviews
    
    Args:
        root_dir: Root directory containing all project files
    """
    try:
        # Initialize configuration
        config.initialize(root_dir)
        if config.should_debug('verbose'):
            print(f"Initialized configuration:")
            print(f"  Root directory: {config.root_dir}")
            print(f"  Language: {config.language}")
            print(f"  Word boost terms: {len(config.word_boost)}")
            
    
        
        # Parse questions (only needed for analysis)
        questions = parse_questions(config.get_path('question_file'))
        if config.should_debug('verbose'):
            print(f"\n{len(questions)} questions parsed")
            if config.should_debug('print_questions'):
                for qid, text in questions:
                    print(f"{qid}: {text}")
    
        # Process all interviews in the audio directory 
        process_interview_directory(
            questions=questions,
        )
            
    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"Error: {str(e)}")
        if config.should_debug('verbose'):
            import traceback
            print(traceback.format_exc())
        return

if __name__ == "__main__":
    import argparse
    import os
    from typing import List, Tuple
    
    parser = argparse.ArgumentParser(description='Process interview audio files')
    parser.add_argument('root_dir', default="demo", nargs='?', help='Root directory containing all project files')
    
    args = parser.parse_args()
    
    main(
        root_dir=args.root_dir
    )
