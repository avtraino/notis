import smtplib
from email.message import EmailMessage
from secrets import noti_from, noti_pass, noti_to




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