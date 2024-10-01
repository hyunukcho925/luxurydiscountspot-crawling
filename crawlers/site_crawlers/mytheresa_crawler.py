from crawlers.base_crawler import BaseCrawler
import re
from utils.currency_converter import currency_converter

class MytheresaCrawler(BaseCrawler):
    def __init__(self, config):
        super().__init__(config)
        self.site_id = "2e33b667-8e9a-466e-969e-7592f9822459"

    async def crawl(self):
        response = await self.supabase.table('crawl_targets') \
            .select('id, site_id, site_product_url, is_active') \
            .eq('site_id', self.site_id) \
            .eq('is_active', True) \
            .execute()

        self.logger.debug(f"Supabase response: {response}")

        results = []
        for target in response.data:
            try:
                url = target['site_product_url']
                self.logger.debug(f"Crawling URL: {url}")
                soup = await self.get_soup(url)
                price = self.extract_price(soup)
                
                results.append({
                    'price': price,
                    'url': url,
                    'crawl_target_id': target['id'],
                    'is_successful': price is not None
                })
                self.logger.debug(f"Extracted price for {url}: {price}")
            except Exception as e:
                self.logger.exception(f"Error crawling {url}")
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
                    self.logger.exception(f"Error converting currency")
        return None