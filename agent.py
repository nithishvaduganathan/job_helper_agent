from deepagents import create_deep_agent

from tools import gmail_creating_tool
from utils.file_loader import file_load
import os
from dotenv import load_dotenv
load_dotenv()
from tools.company_search_tool import gather_company_info
from tools.gmail_creating_tool import send_pdf_email
from tools.resume_selection import select_best_resume
from tools.search_linkedin_naukri_jobs import search_linkedin_naukri_jobs
from tools.google_sheet_tool import get_company_leads,log_sent_application,save_scraped_jobs
from tools.email_body_generation import optimize_email_body
email_agent= {
    "name": "email_agent",
    "description": "A specialist agent for professional outreach. Use this agent to personalize application emails and send them with PDF attachments. It takes a Job Description, Company Info, and a Resume File Path, optimizes the email body to be highly persuasive, and executes the sending process via Gmail.",
    "system_prompt": file_load("sample_email_body.txt"),
    "tools": [send_pdf_email,optimize_email_body],
    "model": "google_genai:gemini-2.5-flash",
}

resume_selection_agent= {
    "name": "resume_selection_agent",
    "description": "A technical screening specialist. Use this agent to analyze a Job Description and Job Title against a local repository of resumes. It will evaluate every PDF in the folder and return the exact file path of the resume that has the highest match score. Essential for ensuring the right version of a resume is sent for a specific role.",
    "system_prompt":file_load("resume_selection_prompt.txt"),
    "tools": [select_best_resume],
    "model": "google_genai:gemini-2.5-flash",
}
job_portal_agent= {
    "name": "resume_selection_agent",
    "description": "A specialized lead generation specialist for job markets. Use this agent to scout LinkedIn and Naukri for the latest job postings based on specific roles and locations. It extracts company names, job descriptions, and most importantly, recruiter contact emails or application URLs. It provides the raw data needed to start the application process.",
    "system_prompt":file_load("job_portal_prompt.txt"),
    "tools": [search_linkedin_naukri_jobs],
    "model": "google_genai:gemini-2.5-flash",
}

root_agent = create_deep_agent(
    name="job_helper",
    model="google_genai:gemini-2.5-flash",
    system_prompt=file_load("system_prompt"),
    tools=[gather_company_info,get_company_leads,log_sent_application,save_scraped_jobs],
    subagents=[resume_selection_agent,email_agent,resume_selection_agent,job_portal_agent],

)

result=root_agent.invoke(
    {"messages": [{"role": "user", "content": "current any job openings in chennai search nakuri job role python developer or ai engineer role"}]}
)
# CORRECT
print(result["messages"][-1].content['text'])