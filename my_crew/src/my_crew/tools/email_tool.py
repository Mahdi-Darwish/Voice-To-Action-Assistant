import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class SendEmailInput(BaseModel):
    to: List[str] = Field(
        ..., description="List of recipient email addresses, e.g. ['james@company.com']"
    )
    subject: str = Field(..., description="Subject line of the email")
    body: str = Field(
        ..., description="The email message content, written out in full sentences"
    )
class SendEmailTool(BaseTool):
    name: str = "send_email"
    description: str = (
        "Sends a plain-text email to one or more recipients with a given subject and body. "
        "Use this whenever the user asks to email, notify, message, or inform someone "
        "(e.g. 'send email to James saying I'll be 2 hours late'). Infer a reasonable "
        "subject line if the user didn't give one explicitly."
    )
    args_schema: Type[BaseModel] = SendEmailInput

    def _run(self, to: List[str], subject: str, body: str) -> str:
        sender_email = os.getenv("GMAIL_ADDRESS")
        sender_password = os.getenv("GMAIL_APP_PASSWORD")

        if not sender_email or not sender_password:
            return (
                "Failed to send email: GMAIL_ADDRESS / GMAIL_APP_PASSWORD "
                "are not set in your .env file."
            )
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = ", ".join(to)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to, msg.as_string())
            return f"Email sent successfully to {', '.join(to)}.\nSubject: {subject}"
        except Exception as e:
            return f"Failed to send email: {str(e)}"