from supabase import Client
from bs4 import BeautifulSoup
import httpx
import logging
import asyncio

class BaseCrawler:
    def __init__(self, config):
        self.config = config
        self.supabase: Client = config.supabase
        self.logger = logging.getLogger('crawler')

    async def get_soup(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return BeautifulSoup(response.content, 'html.parser')

    async def crawl(self):
        raise NotImplementedError("Subclasses must implement the crawl method")