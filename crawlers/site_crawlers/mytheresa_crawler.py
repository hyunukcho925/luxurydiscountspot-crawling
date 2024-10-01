from crawlers.base_crawler import BaseCrawler
from bs4 import BeautifulSoup
import re
from utils.currency_converter import currency_converter
import httpx
import asyncio

class MytheresaCrawler(BaseCrawler):
    def __init__(self, config):
        self.site_id = "2e33b667-8e9a-466e-969e-7592f9822459"
        super().__init__(config)

    async def crawl(self):
        try:
            response = await self.supabase.table('crawl_targets') \
                .select('id, site_id, site_product_url, is_active') \
                .eq('site_id', self.site_id) \
                .eq('is_active', True) \
                .execute()

            self.logger.debug(f"Supabase response: {response}")

            tasks = [self.crawl_single_target(target) for target in response.data]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return [result for result in results if result is not None and not isinstance(result, Exception)]
        except Exception as e:
            self.logger.exception("Error in crawl method")
            return []

    async def crawl_single_target(self, target):
        url = target['site_product_url']
        try:
            self.logger.debug(f"Crawling URL: {url}")
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
            price = self.extract_price(soup)
            
            return {
                'price': price,
                'url': url,
                'crawl_target_id': target['id'],
                'is_successful': price is not None
            }
        except Exception as e:
            self.logger.exception(f"Error crawling {url}")
            return None

    def extract_price(self, soup):
        price_element = soup.find('span', class_='pricing__prices__price')
        if price_element:
            price_text = price_element.text.strip()
            currency_match = re.search(r'[€$£]', price_text)
            currency = 'EUR' if currency_match and currency_match.group() == '€' else 'USD'
            
            price = re.sub(r'[^\d.]', '', price_text)
            if price:
                price = float(price)
                try:
                    price_krw = currency_converter.convert_to_krw(price, currency)
                    return price_krw
                except ValueError as e:
                    self.logger.exception(f"Error converting currency")
        return None