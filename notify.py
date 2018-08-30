import smtplib, platform
from email.message import EmailMessage
from secrets import noti_from, noti_pass, noti_to


def prod_only(func):
    def wrapper(*args, **kwargs):
        if 'Linux' in platform.platform():
            func(*args, **kwargs)
    return wrapper

@prod_only
def send_email(subject,body=" "):

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "Notis <"+noti_from+">"
    msg['To'] = [noti_to]
    msg.set_content(body)

    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.login( noti_from, noti_pass )
    server.send_message(msg)
    server.quit()
