#!/usr/bin/python3.8
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import urlopen
import csv
import re

#getting info of first page to find necissary information such as total results
site = 'https://chico.craigslist.org/search/gra?lang=ja'
html = urlopen(site)
soup = BeautifulSoup(html, 'lxml')

#find number of total results to know how many pages to iterate throuh
total_results = soup.find('span', class_='totalcount')
total_results = int(total_results.text)

#how many pages of results there are
if total_results < 120:
    num_loops = 1
else:
    num_loops = total_results / 120

#initialize variables
page_number = 0
num_products = 0 #REQUIRED parameter NumProducts
listing_data = []

#loop through each page of results
for i in range(int(num_loops)):
    #get results of current page
    site = 'https://chico.craigslist.org/search/syp?s={}&lang=ja'.format(page_number)
    html = urlopen(site)
    soup = BeautifulSoup(html, 'lxml')

    #look through each result from computer parts
    for listing in soup.find_all('li', class_='result-row'):
        #find each listing's title, price, and city
        listing_title = listing.find('a', class_='result-title')
        listing_price = listing.find('span', class_= 'result-price')
        listing_city = listing.find('span', class_= 'result-hood')

        #check if city is listed, if not make city No city data
        if listing_city is not None:
            listing_city = listing_city.text.replace('(', '').replace(')', '').replace(' ', '')
        else:
            listing_city = "No city data"
        listing_price = int(listing_price.text.replace('$', '').replace(',', ''))
        listing_title = listing_title.text

        max_price = 140 #max price to search for
        min_price = 2 #help deal with people listing at $2

        #use regex to look for product under certain dollar amount
        if re.match('^.*([Gg]raphic|[Pp]ower.*[Ss]upply|[Cc][Pp][Uu]|[Mm]onitor).*$', listing_title.lower()):
            if listing_price < max_price and listing_price > min_price:
                num_products = num_products+1
                #make dictionary of results for desks
                listing_data.append({'Title': listing_title, 'Price': listing_price, 'City': listing_city})

    #Move to next page. Every page has 120 results
    page_number = page_number+120

#sort dictionary by price
listing_data = sorted(listing_data, key=lambda x: x['Price'])

#grab current date and time to put in csv
now = datetime.now()
date = now.strftime("%d/%m/%Y")

#get time in 12 hr format
time = now.strftime("%I:%M:%S %p")

#create csv to write out found items
field_labels = ['Title', 'Price', 'City', 'Date', 'Time']

#grab current items in csv to compare later so no repeat listings
existing_identifiers = set()
try:
    with open('listings.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        #read current csv to store existing rows so there are no repeats
        for row in reader:
            #strip out whitespace for comparison
            title = row['Title'].strip()
            price = str(row['Price']).strip()
            city = row['City'].strip()
            identifier = (title, price, city)
            existing_identifiers.add(identifier)
except FileNotFoundError: #if file doesnt exist create file and write header in
    with open('listings.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_labels)
        writer.writeheader()

#append to file new listings
with open('listings.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_labels)

    for new_data in listing_data:
        #strip whitespace for comparison
        title = new_data['Title'].strip()
        price = str(new_data['Price']).strip()
        city = new_data['City'].strip()
        identifier = (title, price, city)
        #make sure row isn't already in csv
        if identifier not in existing_identifiers:
            new_data['Date'] = date
            new_data['Time'] = time
            writer.writerow(new_data)
            existing_identifiers.add(identifier)
