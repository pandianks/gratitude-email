from flask import Flask, request, jsonify
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "pureremedysolutions@gmail.com")
SMTP_PASS = os.getenv("SMTP_PASS")
TO_EMAIL  = os.getenv("TO_EMAIL")
SUBJECT   = os.getenv("SUBJECT", "Your 8 PM Gratitude Reminder")
BODY      = os.getenv("BODY", "Reply with 3 things you’re grateful for today.")
TRIGGER_TOKEN = os.getenv("TRIGGER_TOKEN")  # a secret word only you know


def send_email(subject, body, sender, recipients):
    if not SMTP_PASS:
        raise ValueError("Missing SMTP_PASS environment variable.")
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(sender, recipients, msg.as_string())

@app.get("/")
def home():
    return "OK", 200

@app.get("/run")
def run():
    # Check the secret so random people can’t trigger it
    token = request.args.get("token")
    if not TRIGGER_TOKEN or token != TRIGGER_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    recipients = [e.strip() for e in TO_EMAIL.split(",") if e.strip()]
    try:
        send_email(SUBJECT, BODY, SMTP_USER, recipients)
        return jsonify({"status": "sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
