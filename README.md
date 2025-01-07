# user-research-helper
AI Assistant for UX Research: A human-in-the-loop helper for user interview transcription and insight analysis.

![Logo](assets/logo.png)

## Introduction

Input = Interviews Audio File + Questions 

Ouput = Excel file with answer analysis for each interview organized per question

Entry = Manual segment definition and per interview analysis adjustment on the generated excel file

Output = Word with comprehensive Report per Question based on segment analysis and cross-interview insights, including quotes from interviews

User Research Analyst is designed to simplify the complex process of analyzing user research interviews. While the analysis of surveys and interviews is a complex task requiring advanced skills and intuition, this tool aims to streamline the analysis process by focusing on structured question-oriented insights. Although it does not generate complete reports, it facilitates the analysis by providing a structured approach based on predefined questions.

The tool combines manual and automated analysis processes, serving as a support for analysis rather than a replacement. It offers a blend of manual insights with automated data processing, helping analysts to focus on more nuanced and complex aspects of their research.

This tool uses the AssemblyAI API for audio transcription, and OpenAI GPT-4o for analysis, Python for data processing and report generation, Excel and Word for report generation.

## Acknowledgments

This project was partially funded by [Access42](https://access42.net), a major supporter of web accessibility in France. We sincerely thank them for their support and trust in the development of this software. 

## Features

- Automated audio transcription using AssemblyAI
- Structured interview analysis based on predefined questions
- Segment-based analysis for detailed insights
- Excel report generation for easy data visualization
- Quote extraction and management
- Multi-language support

## Prerequisites

- Python 3.9+
- Required API keys:
  - AssemblyAI API key (for transcription)
  - OpenAI API key (for analysis)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -e .
```
3. Copy `.envExample` to `.env` and fill in your API keys:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ASSEMBLYAI_API_KEY`: Your AssemblyAI API key

## User Data Setup

The project requires a specific data folder structure.
You can use the 'data_skeleton' folder as a template.

1. Create a data folder with the following structure:
```
your/project/folder/
├── audios/         # Place your interview audio files here
├── config.json     # Configuration file for the analysis
└── questions.txt   # List of interview questions
```

2. Required files:
   - `questions.txt`: Contains the list of interview questions, one per line
   - `config.json`: Contains project configuration settings
   - `audios/`: Directory containing the audio files to be transcribed

See the `demo` folder for examples of these files and their format.

## Usage

Once the data folder is set up, you can start the project by running the following commands:

### 1. Process Transcripts
```bash
python process_transcripts.py your/project/folder
```

Handles the initial processing of interview recordings in 3 steps :

- Take a question list "questions.txt" as input and the audio files in the "audios/" directory.

*For exemple in the demo project we have a question list and 5 audio files to process :*
![Audios in demo exemple](assets/audios.png)


1 - Transcribes each audio files into text, saving them in the “transcripts/raw” directory.

*For exemple in the demo project 5 transcripts are generated :*
![Transcripts in demo exemple](assets/transcripts.png)


2 - Structures each transcripts based on interview questions and raw transcripts and saves them in the “transcripts/structured” directory.

*For exemple in the demo project 5 structured transcripts are generated :*
![Structured transcripts in demo exemple](assets/structured_transcripts.png)

3 - Generates initial analysis reports in the “transcripts” directory based on the structured data:
  - `transcript_analysis_report.xlsx`: Contains the results of the analysis, organized by question, with one line per interview.
  - `transcript_analysis_report_quotes.xlsx`: Contains the most significant quotes from the interviews, organized by question, with one line per interview.

*For exemple in the demo project two analysis reports are generated : *
![Analysis reports in demo exemple](assets/analysis_files.png)

If you add a new interview, you only need to add the audio file to the `audios/` directory and the `process_transcripts.py` script will handle the rest. The previous transcripts will not be overwritten. You will need to delete them if you want to start generate new version of them.

The configuration file `config.json` is used to control the behavior of the script. You can modify it to change the default behavior of the script and cancel some steps. For example, you can set the `do_transcribe_audio` flag to `false` to skip the transcription step.


### 2. Manual segment definition and adjustment
Modify the transcript_analysis_report.xlsx file created in the analysis folder. Define the segment to apply to each interview/line of the report in the segment column. You can assign more than one segment per interview by separating each segment with a comma. In practice, we advise limiting it to one or two segments per interview.
At that part of the process adjust also the analysis if you find it necessary.
Copy also those segments in the transcript_analysis_report_quotes.xlsx file created in the analysis folder . 

*For exemple in the demo project the folowing segments are added to the 2 report files :*
![Segments in demo exemple](assets/manual_segment_addition.png)

### 3. Process Analysis (`process_analysis.py`)

```bash
python process_analysis.py your/project/folder
```

Performs a deeper analysis of the transcribed interviews in 3 steps:

	1.	Segment-Based Analysis
	-	Use the file analysis/transcript_analysis_report.xlsx as input.
	-	Generate segment-based analysis and save the results in the analysis/segments folder.
    
    *For exemple in the demo project the segment analysis files generated has this format :*
    ![Per Segment analysis in demo exemple](assets/per_segment_analysis.png)


	2.	Cross-Interview Insights
	-	Use the segment-based analysis from the analysis/segments folder.
	-	Generate cross-interview insights and save the results in analysis/results_report.xlsx.

    *For exemple in the demo project the cross-interview analysis file generated has this format :*
    ![Cross Interview insights in demo exemple](assets/cross_interview_analysis.png)

	3.	Comprehensive Report per Question
	-	Combine quotes from analysis/transcript_analysis_report_quotes.xlsx with insights from analysis/results_report.xlsx.
	-	Create a comprehensive per-question report in MS Word format and save it as analysis/analysis_report.docx.

    *For exemple in the demo project the final report generated has this format :*
    ![Final report in demo exemple](assets/final_report.png)

The configuration file `config.json` is used to control the behavior of the script. You can modify it to change the default behavior of the script and cancel some steps. 

```bash
python process_analysis.py --root_dir data
```

## Project Structure

- `src/` - Main source code directory
- `data/` - Default directory for project data
  - `demo/` - Config files exemples

## Dependencies

- outlines - For structured text processing
- openai - For AI-powered analysis
- assemblyai - For audio transcription
- python-dotenv - For environment variable management
- transformers - For text processing
- openpyxl - For Excel report generation
- python-docx - For Word document handling

## Configuration

The project uses a configuration system that can be customized through:
- Environment variables (via `.env` file)
- Runtime configuration in the code
- Project-specific settings in `config.json`

Key configuration options include:
- Language settings
- Processing flags
- Output directory structure
- Debug levels

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

### What this means:

- You can freely use, modify, and distribute this software
- Any modifications or software including this code must also be released under the GPL-3.0
- You must disclose the source code when distributing the software
- Changes made to the code must be documented

For more details, see the [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) license terms.

## Contributing

We welcome contributions from the community! If you're interested in improving User Research Helper, please feel free to fork the repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change. 

