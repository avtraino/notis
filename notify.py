import smtplib, platform
from email.message import EmailMessage
from secrets import noti_from, noti_pass, noti_default_to


def prod_only(func):
    def wrapper(*args, **kwargs):
        if '-gcp-' in platform.platform():
            func(*args, **kwargs)
    return wrapper

@prod_only
def send_email(subject, body=" ", send_to=noti_default_to):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "Notis <"+noti_from+">"
    msg['To'] = send_to
    msg.set_content(body)

    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.login( noti_from, noti_pass )
    server.send_message(msg)
    server.quit()
