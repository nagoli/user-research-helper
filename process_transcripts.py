import os
import argparse
import shutil
from typing import List, Tuple
from dotenv import load_dotenv
# Load environment variables first
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
load_dotenv(env_path)

from user_research_helper.transcript.process_transcripts import process_transcripts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process interview audio files')
    parser.add_argument('root_dir', default="demo", nargs='?', help='Root directory containing all project files')
    
    args = parser.parse_args()
    
    process_transcripts(
        root_dir=args.root_dir
    )
