import os
from tavily import TavilyClient
from langchain.tools import tool
import os
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
tavily = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def search_linkedin_naukri_jobs(keywords: str, location: str) -> str:
    """
    Searches for the latest job postings on LinkedIn and Naukri based on keywords and location.
    Returns job titles, company names, and application links or recruiter emails.
    """
    # Optimized query to find recent jobs and contact info
    query = f"site:linkedin.com/jobs/ OR site:naukri.com {keywords} in {location} 'posted 1 day ago' 'email'"

    search_result = tavily.search(query=query, search_depth="advanced", max_results=10)

    job_listings = []
    for result in search_result['results']:
        content = result.get('content', '').lower()
        url = result.get('url', '')
        title = result.get('title', '')

        # Try to extract an email if it exists in the snippet
        import re
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
        email_str = emails[0] if emails else "No direct email found (Check URL)"

        job_listings.append(
            f"Job: {title}\nURL: {url}\nContact/Email: {email_str}\n"
        )

    if not job_listings:
        return "No recent jobs found for these keywords."

    return "\n---\n".join(job_listings)