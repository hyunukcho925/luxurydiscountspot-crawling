import sys
import os
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.config import Config
from database.db_manager import DBManager
from crawlers.site_crawlers.mytheresa_crawler import MytheresaCrawler

config = Config()
db_manager = DBManager(config)

def run_crawlers():
    crawlers = [MytheresaCrawler(config)]
    for crawler in crawlers:
        try:
            results = crawler.crawl()
            db_manager.save_crawl_results(results)
        except Exception as e:
            print(f"Error during crawl: {str(e)}")

def handler(request):
    if request.method == "GET":
        run_crawlers()
        return {
            "statusCode": 200,
            "body": "Crawling completed"
        }
    else:
        return {
            "statusCode": 405,
            "body": "Method not allowed"
        }