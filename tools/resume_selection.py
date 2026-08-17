import os
from pypdf import PdfReader
from langchain_google_genai import GoogleGenerativeAI
from langchain.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
# Initialize the LLM specifically for scoring
llm_for_scoring = GoogleGenerativeAI(model="google_genai:gemini-2.5-flash", temperature=0)


@tool
def select_best_resume(job_description: str) -> str:
    """
    Reads all PDF resumes in a folder and compares them to a Job Description (JD).
    Returns the file path of the best-matching resume.
    """
    best_match_path = None
    highest_score = -1
    folder_path="/resume_file"
    # 1. List all PDF files in the folder
    if not os.path.exists(folder_path):
        return f"Error: Folder {folder_path} not found."

    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]

    if not pdf_files:
        return "No PDF files found in the folder."

    # 2. Iterate through each resume
    for filename in pdf_files:
        file_path = os.path.join(folder_path, filename)

        try:
            # Extract text from PDF
            reader = PdfReader(file_path)
            resume_text = ""
            for page in reader.pages:
                resume_text += page.extract_text()

            # 3. Ask the LLM to score this resume against the JD (1-100)
            prompt = f"""
            Compare the Resume with the Job Description. 
            Give a match score from 0 to 100.
            Return ONLY the number.

            JD: {job_description}
            ---
            Resume Text: {resume_text}
            """

            response = llm_for_scoring.invoke([HumanMessage(content=prompt)])
            score = int(''.join(filter(str.isdigit, response.content)))

            # 4. Keep track of the best one
            if score > highest_score:
                highest_score = score
                best_match_path = file_path

        except Exception as e:
            print(f"Skipping {filename} due to error: {e}")

    if best_match_path:
        return f"The best resume is {best_match_path} with a match score of {highest_score}/100."
    else:
        return "Could not determine a best match."