import os
# from langchain_google_genai import ChatGoogleGenerativeAI #for Googleapi
from crewai import Agent, Task, Crew
# from langchain_community.tools import DuckDuckGoSearchRun 
from dotenv import load_dotenv
from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  MDXSearchTool,
  SerperDevTool
)

load_dotenv()


os.getenv("SERPER_API_KEY")
os.getenv("OPENAI_API_KEY")

# openai_api_key = get_openai_api_key()
# os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
# os.environ["SERPER_API_KEY"] = get_serper_api_key()


# # Setting gemini pro as llm
# llm = ChatGoogleGenerativeAI(model="gemini/gemini-pro",
#                             verbose = True,
#                             temperature = 0.5,
#                             google_api_key=os.getenv("GOOGLE_API_KEY"))


# search_tool = DuckDuckGoSearchRun()
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
read_resume = FileReadTool(file_path='./KULDEEP SINGH TAK_2025 .md')
semantic_search_resume = MDXSearchTool(mdx='./KULDEEP SINGH TAK_2025 .md')


keyword_manager = Agent(
    role = "Resume Keyword Optimization Specialist",
    goal = "Extract and strategically integrate relevant keywords into "
    "resumes to improve their visibility in Applicant Tracking Systems (ATS)"
    " and increase the chances of getting noticed by recruiters.",
    tools = [scrape_tool, search_tool],
    verbose = True,
    backstory = ("As a master of language, you possess the uncanny ability to identify and weave in the most impactful keywords"
    "and phrases that will make a resume truly shine in the eyes of both ATS and human recruiters." 
    )
)

researcher = Agent(
    role="Tech Job Researcher",
    goal="Make sure to do amazing analysis on "
         "job posting to help job applicants",
    tools = [scrape_tool, search_tool],
    verbose=True,
    backstory=(
        "As a Job Researcher, your prowess in "
        "navigating and extracting critical "
        "information from job postings is unmatched."
        "Your skills help pinpoint the necessary "
        "qualifications and skills sought "
        "by employers, forming the foundation for "
        "effective application tailoring."
    )
)

profiler = Agent(
    role="Personal Profiler for Engineers",
    goal="Do increditble research on job applicants "
         "to help them stand out in the job market",
    tools = [scrape_tool, search_tool,
             read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Equipped with analytical prowess, you dissect "
        "and synthesize information "
        "from diverse sources to craft comprehensive "
        "personal and professional profiles, laying the "
        "groundwork for personalized resume enhancements."
    )
)

resume_strategist = Agent(
    role = "Resume Strategist for Engineers",
    goal = "Find all the best ways to make a resume stand out in the job market.",
    tools =  [scrape_tool, search_tool,
             read_resume, semantic_search_resume],
    backstory = (
        "With a strategic mind and an eye for detail, you excel at refining resumes to highlight"
        "the most relevant skills and experiences, ensuring they resonate perfectly with the job's requirements."
    )
)



interview_preparer = Agent(
    role="Engineering Interview Preparer",
    goal="Create interview questions and talking points "
         "based on the resume and job requirements",
    tools =  [scrape_tool, search_tool,
             read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Your role is crucial in anticipating the dynamics of "
        "interviews. With your ability to formulate key questions "
        "and talking points, you prepare candidates for success, "
        "ensuring they can confidently address all aspects of the "
        "job they are applying for."
    )
)

keyword_manager_task = Task(
    description=(
        "Identify and extract the most relevant keywords for the provided resume ({resume_text}) "
        "and target job role ({job_posting_url}). Utilize tools to analyze job descriptions, "
        "research industry trends, and simulate ATS parsing. "
        "Integrate these keywords strategically into the resume."
    ),
    expected_output=(
        "A revised resume with optimized keyword usage, along with a list of "
        "additional keywords for use in cover letters and job applications."
    ),
    agent=keyword_manager,
    async_execution=True
)

# Task for Researcher Agent: Extract Job Requirements
research_task = Task(
    description=(
        "Analyze the job posting URL provided ({job_posting_url}) "
        "to extract key skills, experiences, and qualifications "
        "required. Use the tools to gather content and identify "
        "and categorize the requirements."
    ),
    expected_output=(
        "A structured list of job requirements, including necessary "
        "skills, qualifications, and experiences."
    ),
    agent=researcher,
    async_execution=True
)
# Task for Profiler Agent: Compile Comprehensive Profile
profile_task = Task(
    description=(
        "Compile a detailed personal and professional profile "
        "using the GitHub ({github_url}) URLs, and personal write-up "
        "({personal_writeup}). Utilize tools to extract and "
        "synthesize information from these sources."
    ),
    expected_output=(
        "A comprehensive profile document that includes skills, "
        "project experiences, contributions, interests, and "
        "communication style."
    ),
    agent=profiler,
    async_execution=True
)

resume_strategy_task = Task(
    description=(
        "Using the profile and job requirements obtained from "
        "previous tasks, tailor the resume to highlight the most "
        "relevant areas. Employ tools to adjust and enhance the "
        "resume content. Make sure this is the best resume even but "
        "don't make up any information. Update every section, "
        "inlcuding the initial summary, work experience, skills, "
        "and education. All to better reflrect the candidates "
        "abilities and how it matches the job posting."
    ),
    expected_output=(
        "An updated resume that effectively highlights the candidate's "
        "qualifications and experiences relevant to the job."
    ),
    output_file="tailored_resume.md",
    context=[research_task, profile_task],
    agent=resume_strategist
)

interview_preparation_task = Task(
    description=(
        "Create a set of potential interview questions and talking "
        "points based on the tailored resume and job requirements. "
        "Utilize tools to generate relevant questions and discussion "
        "points. Make sure to use these question and talking points to "
        "help the candiadte highlight the main points of the resume "
        "and how it matches the job posting."
    ),
    expected_output=(
        "A document containing key questions and talking points "
        "that the candidate should prepare for the initial interview."
    ),
    output_file="interview_materials.md",
    context=[research_task, profile_task, resume_strategy_task],
    agent=interview_preparer
)

JobcmdAgents = Crew(
    agents=[keyword_manager,
            profiler,
            researcher,
            resume_strategist,
            interview_preparer],

    tasks=[keyword_manager_task,
           research_task,
           profile_task,
           resume_strategy_task,
           interview_preparation_task],

    verbose=True
)

job_application_inputs = {
    'job_posting_url': 'https://eeho.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/jobsearch/job/275319?utm_medium=jobboard&utm_source=LinkedIn',
    'github_url': 'https://github.com/Itzkuldeep',
    'personal_writeup': """Kuldeep is a skillful person with hands-on practice on different projects based on software development,
                        web development, and artificial intelligence. Ready to join a team where I can grow my knowledge in great 
                        and futuristic fields.""",
    'resume_text': """Kuldeep Singh Tak is a motivated software engineer with expertise in Python, Flask, and web development. 
                      Proven track record of delivering AI-driven solutions and contributing to successful projects."""
}

result = JobcmdAgents.kickoff(inputs=job_application_inputs)