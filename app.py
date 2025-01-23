import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import (
    FileReadTool,
    ScrapeWebsiteTool,
    MDXSearchTool,
    SerperDevTool
)

# Load environment variables
load_dotenv()

# Set API keys
os.getenv("SERPER_API_KEY")
os.getenv("OPENAI_API_KEY")

# Define tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
read_resume = FileReadTool(file_path='./KULDEEP SINGH TAK_2025.md')
semantic_search_resume = MDXSearchTool(mdx='./KULDEEP SINGH TAK_2025.md')

# Define agents
keyword_manager = Agent(
    role="Resume Keyword Optimization Specialist",
    goal="Extract and strategically integrate relevant keywords into resumes to improve their visibility in Applicant Tracking Systems (ATS) and increase the chances of getting noticed by recruiters.",
    tools=[scrape_tool, search_tool],
    verbose=True,
    backstory=(
        "As a master of language, you possess the uncanny ability to identify and weave in the most impactful keywords "
        "and phrases that will make a resume truly shine in the eyes of both ATS and human recruiters."
    )
)

researcher = Agent(
    role="Tech Job Researcher",
    goal="Analyze job postings to help job applicants tailor their applications.",
    tools=[scrape_tool, search_tool],
    verbose=True,
    backstory=(
        "As a Job Researcher, your prowess in navigating and extracting critical information from job postings is unmatched. "
        "Your skills help pinpoint the necessary qualifications and skills sought by employers."
    )
)

profiler = Agent(
    role="Personal Profiler for Engineers",
    goal="Compile a comprehensive profile for engineers to help them stand out in the job market.",
    tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Equipped with analytical prowess, you dissect and synthesize information from diverse sources to craft comprehensive "
        "personal and professional profiles, laying the groundwork for personalized resume enhancements."
    )
)

resume_strategist = Agent(
    role="Resume Strategist for Engineers",
    goal="Find the best ways to make a resume stand out in the job market.",
    tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "With a strategic mind and an eye for detail, you excel at refining resumes to highlight the most relevant skills and experiences, "
        "ensuring they resonate perfectly with the job's requirements."
    )
)

interview_preparer = Agent(
    role="Engineering Interview Preparer",
    goal="Create interview questions and talking points based on the resume and job requirements.",
    tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Your role is crucial in anticipating the dynamics of interviews. With your ability to formulate key questions and talking points, "
        "you prepare candidates for success, ensuring they can confidently address all aspects of the job they are applying for."
    )
)

# Define tasks
keyword_manager_task = Task(
    description=(
        "Identify and extract the most relevant keywords for the provided resume ({resume_text}) and target job role ({job_posting_url}). "
        "Utilize tools to analyze job descriptions, research industry trends, and simulate ATS parsing. "
        "Integrate these keywords strategically into the resume."
    ),
    expected_output=(
        "A revised resume with optimized keyword usage, along with a list of additional keywords for use in cover letters and job applications."
    ),
    agent=keyword_manager,
    async_execution=True
)

research_task = Task(
    description=(
        "Analyze the job posting URL provided ({job_posting_url}) to extract key skills, experiences, and qualifications required. "
        "Use the tools to gather content and categorize the requirements."
    ),
    expected_output="A structured list of job requirements, including necessary skills, qualifications, and experiences.",
    agent=researcher,
    async_execution=True
)

profile_task = Task(
    description=(
        "Compile a detailed personal and professional profile using the GitHub ({github_url}) URLs and personal write-up ({personal_writeup}). "
        "Utilize tools to extract and synthesize information from these sources."
    ),
    expected_output=(
        "A comprehensive profile document that includes skills, project experiences, contributions, interests, and communication style."
    ),
    agent=profiler,
    async_execution=True
)

resume_strategy_task = Task(
    description=(
        "Using the profile and job requirements obtained from previous tasks, tailor the resume to highlight the most relevant areas. "
        "Update every section, including the initial summary, work experience, skills, and education. "
        "Ensure the resume reflects the candidate's abilities and how they match the job posting."
    ),
    expected_output="An updated resume that effectively highlights the candidate's qualifications and experiences relevant to the job.",
    output_file="tailored_resume.md",
    context=[research_task, profile_task],
    agent=resume_strategist
)

interview_preparation_task = Task(
    description=(
        "Create a set of potential interview questions and talking points based on the tailored resume and job requirements. "
        "Ensure these questions and talking points help the candidate highlight the main points of the resume and its alignment with the job posting."
    ),
    expected_output="A document containing key questions and talking points for the initial interview.",
    output_file="interview_materials.md",
    context=[research_task, profile_task, resume_strategy_task],
    agent=interview_preparer
)

# Define crew
JobcmdAgents = Crew(
    agents=[keyword_manager, resume_strategist, interview_preparer],
    tasks=[keyword_manager_task, resume_strategy_task, interview_preparation_task],
    verbose=True
)

# Job application inputs
job_application_inputs = {
    'job_posting_url': 'https://eeho.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/jobsearch/job/275319',
    'github_url': 'https://github.com/Itzkuldeep',
    'personal_writeup': (
        "Kuldeep is a skillful person with hands-on practice on different projects based on software development, "
        "web development, and artificial intelligence. Ready to join a team where I can grow my knowledge in great "
        "and futuristic fields."
    ),
    'resume_text': (
        "Kuldeep Singh Tak is a motivated software engineer with expertise in Python, Flask, and web development. "
        "Proven track record of delivering AI-driven solutions and contributing to successful projects."
    )
}

# Execute crew
result = JobcmdAgents.kickoff(inputs=job_application_inputs)
