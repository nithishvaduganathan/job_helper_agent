import re
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import json
import os
from langchain.tools import tool

@tool
def gather_company_info(company_name):
    """
        Searches for company details, website, and career-related emails.
        Input: company_name (e.g., 'OpenAI')
        Output: A JSON string containing website, description, and contact emails.
    """

    class CompanyAnalyzerTool:
        def __init__(self, tavily_api_key: str):
            self.tavily = TavilyClient(api_key=tavily_api_key)
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

        def gather_company_data(self, company_name: str) -> str:
            """
            Searches for company details, website, and career-related emails.
            Input: company_name (e.g., 'OpenAI')
            Output: A JSON string containing website, description, and contact emails.
            """
            # 1. Search for the website and career page
            search_query = f"{company_name} official website careers contact email"
            search_results = self.tavily.search(query=search_query, search_depth="advanced", max_results=3)

            results_data = {
                "company_name": company_name,
                "website": "Not found",
                "career_email": "Not found",
                "about": "Not found",
                "social_links": []
            }

            # Identify the main website URL from search results
            if search_results['results']:
                results_data["website"] = search_results['results'][0]['url']
                results_data["about"] = search_results['results'][0]['content']

            # 2. Scrape the identified website for emails
            target_url = results_data["website"]
            if target_url != "Not found":
                found_emails = self._scrape_emails(target_url)
                if found_emails:
                    results_data["career_email"] = found_emails

            return json.dumps(results_data, indent=2)

        def _scrape_emails(self, url: str) -> str:
            """Helper to find emails using regex and page crawling."""
            try:
                # Try to fetch the homepage
                response = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Common pages to check for emails
                contact_links = []
                for link in soup.find_all('a', href=True):
                    href = link['href'].lower()
                    if any(k in href for k in ['contact', 'career', 'about', 'jobs']):
                        # Ensure absolute URL
                        if href.startswith('/'):
                            contact_links.append(url.rstrip('/') + href)
                        elif href.startswith('http'):
                            contact_links.append(href)

                # Look for emails in the homepage + top 2 contact/career pages
                pages_to_scan = [url] + contact_links[:2]
                all_emails = set()

                email_regex = r'[a-zA-Z0-9._%+-]+@(?!example\.com|sentry\.io|git\.com)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

                for page_url in pages_to_scan:
                    try:
                        res = requests.get(page_url, headers=self.headers, timeout=8)
                        emails = re.findall(email_regex, res.text)
                        for email in emails:
                            # Prioritize career/hr related emails
                            email_lower = email.lower()
                            if any(word in email_lower for word in
                                   ['hr', 'career', 'jobs', 'recruiting', 'apply', 'info']):
                                return email  # Return immediately if high-value email found
                            all_emails.add(email)
                    except:
                        continue

                return list(all_emails)[0] if all_emails else "Not found"

            except Exception:
                return "Not found"

    return CompanyAnalyzerTool(
        tavily_api_key=os.environ["TAVILY_API_KEY"]).gather_company_data(company_name)