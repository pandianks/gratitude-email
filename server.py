import os
import threading
from flask import Flask, request, jsonify
from gratitude import send_gratitude_email

app = Flask(__name__)

def send_email_in_background():
    """This function runs in the background to send the email."""
    try:
        # Note: We now pass the SendGrid API key instead of SMTP details
        send_gratitude_email(
            sendgrid_api_key=os.getenv("SENDGRID_API_KEY"),
            to_email=os.getenv("TO_EMAIL"),
            subject=os.getenv("SUBJECT"),
            body=os.getenv("BODY"),
        )
    except Exception as e:
        print(f"Error in background email thread: {e}")

@app.route('/')
def home():
    """A simple health check endpoint."""
    return "OK"

@app.route('/run')
def run_email_task():
    """Triggers the email sending in a background thread."""
    # 1. Check for the secret token for security
    provided_token = request.args.get('token')
    expected_token = os.getenv('TRIGGER_TOKEN')

    if not provided_token or provided_token != expected_token:
        return jsonify({"error": "unauthorized"}), 401

    # 2. Create and start the background thread
    email_thread = threading.Thread(target=send_email_in_background)
    email_thread.start()
    
    # 3. Respond immediately to the web request
    return jsonify({"status": "email task triggered"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

