import argparse
import requests
from bs4 import BeautifulSoup
import logging
from base64 import b16encode
import io
import os 
from utils import *



class Crawler(object):

    def __init__(self, start_url, storage_dir, mylogger=None):
        self.headers = { 'User-Agent': 'SearchReddit bot 0.1', }
        self.start_url = start_url
        self.storage_dir = storage_dir
        self.mylogger = mylogger

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
                self.mylogger.debug("We GOT AN EXCEPTION: {}".format(e))
                break
            self.mylogger.debug(next_page_url)


def main():
    logger = logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description='/r/learnprogramming')
    parser.add_argument('--start_url', dest='start_url')
    parser.add_argument('--storage_dir', dest='storage_dir')
    args = parser.parse_args()

    my_crawler = Crawler(args.start_url, args.storage_dir, mylogger=logger)
    my_crawler.crawl()


if __name__== '__main__':
    main()
