import requests
from bs4 import BeautifulSoup
import logging
from base64 import b16encode
import io
import os 



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



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


class Crawler(object):

    def __init__(self, start_url, storage_dir):
        self.headers = { 'User-Agent': 'SearchReddit bot 0.1', }
        self.start_url = start_url
        self.storage_dir = storage_dir

    @staticmethod
    def _make_absolute_url(url):
        return 'https://reddit.com' + url

    def crawl(self):
        current_page_url = self.start_url
        while True:
            current_page = downloadUrl(current_page_url, headers=self.headers)
            soup = BeautifulSoup(current_page)
            all_posts_links = soup.findAll('a', attrs={'class': 'title'})
            post_links = [Crawler._make_absolute_url(link['href']) for link in all_posts_links]

            for post_link in post_links:
                html = downloadUrl(post_link, headers=self.headers)
                stored_text_file_name = os.path.join(self.storage_dir, b16encode(post_link))

                with io.open(stored_text_file_name, 'w', encoding='utf8') as stored_text_file:
                    stored_text_file.write(html)

            try:
                next_page_url = soup.find('a', attrs={'rel': 'next'})['href']
                current_page_url = next_page_url
            except Exception as e:
                logger.debug("We GOT AN EXCEPTION: {}".format(e))
                break
            logger.debug(next_page_url)




