import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(file_path):
    email_user = "your_email@example.com"
    email_password = "your_password"
    email_to = "recipient@example.com"

    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = email_to
    msg["Subject"] = "Exported Excel File"

    logger.info(f"Attaching file: {file_path}")
    with open(file_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
    part["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
    msg.attach(part)

    logger.info("Sending email.")
    with smtplib.SMTP_SSL("smtp.example.com", 465) as server:
        server.login(email_user, email_password)
        server.sendmail(email_user, email_to, msg.as_string())
    logger.info("Email sent successfully.")
