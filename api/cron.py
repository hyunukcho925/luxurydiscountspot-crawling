from http.server import BaseHTTPRequestHandler
import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config
from database.db_manager import DBManager
from crawlers.mytheresa_crawler import MytheresaCrawler

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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        run_crawlers()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Crawling completed'.encode())
        return