import logging
from datetime import datetime
import asyncio

class DBManager:
    def __init__(self, config):
        self.supabase = config.supabase
        self.logger = logging.getLogger('crawler')

    async def save_crawl_results(self, results):
        tasks = []
        for result in results:
            result['crawled_at'] = datetime.now().isoformat()
            tasks.append(self.save_price_crawl(result))
            tasks.append(self.update_crawl_target(result['crawl_target_id']))
        
        await asyncio.gather(*tasks, return_exceptions=True)

    async def save_price_crawl(self, result):
        try:
            data = {
                'crawl_target_id': str(result['crawl_target_id']),
                'price': result['price'],
                'currency': result.get('currency', 'KRW'),
                'crawled_at': result['crawled_at']
            }
            response = await self.supabase.table('price_crawls').insert(data).execute()
            
            if response and response.data:
                self.logger.info(f"Successfully saved price crawl for target {result['crawl_target_id']}")
            else:
                self.logger.warning(f"No data returned when saving price crawl for target {result['crawl_target_id']}")
            
            self.logger.debug(f"Supabase response: {response}")
        except Exception as e:
            self.logger.exception(f"Unexpected error in save_price_crawl for target {result['crawl_target_id']}")

    async def update_crawl_target(self, crawl_target_id):
        try:
            data = {'last_crawled_at': datetime.now().isoformat()}
            response = await self.supabase.table('crawl_targets').update(data).eq('id', str(crawl_target_id)).execute()

            if response and response.data:
                self.logger.info(f"Successfully updated crawl target {crawl_target_id}")
            else:
                self.logger.warning(f"No data returned when updating crawl target {crawl_target_id}")

            self.logger.debug(f"Supabase response: {response}")
        except Exception as e:
            self.logger.exception(f"Supabase API Error in update_crawl_target for target {crawl_target_id}")

    async def batch_insert_price_crawls(self, results):
        try:
            data = [{
                'crawl_target_id': str(result['crawl_target_id']),
                'price': result['price'],
                'currency': result.get('currency', 'KRW'),
                'crawled_at': result['crawled_at']
            } for result in results]

            response = await self.supabase.table('price_crawls').insert(data).execute()

            if response and response.data:
                self.logger.info(f"Successfully batch inserted {len(data)} price crawls")
            else:
                self.logger.warning("No data returned when batch inserting price crawls")

            self.logger.debug(f"Supabase response: {response}")
        except Exception as e:
            self.logger.exception("Unexpected error in batch_insert_price_crawls")