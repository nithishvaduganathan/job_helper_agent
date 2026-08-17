from langchain_core.messages import SystemMessage
from langchain_google_genai import GoogleGenerativeAI
from langchain.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
# Initialize a powerful model for copywriting
llm_writer = GoogleGenerativeAI(model="google_genai:gemini-2.5-flash", temperature=0.7)


@tool
def optimize_email_body(sample_email: str, job_description: str, company_info: str) -> str:
    """
    Optimizes a sample email body to align with a specific Job Description and Company Info.
    - sample_email: Your draft or base email template.
    - job_description: The requirements and responsibilities of the job.
    - company_info: Details about the company's culture, mission, or recent news.
    """

    prompt = f"""
    You are an expert Career Coach and Copywriter. Your goal is to rewrite the 'Original Email' 
    to make it highly persuasive for the specific 'Job Description' and 'Company Information' provided.

    INSTRUCTIONS:
    1. Maintain a professional yet enthusiastic tone.
    2. Highlight 2-3 specific skills from the JD that the candidate possesses.
    3. Mention something specific from the Company Info to show you've done your research.
    4. Keep it concise (under 200 words).
    5. Ensure there is a clear call to action (requesting an interview).

    ORIGINAL EMAIL:
    {sample_email}

    JOB DESCRIPTION:
    {job_description}

    COMPANY INFORMATION:
    {company_info}

    REWRITTEN EMAIL:
    """

    messages = [
        SystemMessage(content="You are a professional corporate recruiter and copywriter."),
        HumanMessage(content=prompt)
    ]

    response = llm_writer.invoke(messages)
    return response.content