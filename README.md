##Craigslist Price Checker
This project is used to find low price computer parts and send automated email notifications with a csv filled with regex specified items in a certain price range. This was implmeneted in crontabs to search every hour and send the updated csv once a day. 

#Dependencies
Unix based system for crontab
Python 3.8
Python libraries:
	`requests`
	`smtplib`
	`email.mime.text`
	`bs4`
	`urllib`
	`re`
	`csv`
	
#running the project
Prerequisite: Replace emails in `email_listings.py` with email addresses you want to send and recieve. Replace password with gmail app password.

For automation add cronfile to crontab:
	`crontab cronfile`

for manual runs:
	`python price_check.py`
	`pytonh email_listings.py`

