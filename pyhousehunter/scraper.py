# author: Alex Truong Hai Yen
# date: 2021-02-25

from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
 
def scraper(url, online = False):
    """Function to scrape housing data from a given craiglist url

    Parameters
    ----------
    url : url
        The given craiglist url to scrape the data from
    
    online: bool
        Whether the data is scraped directly online from the url (default = False) 
        False means the data is scraped from local HTML file

    Returns
    -------
    pandas.core.frame.DataFrame
        A dataframe containing listing information such as price, house type and neighborhood. 

    Examples
    -------
    >>> scraper(url = 'https://vancouver.craigslist.org/search/van/apa')
    """
    # PART 0: Validate inputs
    # try:

    # except:


    # PART 1: create soup object either from the url or local HTML file
    if online:
        headers = {
            'DNT': '1',
            'Referer': 'https://vancouver.craigslist.org/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        page = requests.get(url, headers = headers)

        # checking scrape status
        if page.status_code == 200:
            print("OK")
        else: 
            print(page.status_code)

        soup = BeautifulSoup(page.text, 'html.parser')
    else:
        soup = BeautifulSoup(open("pyhousehunter/temp/van_housing_listings.html"), "html.parser") # local scraping


    # PART2: extracting information from scrape results into dataframe
    listings = soup.find_all('div', attrs = {'class': 'result-info'})
    data = []

    for i in range(len(listings)):
        listing_id = listings[i].find('a').get('data-id')
        listing_url = listings[i].find('a').get('href')
        price= listings[i].find('span', attrs = {'class': 'result-price'}).text
        
        house = listings[i].find_all('span', attrs = {'class': 'housing'})
        if len(house) != 0:
            house_type = house[0].text.strip().replace(" ", "").replace("\n", "")[:-1]
        else:
            house_type = ""
        
        neighborhood = listings[i].find_all('span', attrs = {'class': 'result-hood'})
        if len(neighborhood) != 0:
            neighborhood = neighborhood[0].text.strip().replace("(","").replace(")","")
        else:
            neighborhood = ""
        data.append((listing_id, listing_url, price, house_type, neighborhood))

    output = pd.DataFrame(
        data,
        columns = ['listing_id', 'listing_url', 'price', 'house_type', 'neighborhood']
    )
    return output