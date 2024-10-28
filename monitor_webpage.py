import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Set up email configuration (use environment variables for security)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# Set up the URL and text to check
URL_TO_CHECK = os.getenv("URL_TO_CHECK")
TEXT_TO_FIND = os.getenv("TEXT_TO_FIND", "important text")

# Time between every check
TIME_TO_SLEEP = int(os.getenv("TIME_TO_SLEEP", 30))

def send_email():
    global last_email_sent
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
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        last_email_sent = 0


def check_text_in_webpage():
    """Check if the text exists on the webpage."""
    try:
        response = requests.get(URL_TO_CHECK, timeout=10)
        response.raise_for_status()
        return TEXT_TO_FIND in response.text
    except requests.RequestException as e:
        logging.error(f"Error accessing '{URL_TO_CHECK}': {e}")
        return False

last_email_sent = 0
cooldown_period = 3600/4 # Cooldown period of 15 minutes in seconds

def main():
    global last_email_sent
    while True:
        current_time = time.time()
        if not check_text_in_webpage():
            logging.warning(f"'{TEXT_TO_FIND}' not found on '{URL_TO_CHECK}'.")
            if current_time - last_email_sent > cooldown_period:
                logging.info("Sending email.")
                send_email()
                last_email_sent = current_time
            else:
                logging.info("No email send, cooldown period is active.")
        else:
            logging.info(f"'{TEXT_TO_FIND}' found on '{URL_TO_CHECK}'.")
        logging.info(f"Checking again in '{TIME_TO_SLEEP}' seconds.")
        time.sleep(TIME_TO_SLEEP)

if __name__ == "__main__":
    main()
