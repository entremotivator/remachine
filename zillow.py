from typing import List
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests

def create_url(zipcode: int, sort_by: str=None) -> str:
    """Generates a URL to the Zillow properties listed for the given zipcode."""
    sort_options = {
        'newest': 'days_sort',
        'high-low': 'priced_sort',
        'low-high': 'pricea_sort'
    }
    option = sort_options.get(sort_by, 'globalrelevanceex_sort')
    url = f'https://www.zillow.com/homes/for_sale/{zipcode}/0_singlestory/{option}'
    return url

def get_zpids(zipcode: int, sort_by: str=None) -> List[int]:
    """Extracts all Zillow Property ID's (zpid) for each listing in the given zipcode."""
    url = create_url(zipcode, sort_by)
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=headers)
    webpage = urlopen(req).read()
    
    # Parse the HTML into a tree
    soup = BeautifulSoup(webpage, 'html.parser')
    listings = soup.find('ul', {'class': 'photo-cards photo-cards_wow photo-cards_short'})
    
    def _extract_zpid(li: Tag) -> int:
        article = li.find('article', {'class': 'list-card list-card-short list-card_not-saved'})
        if article is None:
            return None
        return int(article.get('id').replace('zpid_', ''))

    zpids = []
    for li in listings.find_all('li'):
        zpid = _extract_zpid(li)
        if zpid is not None:
            zpids.append(zpid)
    return zpids

def fetch_property_details(api_key: str, zpid: int):
    """Fetch property details from Zillow API using the ZPID."""
    url = "https://zillow-zestimate.p.rapidapi.com/zestimate"
    querystring = {"zpid": str(zpid)}
    
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "zillow-zestimate.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
