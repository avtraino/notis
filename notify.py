import smtplib, platform
from email.message import EmailMessage
from secrets import noti_from, noti_pass, noti_default_to
import argparse

def prod_only(func):
    def wrapper(*args, **kwargs):
        if '-gcp-' in platform.platform():
            func(*args, **kwargs)
        else:
            print("not in Prod, suppressing email")
    return wrapper

@prod_only
def send_email(subject="(no subject)", body=" ", send_to=noti_default_to, content_type="text/plain"):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "Notis <"+noti_from+">"
    msg['To'] = send_to

    if content_type == "text/html":
        msg.add_header('Content-Type','text/html')
        msg.set_payload(body.encode("utf8"))
    else:
        msg.set_content(body)

    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.login( noti_from, noti_pass )
    server.send_message(msg)
    server.quit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--subject')
    parser.add_argument('--body')
    parser.add_argument('--to', dest='send_to')
    parser.add_argument('--content-type')
    args = parser.parse_args()

    send_email(args.subject, args.body, args.send_to, args.content_type)