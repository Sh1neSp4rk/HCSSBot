# Tools/email_sender.py
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import logging

def send_email(attachments, recipient_email):
    sender_email = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')

    if not sender_email or not email_password:
        raise ValueError("Email address or password is missing")

    subject = "HCSSBot API Data Files"
    body = f"The following files have been generated and are attached:\n\n" + "\n".join(attachments)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for file in attachments:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file)}')
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        logging.info(f"Email sent to {recipient_email}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
