#!/usr/bin/python3.8
import smtplib
from email.mime.text import MIMEText
import csv

#read in csv file
deal_listings = []
with open('listings.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        deal_listings.append(row)

#create body of message
body = "New parts found\n"
for i in range(1,6):
    body+="{} available for ${} in {}\n".format(deal_listings[i][0], deal_listings[i][1], deal_listings[i][2])

#email setup
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

#get time for email subject
now = datetime.now()
date = now.strftime("%d/%m/%Y")
time = now.strftime("%I:%M:%S %p")

#sending using app password from gmail account
subject = "New Parts from {} {}".format(date, time)
sender = "xxxx@gmail.com"
recipients = ["xxxx@gmail.com"]
#use gmail app password here
password = "xxxx xxxx xxxx xxxx"

send_email(subject, body, sender, recipients, password)
