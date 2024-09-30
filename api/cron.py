from http.server import BaseHTTPRequestHandler
import sys
import os
from pathlib import Path
import asyncio

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from config.config import Config
    from database.db_manager import DBManager
    from crawlers.site_crawlers.mytheresa_crawler import MytheresaCrawler
except ImportError as e:
    print(f"Error importing modules: {str(e)}")
    sys.exit(1)

async def initialize():
    global config, db_manager
    config = Config()
    await config.initialize_supabase()
    db_manager = DBManager(config)

async def run_crawlers():
    await initialize()
    crawlers = [MytheresaCrawler(config)]
    for crawler in crawlers:
        try:
            results = await crawler.crawl()
            await db_manager.save_crawl_results(results)
        except Exception as e:
            print(f"Error during crawl: {str(e)}")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/cron':
            self.handle_cron()
        else:
            self.send_error(404, "Not Found")

    def handle_cron(self):
        try:
            asyncio.run(run_crawlers())
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Crawling completed")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")

    def do_POST(self):
        self.send_response(405)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Method not allowed")

def main():
    try:
        from http.server import HTTPServer
        port = int(os.environ.get('PORT', 8000))
        server_address = ('', port)
        httpd = HTTPServer(server_address, Handler)
        print(f"Server running on port {port}")
        httpd.serve_forever()
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()