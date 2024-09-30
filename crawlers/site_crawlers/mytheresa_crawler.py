from crawlers.base_crawler import BaseCrawler
from bs4 import BeautifulSoup
import re
from utils.currency_converter import currency_converter

class MytheresaCrawler(BaseCrawler):
    def __init__(self, config):
        self.site_id = "2e33b667-8e9a-466e-969e-7592f9822459"
        super().__init__(config)

    async def crawl(self):
        response = self.supabase.table('crawl_targets') \
            .select('id, site_id, site_product_url, is_active') \
            .execute()

        self.logger.debug(f"Supabase response: {response}")

        results = []
        for target in response.data:
            if target['site_id'] == self.site_id and target['is_active']:
                url = target['site_product_url']
                try:
                    self.logger.debug(f"Crawling URL: {url}")
                    soup = self.get_soup(url)
                    price = self.extract_price(soup)
                    
                    results.append({
                        'price': price,
                        'url': url,
                        'crawl_target_id': target['id'],
                        'is_successful': price is not None
                    })
                    self.logger.debug(f"Extracted price for {url}: {price}")
                except Exception as e:
                    self.logger.error(f"Error crawling {url}: {str(e)}")
                    results.append({
                        'price': None,
                        'url': url,
                        'crawl_target_id': target['id'],
                        'is_successful': False
                    })

        return results

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
                    self.logger.error(f"Error converting currency: {str(e)}")
        return None