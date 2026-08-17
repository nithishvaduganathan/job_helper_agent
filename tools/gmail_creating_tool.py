import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from langchain.tools import tool

# --- CONFIGURATION ---
# Use your Gmail address and the 16-character App Password
SENDER_EMAIL = "nithishvaduganathan07@gmail.com"
APP_PASSWORD = os.environ["APP_PASSWORD"]


@tool
def send_pdf_email(recipient: str, subject: str, body: str, pdf_file_path: str) -> str:
    """
    Sends an email with a PDF file attached.
    - recipient: The receiver's email address.
    - subject: The email subject.
    - body: The message text.
    - pdf_file_path: The local path to the .pdf file (e.g., 'resume/file.pdf').
    """
    try:
        # 1. Check if file exists and is a PDF
        if not os.path.exists(pdf_file_path):
            return f"Error: The file {pdf_file_path} was not found."

        if not pdf_file_path.lower().endswith('.pdf'):
            return "Error: The tool only supports sending .pdf files."

        # 2. Create the container email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # 3. Attach the PDF
        with open(pdf_file_path, "rb") as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
            pdf_attachment.add_header(
                "Content-Disposition",
                "attachment",
                filename=os.path.basename(pdf_file_path)
            )
            msg.attach(pdf_attachment)

        # 4. Connect to Gmail and send
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade to secure connection
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        return f"PDF sent successfully to {recipient}!"

    except Exception as e:
        return f"Failed to send email. Error: {str(e)}"