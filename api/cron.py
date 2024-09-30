import sys
from pathlib import Path
import asyncio
from config.config import Config
from database.db_manager import DBManager
from crawlers.site_crawlers import get_all_crawlers
from utils.logger import setup_logger
import supabase

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

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
            results = crawler.crawl()  # 비동기 호출 제거
            db_manager.save_crawl_results(results)  # 비동기 호출 제거
            logger.info(f"Completed crawl for crawler: {crawler.__class__.__name__}")
        except Exception as e:
            logger.error(f"Error during crawl for crawler: {crawler.__class__.__name__}: {str(e)}")
            logger.exception("Exception details:")

def handler(event, context):
    try:
        logger.info("Starting crawler application")
        run_crawlers()
        return {
            "statusCode": 200,
            "body": "Crawling completed"
        }
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": f"Internal Server Error: {str(e)}"
        }