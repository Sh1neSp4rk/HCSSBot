# EmailSender.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def send_email(subject, body, attachment_file):
    logging.info("Setting up the email details")
    from_email = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')
    to_email = os.getenv('TARGET_EMAIL')

    if not from_email or not email_password or not to_email:
        logging.error("Email credentials or target email address are not set in environment variables")
        raise ValueError("Email credentials or target email address are not set in environment variables")

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    logging.info(f"Attaching file: {attachment_file}")
    with open(attachment_file, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_file)}')
        msg.attach(part)

    # Connect to the server and send the email
    logging.info("Connecting to the email server and sending email")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, email_password)
        server.send_message(msg)
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
    finally:
        server.quit()
