import requests
from bs4 import BeautifulSoup

def downloadUrl(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('non-OK- status code: {}'.format(r.status_code))
    return r.text


def parseText(html):
    soup = BeautifulSoup(html)
    data = soup.select('div.usertext-body')[1]
    return data
