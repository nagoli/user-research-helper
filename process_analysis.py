from dotenv import load_dotenv
load_dotenv()
import argparse
import os
from typing import List, Tuple

from user_research_helper.result_analysis.process_analysis import process_analysis

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Process analysis of segmented transcript report')
    parser.add_argument('root_dir', default="demo", nargs='?', help='Root directory containing all project files')
    
    
    args = parser.parse_args()
    
    process_analysis(
        root_dir=args.root_dir
    )
