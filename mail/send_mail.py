import os

from secret_manager import get_secret
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email
from python_http_client.exceptions import HTTPError

SECRET_MANAGER_PROJECT_ID: str = os.getenv('SECRET_MANAGER_PROJECT_ID')
SENDGRID_API_KEY: str = get_secret(SECRET_MANAGER_PROJECT_ID, 'sendgrid_apikey')
EMAIL_SENDER: str = get_secret(SECRET_MANAGER_PROJECT_ID, 'email_sender')
EMAIL_SENDER_NAME: str = get_secret(SECRET_MANAGER_PROJECT_ID, 'email_sender_name')


def email(to: str, subject: str, body: str) -> str:
    sg = SendGridAPIClient(SENDGRID_API_KEY)

    message = Mail(
        to_emails=to,
        from_email=Email(EMAIL_SENDER, EMAIL_SENDER_NAME),
        subject=subject,
        html_content=body
        )

    try:
        response = sg.send(message)
        print(f"email.status_code={response.status_code}", flush=True)
        return f"email.status_code={response.status_code}"

    except HTTPError as e:
        print(str(e), flush=True)
        return str(e)

