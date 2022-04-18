
from bs4 import BeautifulSoup as bSoup
from requests_html import HTMLSession
import pandas as pd


def open_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def find_price(listing, link):
    """
    Extracts the price from the gpu listing.
    :param listing: the gpu listing
    :param link: the link to the gpu listing's full product page'
    :return: the price of the gpu listing
    """
    price = listing.select_one('.mp-Listing-price').text

    if price in ['Gereserveerd', 'Prijs o.t.k.']:
        return None

    elif price == 'Gratis':
        return '0'

    elif price == 'Bieden':
        # scrapes data from the full product page of the listing
        # if no set price but bids -> return highest bid -> if no bids return minimum bid
        session = HTMLSession()
        resp = session.get(link)
        resp.html.render(sleep=1)
        soup = bSoup(resp.html.html, 'html.parser')

        bid = soup.select_one('.BiddingList-price')
        if bid is None:
            return bid
        return bid.text[2:]

    else:
        return price[2:]


# def find_date(link):
#     session = HTMLSession()
#     resp = session.get(link)
#     resp.html.render(sleep=0.2)
#     soup = bSoup(resp.html.html, 'html.parser')
#     date = soup.select_one('.Stats-stat:last-of-type .Stats-summary')
#     print(date.text)


def extract(html_file_path, csv_file_path):
    """
    Extracts the title, date, seller name, location, link and price of every gpu listing from the scraped HTML.
    Saves the data to a csv_file.

    :param html_file_path: path of the file containing the scraped HTML
    :param csv_file_path: path of the csv file where the extracted data gets saved to
    """
    soup = bSoup(open_html(html_file_path), 'html.parser')
    listings = soup.select_one('.mp-Listings')
    data = []
    for listing in listings:
        if listing.name == 'li':
            title = listing.select_one('.mp-Listing-title').text.lower()
            # description = listing.select_one('.mp-Listing-description').text
            # date = listing.select_one('.mp-Listing-date').text
            seller_name = listing.select_one('.mp-Listing-seller-name').text
            seller_location = listing.select_one('.mp-Listing-location').text
            link = 'https://www.2dehands.be' + listing.select_one('a')['href']

            price = find_price(listing, link)

            data.append({'title': title, 'price': price, 'seller_name': seller_name, 'seller_location': seller_location,
                         'link': link})

    df = pd.DataFrame(data, )
    df.dropna(inplace=True, subset=['price'])
    df.to_csv(csv_file_path, sep=';')

# extract('html_saved/mainTest.txt', 'data/mainTest.csv')
