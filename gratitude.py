import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_gratitude_email(smtp_host, smtp_port, smtp_user, smtp_pass, to_email, subject, body):
    """
    Connects to an SMTP server and sends a gratitude email.
    """
    # Create the email message
    message = MIMEMultipart()
    message["From"] = smtp_user
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the server and send the email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, to_email.split(','), message.as_string())
        print("Successfully sent the gratitude email.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        # Re-raise the exception to ensure the error is logged in Render
        raise e

