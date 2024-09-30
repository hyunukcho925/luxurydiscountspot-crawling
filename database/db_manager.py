import logging
from datetime import datetime
from postgrest.exceptions import APIError

class DBManager:
    def __init__(self, config):
        self.supabase = config.supabase
        self.logger = logging.getLogger('crawler')

    async def save_crawl_results(self, results):
        for result in results:
            try:
                result['crawled_at'] = datetime.now().isoformat()  # 이 줄을 추가
                await self.save_price_crawl(result)
                await self.update_crawl_target(result['crawl_target_id'])
            except Exception as e:
                self.logger.error(f"Error saving crawl result: {str(e)}")

    async def save_price_crawl(self, result):
        try:
            data = {
                'crawl_target_id': str(result['crawl_target_id']),  # UUID를 문자열로 변환
                'price': result['price'],
                'currency': result.get('currency', 'Unknown'),
                'crawled_at': result['crawled_at']
            }
            response = await self.supabase.table('price_crawls').insert(data).execute()
            
            if response and response.data:
                self.logger.info(f"Successfully saved price crawl for target {result['crawl_target_id']}")
            else:
                self.logger.warning(f"No data returned when saving price crawl for target {result['crawl_target_id']}")
            
            self.logger.debug(f"Supabase response: {response}")
        except Exception as e:
            self.logger.error(f"Unexpected error in save_price_crawl: {str(e)}")
            self.logger.exception("Exception details:")

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
            self.logger.error(f"Supabase API Error in update_crawl_target: {str(e)}")
            self.logger.exception("Exception details:")