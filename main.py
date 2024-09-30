import schedule
import time
from config.config import Config
from database.db_manager import DBManager
from crawlers.site_crawlers import get_all_crawlers
from utils.logger import setup_logger
import supabase

logger = setup_logger()
config = Config()
db_manager = DBManager(config)

logger.debug(f"Supabase version: {supabase.__version__}")
logger.debug(f"Config: {config}")
logger.debug(f"Supabase client: {config.supabase}")

def run_crawlers():
    crawlers = get_all_crawlers(config)
    for crawler in crawlers:
        try:
            logger.info(f"Starting crawl for crawler: {crawler.__class__.__name__}")
            results = crawler.crawl()
            db_manager.save_crawl_results(results)
            logger.info(f"Completed crawl for crawler: {crawler.__class__.__name__}")
        except Exception as e:
            logger.error(f"Error during crawl for crawler: {crawler.__class__.__name__}: {str(e)}")
            logger.exception("Exception details:")

def main():
    logger.info("Starting crawler application")
    
    # 즉시 한 번 실행
    run_crawlers()
    
    # 매일 자정에 실행하도록 스케줄 설정
    schedule.every().day.at("00:00").do(run_crawlers)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()