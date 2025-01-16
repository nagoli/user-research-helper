# user-research-helper

A human-in-the-loop AI assistant for user interview transcription and insight analysis.

---
![GitHub views](https://komarev.com/ghpvc/?username=your-repo-name&color=blue)

## 1. Introduction

User Research Helper is an AI-augmented tool that streamlines the process of analyzing user research interviews. It combines automated audio transcription (via AssemblyAI) with OpenAI-powered analysis to generate organized, question-based insights. By blending automated data processing with manual oversight, User Research Helper allows UX researchers and analysts to focus on deeper insights rather than tedious transcription and data wrangling.

### Key Benefits

- **Save Time:** Automated transcription and analysis reduce manual overhead.
- **Stay Flexible:** Human-in-the-loop oversight ensures you can refine results or override AI suggestions.
- **Centralize Insights:** Organized Excel sheets and Word reports keep all findings in one place.
- **Scalable:** Easily handle multiple interviews without losing structure or clarity.

![User research helper process](assets/process.png)

---

## 2. Key Features

- **Automated Audio Transcription**  
  Quickly convert interview recordings to text using the AssemblyAI API.

- **Question-Based Analysis**  
  Automatically map interview responses to a predefined set of questions for organized insights.

- **Segment-Based Insights**  
  Define user segments (e.g., demographics, behavior groups) and tag each interview's responses accordingly.

- **Excel Report Generation**  
  Generate structured Excel files that summarize findings per question, per interview.

- **Quote Extraction**  
  Automatically pinpoint and extract key quotes for easy reference in the analysis report.

- **Cross-Interview Insights**  
  Combine data from multiple interviews to uncover broader trends, patterns, and outliers.

- **Multi-Language Support**  
  Process interviews in various languages without sacrificing structure or clarity.

---

## 3. Quick Start

To get started with **User Research Helper**, you will need the following:

- **OpenAI API Key:** [Obtain one here](https://openai.com/api/)
- **AssemblyAI API Key:** [Obtain one here](https://assemblyai.com)

You have two main options to use this tool:

1. **Colab Option:** Use Google Colab to run the tool without any local installations (Google account needed).
2. **Python Option:** Run the tool locally on your machine.

### 3.1 Colab Option

If you prefer to use this tool on Google Colab, follow these steps:

1. **Requirements:**
   - A Google account with access to Google Drive.

2. **Prepare Your Data:**
   - Organize your data as explained in the [Data Setup section](#51-data-setup) and add them to your Google Drive.

3. **Open the Colab Notebook:**
   - Access the [Colab Notebook](https://colab.research.google.com/github/nagoli/user-research-helper/blob/main/user_research_helper.ipynb).

4. **Follow the Instructions:**
   - Execute the notebook cells step-by-step as per the provided instructions to set up and run the tool.

5. **Share Your Findings:**
   - Use the generated Word document located at `analysis/results_with_quotes.docx` on your Google Drive to share your insights.

### 3.2 Python Option

If you are comfortable running Python on your local machine, follow these steps:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/nagoli/user-research-helper.git
    cd user-research-helper
    ```

2. **Install Dependencies:**

    ```bash
    pip install -e .
    ```

3. **Configure API Keys:**
    - Copy the example environment file and set your API keys:

      ```bash
      cp .envExample .env
      ```

    - Open the `.env` file in a text editor and add your `OPENAI_API_KEY` and `ASSEMBLYAI_API_KEY`:

      ```env
      OPENAI_API_KEY=your-openai-api-key
      ASSEMBLYAI_API_KEY=your-assemblyai-api-key
      ```

4. **Prepare Your Data:**
    - Organize your data as explained in the [Data Setup section](#1-data-setup).

5. **Process Transcripts:**

    ```bash
    python process_transcripts.py your/project/folder
    ```

6. **Define Segments:**
    - Open and edit `analysis/transcript_analysis_report.xlsx` to define segments for each interview.

7. **Process Analysis:**

    ```bash
    python process_analysis.py your/project/folder
    ```

8. **Share Your Findings:**
   - Use the generated Word document located at `analysis/results_with_quotes.docx` to share your insights.

---

## 4. Tool Workflow

Here is an overview of how User Research Helper operates:

1. **Input**  
   - Audio recordings of interviews  
   - A set of predefined interview questions  

2. **Process**  
   - Transcribes each audio file automatically  
   - Maps responses to corresponding interview questions  
   - Provides an Excel report with initial analysis per question, per interview  

3. **Human Review**  
   - Lets you manually segment or categorize interviews in the Excel file  
   - Offers the flexibility to refine automated analyses  

4. **Output**  
   - Generates a Word report that summarizes cross-interview findings by question  
   - Integrates direct quotes from transcripts  
   - Enables a high-level, human-vetted view of key insights  

---

## 5. Usage Guide

This **Usage** guide explains how to organize your data, run each processing step, and refine interview segments. It also describes the intermediate files that the tool generates to avoid unnecessary re-computation. If you ever need to re-run a specific analysis step, simply delete the relevant intermediate files before running the script again.

---

### 5.1. Data Setup

#### a. Folder Structure

   Create or select a project folder with the following structure:

```
your/project/folder/
│
├── audios/         # Place your interview audio files here
├── config.json     # Configuration file for the analysis
└── questions.txt   # List of interview questions
```

#### b. Use the `data_skeleton` Folder (Recommended) 

- You can copy or reference the [`data_skeleton/`](data_skeleton/) folder included in this repository.  
- It contains a ready-to-use `config.json` that shows which settings you can define for your project—such as special instructions for the language model (LLM).  
- Feel free to customize `config.json` for flags like `"do_transcribe_audio": true/false` or other advanced settings related to LLM instructions.

#### c. Required Files  

- **`questions.txt`**: One interview question per line.  
- **`config.json`**: Stores project configuration (e.g., transcription toggle, advanced LLM parameters).  
- **`audios/`**: Folder containing your audio files to be transcribed.

> **Tip:** The [`demo/`](demo/) folder offers a complete walk-through with sample audio files, questions, and configuration. Use it as a reference to get started quickly.

> The demo includes a sample of 5 interviews exploring users’ habits while drinking coffee.  

> The question file for this demo project is:
> ![Questions in demo exemple](assets/questions.png)

> The config file for this demo project is :
> ![Config in demo exemple](assets/config.png)

---

### 5.2. Process Transcripts

Once your data folder is prepared:

```bash
python process_transcripts.py your/project/folder
```

This script performs three main tasks and writes intermediate files to help avoid re-processing:

#### a. Audio Transcription

- Reads `questions.txt` and transcribes every audio file in `audios/`
- Saves raw transcripts in `transcripts/raw/`

> In the demo folder (5 sample audios), you'll see 5 raw transcripts:
> ![Audios in demo exemple](assets/audios.png)
> ![Transcripts in demo exemple](assets/transcripts.png)

#### b. Structured Transcripts

- Organizes raw transcripts by your predefined questions
- Saves structured transcripts in `transcripts/structured/`

> Example from demo: each transcript is now sectioned by question:
> ![Structured transcripts in demo exemple](assets/structured_transcripts.png)

#### c. Initial Analysis Reports

- Generates two Excel files in the `transcripts/` directory:
  - `transcript_analysis_report.xlsx`
  - `transcript_analysis_report_quotes.xlsx`
- These files list interview responses and notable quotes per question, per interview

>The demo project example:
>![Analysis reports in demo exemple](assets/analysis_files.png)

**Note on Intermediate Files**

- If you add a new interview (audio file) later, simply place it in `audios/` and rerun the script
- Existing transcripts are not overwritten unless you manually remove them. This design helps you avoid re-transcribing interviews every time.

### 5.3. Manual Segment Definition & Adjustment

After the initial analysis, the generated Excel files in the `transcripts/` folder will be automatically copied into the `analysis/` folder. These are the files you will modify to add segments or adjust AI-generated insights.

#### a. Segments in the Analysis Folder

- Open `transcript_analysis_report.xlsx` located in the `analysis/` folder
- Under the Segment column, assign one or two segments (e.g., "Beginner", "Expert") to each interview. Separate multiple segments with commas
- Update or refine any AI-generated text if needed
- Repeat the same segment assignments in `transcript_analysis_report_quotes.xlsx` to keep quotes aligned

> In the demo project, segments have been added to both files:
> ![Segments in demo exemple](assets/manual_segment_addition.png)

#### b. Preserving Modifications

- The tool automatically generates fresh reports in the `transcripts/` folder if you re-run `process_transcripts.py`
- These new reports do not overwrite your `analysis/` folder files by default. This safeguard keeps your manual modifications safe
- If you want to incorporate newly generated data from `transcripts/` into `analysis/`, you'll need to manually overwrite the existing analysis files in `analysis/`—and re-add segments or edits as needed.

### 5.4. Process Analysis

Next, refine your insights further:

```bash
python process_analysis.py your/project/folder
```

This script uses intermediate files to avoid repeating costly computations:

#### a. Segment-Based Analysis

- Reads your edited `transcript_analysis_report.xlsx` from `analysis/`
- Produces detailed, segment-focused Excel sheets in `analysis/segments/`

> Demo shows segment analyses with key observations per group:
![Per Segment analysis in demo exemple](assets/per_segment_analysis.png)

#### b. Cross-Interview Insights

- Examines the segment-based output to identify patterns across multiple interviews
- Saves consolidated data in `analysis/results_report.xlsx`

> Demo merges segment data to reveal broad trends:
> ![Cross Interview insights in demo exemple](assets/cross_interview_analysis.png)

#### c. Comprehensive Word Report

- Combines quotes from `transcript_analysis_report_quotes.xlsx` with the aggregated data in `results_report.xlsx`
- Outputs a final `analysis_report.docx` in the `analysis/` folder

> The demo project's final Word report looks like this:
> ![Final report in demo exemple](assets/final_report.png)

### 5.5 Regenerating Specific Parts

#### a. Intermediate Files

- Each stage above saves its results in distinct directories (e.g., `transcripts/raw`, `analysis/segments`).
- This design ensures you don’t need to re-run the entire workflow every time.

#### b. How to Re-Run a Specific Step

- Delete (or rename) the relevant intermediate files or folders. For instance, remove a specific raw transcript to re-transcribe an audio file.
- Then re-run the associated script (`process_transcripts.py` or `process_analysis.py`).
- The tool will regenerate only what’s missing, preventing unnecessary overhead.

---

## 6. Installation & Configuration

### Prerequisites

- Python 3.9+
- Required API keys:
- AssemblyAI API key (for transcription)
- OpenAI API key (for analysis)

### Installation

1. **Clone the Repository**  

```bash
git clone https://github.com/nagoli/user-research-helper.git
cd user-research-helper
```

2. **Install Dependencies**  

```bash
pip install -e .
```

3. **Set up Environment Variables**  

```bash
cp .envExample .env
```

Open the `.env` file and add your keys:

```env
OPENAI_API_KEY=<your-openai-api-key>
ASSEMBLYAI_API_KEY=<your-assemblyai-api-key>
```

---

## 7. Project Structure

- **src/** - Main source code directory
- **demo/** - Example project with sample files and configuration
- **data_skeleton/** - Template directory structure for new projects
- **assets/** - Documentation images and resources

---

## 8. Dependencies

- `pandas` - For data processing
- `outlines` - For structured text processing
- `openai` - For AI-powered analysis
- `assemblyai` - For audio transcription
- `python-dotenv` - For environment variable management
- `transformers` - For text processing
- `openpyxl` - For Excel report generation
- `python-docx` - For Word document handling

---

## 9. License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

**What this means**:  

- You can freely use, modify, and distribute this software.  
- Any modifications or software including this code must also be released under the GPL-3.0.  
- You must disclose the source code when distributing the software.  
- Changes made to the code must be documented.  

For more details, see the [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) license terms.

---

## 10. Contributing & Acknowledgments

We welcome contributions from the community!  

- **Contributing**: Feel free to fork the repository, make your changes, and submit a pull request. For major changes, open an issue to discuss them first.  
- **Acknowledgments**: This project was partially funded by [Access42](https://access42.net), a major supporter of web accessibility in France. We sincerely thank them for their support and trust in the development of this software.
