import requests
from bs4 import BeautifulSoup


def downloadUrl(url, headers=None):
    # assert url.startswith('https://www.reddit.com/r/learnprogramming/')
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception('non-OK- status code: {}'.format(r.status_code))
    return r.text


def parseRedditPost(html):
    soup = BeautifulSoup(html)
    hdata = soup.select('div.usertext-body')[1]
    tdata = hdata.text
    return tdata


