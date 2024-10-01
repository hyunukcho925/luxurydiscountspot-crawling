import asyncio
from config.config import Config
from database.db_manager import DBManager
from crawlers.site_crawlers import get_all_crawlers
from utils.logger import setup_logger

logger = setup_logger()

async def run_crawlers():
    config = Config()
    db_manager = DBManager(config)
    crawlers = get_all_crawlers(config)

    for crawler in crawlers:
        try:
            logger.info(f"Starting crawl for crawler: {crawler.__class__.__name__}")
            results = await crawler.crawl()
            await db_manager.save_crawl_results(results)
            logger.info(f"Completed crawl for crawler: {crawler.__class__.__name__}")
        except Exception as e:
            logger.exception(f"Error during crawl for crawler: {crawler.__class__.__name__}")

async def async_handler(event, context):
    try:
        logger.info("Starting crawler application")
        await run_crawlers()
        return {
            "statusCode": 200,
            "body": "Crawling completed"
        }
    except Exception as e:
        logger.exception("Error in handler")
        return {
            "statusCode": 500,
            "body": f"Internal Server Error: {str(e)}"
        }

def handler(event, context):
    return asyncio.run(async_handler(event, context))