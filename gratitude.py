import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_gratitude_email(sendgrid_api_key, to_email, subject, body):
    """
    Sends an email using the SendGrid API.
    """
    # The 'from_email' must be a verified sender in your SendGrid account.
    # For this test, we can use the same email you send to.
    from_email = os.getenv("SMTP_USER") 

    message = Mail(
        from_email=from_email,
        to_emails=to_email.split(','),
        subject=subject,
        plain_text_content=body
    )
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(f"Email sent via SendGrid, status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email via SendGrid: {e}")
        raise e
