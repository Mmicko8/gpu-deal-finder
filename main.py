# ########################################### Description ##############################################################
# Script name: Good Gpu Deal Finder
# Author: Michel Matthe
# Email: matthe.michel@gmail.com
# Required modules: requests_html, pandas, smtplib, getpass, ssl, csv

# This program scrapes www.2dehands.be for gpu listings and sends an email alert if there are listings which fit the
# requirements.

# price_requirements contains the names of the GPU models the program wil look for and the maximum price for each model
# example: price_requirements contains 'gtx 1080,200' : this means it will send an email alert only if it finds
# gpu listings for gtx 1080 models listed for 200 euro or less

# IF RUNNING ON PyCharm -> enable 'Emulate terminal in output console' in 'Edit configurations...' option

# ########################################### Imports ##################################################################

from scraper import scrape
from extracter import extract
from analyser import analyse
from Unduplicater import un_duplicate
from mailer import email

# ########################################### Arguments ################################################################

# Scrape
url = 'https://www.2dehands.be/l/computers-en-software/videokaarten/#Language:nl-BE|sortBy:SORT_INDEX|sortOrder:' \
      'DECREASING'  # url of the website that will be scraped
html_file_path = 'data/scraped_page.txt'  # path of the file where the scraped html will be saved

# Extract
extracted_data_file_path = 'data/extracted_data.csv'  # path of the file where the extracted data will be saved

# Analyse
old_deals_path = 'data/old_gpu_deals.txt'  # path of the file where the gpu deals of which an alert was
# already sent are stored to prevent duplicates

gpu_deals_path = 'data/gpu_deals.txt'  # path of the file where the information of the gpu's that match
# the requirements are saved

price_requirements = 'resources/price_requirements.csv'  # path of the csv file with the gpu model names and prices
# EDIT this file to customise which gpu's to send an alert for at which price

# Email
email_send = "michel.2dehandsscript@gmail.com "  # Email address that will send the email requires less secure access to
# be enabled
email_receive = "michel.matthe@live.co.uk"  # Email address that will receive the email
smtp_server = "smtp.gmail.com"  # address of the smtp server of the sender email


# ########################################### Program ##################################################################


def main():
    # scrape
    scrape(url, html_file_path)

    # Extract
    extract(html_file_path, extracted_data_file_path)

    # analyse
    df = analyse(extracted_data_file_path, price_requirements)

    # remove duplicates
    df = un_duplicate(df, old_deals_path)
    df.to_csv(gpu_deals_path, sep='\t')

    # email
    with open(gpu_deals_path, 'r') as file:
        message = file.read()
    if len(message.split('\n')) == 2:
        print("No deals found.")
        return
    message = message.replace('\n', '\n\n')  # extra line whitespace for readability
    email('gpu Alert', message, email_receive, email_send, smtp_server)


if __name__ == "__main__":
    main()
