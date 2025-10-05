import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import argparse

# Load variables from .env if present
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))  # STARTTLS port
SMTP_USER = os.getenv("SMTP_USER")  # your Gmail address
SMTP_PASS = os.getenv("SMTP_PASS")  # your 16-char app password
TO_EMAIL  = os.getenv("TO_EMAIL", SMTP_USER)
SUBJECT   = os.getenv("SUBJECT", "Your 8 PM Gratitude Reminder")
BODY      = os.getenv("BODY", "Reply with 3 things you’re grateful for today.")


def send_email(subject: str, body: str, sender: str, recipients: list[str]):
    if not (SMTP_USER and SMTP_PASS):
        raise ValueError("Missing SMTP_USER or SMTP_PASS. Set them in a .env file.")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    # Gmail with STARTTLS on port 587
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(sender, recipients, msg.as_string())


def main():
    parser = argparse.ArgumentParser(description="Send a gratitude reminder email.")
    parser.add_argument("--test", action="store_true", help="Send a test email now and exit")
    args = parser.parse_args()

    recipients = [e.strip() for e in TO_EMAIL.split(",") if e.strip()]

    if args.test:
        print("Sending test email...")
        send_email(SUBJECT + " (TEST)", BODY, SMTP_USER, recipients)
        print("Test email sent.")
    else:
        send_email(SUBJECT, BODY, SMTP_USER, recipients)
        print("Email sent.")


if __name__ == "__main__":
    main()
