import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import requests

# Set up email configuration (use environment variables for security)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# Set up the URL and text to check
URL_TO_CHECK = os.getenv("URL_TO_CHECK")
TEXT_TO_FIND = os.getenv("TEXT_TO_FIND", "important text")

def send_email():
    """Send an email notification."""
    subject = "Text Missing Notification"
    body = f"The text '{TEXT_TO_FIND}' is missing from the webpage '{URL_TO_CHECK}'."

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_text_in_webpage():
    """Check if the text exists on the webpage."""
    try:
        response = requests.get(URL_TO_CHECK, timeout=10)
        response.raise_for_status()
        return TEXT_TO_FIND in response.text
    except requests.RequestException as e:
        print(f"Error accessing '{URL_TO_CHECK}': {e}")
        return False

def main():
    while True:
        if not check_text_in_webpage():
            print(f"'{TEXT_TO_FIND}' not found on '{URL_TO_CHECK}'. Sending email.")
            send_email()
            break
        print(f"'{TEXT_TO_FIND}' found on '{URL_TO_CHECK}'. Checking again in 30 seconds.")
        time.sleep(30)

if __name__ == "__main__":
    main()
