# Resume Optimization and Job Preparation Automation

This project automates resume optimization, job application research, and interview preparation using AI-powered agents. It employs tools like `LiteLLM`, `LangChain`, and Google Generative AI (Gemini Pro) for NLP tasks and integrates utilities for web scraping, resume analysis, and semantic search.

## Features

1. **Resume Optimization**: Extracts and integrates relevant keywords to improve Applicant Tracking System (ATS) visibility.
2. **Job Posting Analysis**: Extracts skills, qualifications, and experiences required from job descriptions.
3. **Profile Compilation**: Creates detailed personal and professional profiles from provided data.
4. **Interview Preparation**: Generates interview questions and talking points tailored to the job requirements and resume.
5. **Automated Workflow**: Agents collaborate through predefined tasks to generate tailored resumes and interview materials.

---

## Prerequisites

Ensure the following are installed on your system:

1. **Python 3.9+**
2. **Visual Studio Build Tools** (Required for building dependencies like `langchain-google-genai`):
   - Download and install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

3. **Dependencies**: Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the project root and include the following keys:

   ```env
   GOOGLE_API_KEY=your_google_api_key
   OPENAI_API_KEY=your_openai_api_key (if you API limit is exceeded than create a new OPENAI account to use the project.)
   SERPER_API_KEY=your_serper_api_key
   ```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `Visual Studio Build Tools` are installed to avoid compilation issues.

4. Set up the `.env` file with the required API keys (as shown above).

---

## Usage

Run the script to execute the agents for resume optimization and job preparation:

```bash
python main.py
```

The following inputs are required:

- **Job Posting URL**
- **GitHub URL**
- **Personal Write-Up**
- **Existing Resume Text**

The system generates the following outputs:

- Optimized resume
- List of keywords for cover letters and applications
- Interview preparation materials

---

## Key Components

1. **Agents**:
   - `Keyword Manager`: Optimizes resumes for ATS systems.
   - `Researcher`: Analyzes job postings.
   - `Profiler`: Creates comprehensive profiles from user data.
   - `Resume Strategist`: Enhances resumes to align with job requirements.
   - `Interview Preparer`: Prepares tailored interview materials.

2. **Tools**:
   - `SerperDevTool`: For job posting analysis.
   - `ScrapeWebsiteTool`: For web scraping.
   - `FileReadTool`: For reading resume files.
   - `MDXSearchTool`: For semantic search in resume files.

3. **Crew and Tasks**:
   - Tasks are defined for each agent to execute specific roles.
   - The `Crew` orchestrates the execution of these tasks.

---

## Project Workflow

1. **Input Data**: Provide job posting URL, GitHub URL, personal write-up, and resume text.
2. **Task Execution**: Agents execute tasks in parallel to:
   - Analyze job postings.
   - Extract and integrate keywords.
   - Create profiles and tailor resumes.
3. **Output**: Generates an optimized resume and interview preparation materials.

---

## Troubleshooting

1. **Infinite Loop**: If using Gemini API Ensure the LLM provider is correctly configured in `ChatGoogleGenerativeAI`. Check API keys and `LiteLLM` provider setup.Use OpenAI for best output and performance
2. **Dependency Issues**: Ensure `Visual Studio Build Tools` are installed and up to date. In it install C/C++ dev tools. 
3. **Environment Variables**: Verify `.env` file configuration.

