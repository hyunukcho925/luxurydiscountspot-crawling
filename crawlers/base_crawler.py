from supabase import Client, create_client
from bs4 import BeautifulSoup
import requests
import logging

class BaseCrawler:
    def __init__(self, config):
        self.config = config
        self.supabase: Client = config.supabase
        self.logger = logging.getLogger('crawler')

    def get_soup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.content, 'html.parser')

    def crawl(self):
        raise NotImplementedError("Subclasses must implement the crawl method")