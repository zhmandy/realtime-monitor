import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = ''
my_pass = ''
my_user = ''


def sendemail():
    try:
        msg = MIMEText('Alert! Undefined Person!', 'plain', 'utf-8')
        msg['From'] = formataddr(["RaspberryPi Camera", my_sender])
        msg['To'] = formataddr(["Receiver", my_user])
        msg['Subject'] = "Warning!"

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user], msg.as_string())
        result = True
        server.quit()
    except Exception:
        result = False
    return result


result = sendemail()
if result:
    print("Success")
else:
    print("Fail")
