import mysql.connector
from langchain.tools import tool

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",  # Replace with your password
    "database": "job_automation"
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@tool
def get_company_leads(location: str) -> str:
    """
    Search the database for companies in a specific location.
    Returns: Company Name, Email, TechStack, Location.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM company_leads WHERE location LIKE %s"
        cursor.execute(query, (f"%{location}%",))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return f"No companies found in {location}."
        return str(results)
    except Exception as e:
        return f"Database Error: {str(e)}"


@tool
def log_sent_application(company_name: str, email: str, job_role: str, status: str = "Sent") -> str:
    """
    Logs an application to the history table after an email is sent.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO sent_applications (company_name, email, job_role, status) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (company_name, email, job_role, status))
        conn.commit()
        cursor.close()
        conn.close()
        return f"Successfully logged application to {company_name} in MySQL."
    except Exception as e:
        return f"Database Error: {str(e)}"


@tool
def save_scraped_jobs(company_name: str, email: str, job_role: str, job_description: str) -> str:
    """
    Saves newly found jobs from LinkedIn/Naukri for later processing.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO scraped_jobs (company_name, email, job_role, job_description) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (company_name, email, job_role, job_description))
        conn.commit()
        cursor.close()
        conn.close()
        return f"Job at {company_name} saved to MySQL table 'scraped_jobs'."
    except Exception as e:
        return f"Database Error: {str(e)}"