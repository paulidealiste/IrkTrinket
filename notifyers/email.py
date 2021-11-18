import smtplib
import ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "Automated email from the InkTrinket screenshot monitoring app"
body = "This email was automatically sent by InkTrinket with the current desktop state."
sender_email = ''
sender_pass = ''


def send_report(receiver_email, current_progress, report_path):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))
    
    with open(report_path, 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename='current_snapshot.png')
        message.attach(img)

    with smtplib.SMTP("smtp.mail.yahoo.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
