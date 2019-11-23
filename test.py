import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.mime.application
from datetime import date

import schedule


def dgr_mail():
    plant_name=''

    Subject = "Daily Generation Report  of "+ plant_name + " - "+str(date.today())
    
	TO = []

    message = """Hi 
    You're receiving this e-mail because I'm testing my code """
    folder_name='path to the folder'
    msg = MIMEMultipart()
    FROM = "email"
    # Prepare actual message
    msg['Subject'] = Subject
    msg['From'] = FROM
    msg['To'] = ", ".join(TO)
    msg.attach(MIMEText(message, 'plain'))
    fo=open(folder_name,'rb')
    attach = email.mime.application.MIMEApplication(fo.read(),_subtype="pdf")
    fo.close()
    attach.add_header('Content-Disposition','attachment',filename='')

    msg.attach(attach)
    server = smtplib.SMTP_SSL('zimsmtp.logix.in', 465)
    server.login("email-address", "pasword")
    server.sendmail(FROM,TO, msg.as_string())
    print('mail is sent')
    server.quit()


schedule.every().day.at("18:30").do(dgr_mail)
while True:
    schedule.run_pending()
    time.sleep(1)





