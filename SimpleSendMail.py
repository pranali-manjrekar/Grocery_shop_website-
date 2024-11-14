# Python code to illustrate Sending mail from
# your Gmail account
import smtplib
# creates SMTP session
from idlelib.idle_test.test_run import S

s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication


# message to be sent
#message = "Message_you_need_to_send"
# sending the mail


def SendMail(receiver, message):
    try:
        sender = "vitmumbai17@gmail.com"
        password = "project17"
        s.login(sender,password)
        s.sendmail(sender, receiver, message)
        print("Successfully sent email")
        # terminating the session
        s.quit()
    except Exception as e:
        print("Error: unable to send email")
        # terminating the session
        s.quit()


#SendMail("vitmumbai17@gmail.com","It's test mail")