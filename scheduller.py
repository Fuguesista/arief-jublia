from datetime import datetime
from model.email_model.email_model import *
from main import app, db, data_config
from time import sleep
import email, smtplib, ssl
# from email import encoders
# from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = data_config["SENDER_EMAIL"]
password = data_config["SENDER_PASSWORD"]


def generate_text_email (to_email, subject_email, body_text:str):
    global sender_email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject_email

    message.attach(MIMEText(body_text, "html"))
    return message.as_string()

while True:
    with app.app_context():
        while True:
            list_emails = get_due_emails()
            if (len(list_emails) > 0):
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    for data in list_emails:
                        server.sendmail(sender_email, data.email_receipt, generate_text_email(data.email_receipt, data.email_subject, data.email_content))
                        data_email_done = Email.query.get_or_404(data.id)
                        data_email_done.is_sended = True
                        data_email_done.time_send = int(datetime.now().timestamp())
        sleep(0.1)
    