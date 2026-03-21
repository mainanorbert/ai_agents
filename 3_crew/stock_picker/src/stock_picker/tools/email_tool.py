from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import Dict

class SendEmailInput(BaseModel):
    """Input for sending an email"""
    to_email: str = Field(..., description="Recipient email address (single email for now)")
    subject: str = Field(..., description="Email subject line")
    html_body: str = Field(..., description="HTML content of the email body")

class SendHTMLEmailTool(BaseTool):
    name: str = "Send HTML Email"
    description: str = (
        "Useful for sending a professional HTML email to one recipient. "
        "Use this when you need to notify someone, send reports, proposals, "
        "follow-ups, or any formatted message via email."
    )
    args_schema: Type[BaseModel] = SendEmailInput

    def _run(self, to_email: str, subject: str, html_body: str) -> str:
        api_key = os.getenv("SENDGRID_API_KEY")
        if not api_key:
            return "Error: SENDGRID_API_KEY environment variable not set."

        from_email_str = os.getenv("EMAIL_FROM", "osiemomaina85@gmail.com")  # fallback to your address; better to set env var

        try:
            sg = SendGridAPIClient(api_key=api_key)

            from_email = Email(from_email_str)
            to_email_obj = To(to_email)
            content = Content("text/html", html_body)

            # Build the mail object
            mail = Mail(
                from_email=from_email,
                to_emails=to_email_obj,
                subject=subject,
                html_content=html_body  # preferred way in recent versions
            )

            # Or use the older .get() style if needed (your original pattern):
            # mail_dict = Mail(from_email, to_email_obj, subject, content).get()
            # response = sg.client.mail.send.post(request_body=mail_dict)

            response = sg.send(mail)

            if response.status_code in (200, 202):
                return f'{{"status": "success", "message_id": "{response.headers.get("X-Message-Id", "unknown")}"}}'
            else:
                return f'{{"status": "error", "code": {response.status_code}, "body": "{response.body}"}}'

        except Exception as e:
            return f'{{"status": "error", "exception": "{str(e)}"}}'