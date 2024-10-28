import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import requests
import logging
import random

# Setup logging
logging.basicConfig(level=logging.INFO)

# Set up email configuration (use environment variables for security)
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# Set up the URL and text to check
URL_TO_CHECK = os.getenv("URL_TO_CHECK")
TEXT_TO_FIND = os.getenv("TEXT_TO_FIND", "important text")

# Time between every check
MIN_TIME_TO_SLEEP = int(os.getenv("TIME_TO_SLEEP", 30))
MAX_TIME_TO_SLEEP = int(os.getenv("TIME_TO_SLEEP", 60))

DEBUG = int(os.getenv("DEBUG", 1))

def send_email():
    global last_email_sent
    """Send an email notification."""
    subject = "Text Missing Notification"
    body = f"The text '{TEXT_TO_FIND}' is missing from the webpage '{URL_TO_CHECK}'."

    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(LOGIN, PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        logging.info("Email sent successfully.")
        return True
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"Authentication error: {e}")
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
    return False

def check_text_in_webpage():
    """Check if the text exists on the webpage."""
    try:
        response = requests.get(URL_TO_CHECK, timeout=10)
        response.raise_for_status()
        if DEBUG == 1:
            logging.info(f"Response status: {response.status_code}")
            logging.info(f"Response content: {response}")
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
                success = send_email()
                if success:
                    last_email_sent = current_time
                else:
                    last_email_sent = 0
            else:
                logging.info("No email send, cooldown period is active.")
        else:
            logging.info(f"'{TEXT_TO_FIND}' found on '{URL_TO_CHECK}'.")
        time_sleep = random.randint(MIN_TIME_TO_SLEEP, MAX_TIME_TO_SLEEP)
        logging.info(f"Checking again in '{time_sleep}' seconds.")
        time.sleep(time_sleep)

if __name__ == "__main__":
    main()
