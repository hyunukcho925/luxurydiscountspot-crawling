from .mytheresa_crawler import MytheresaCrawler
# 다른 사이트 크롤러들도 여기에 import

def get_all_crawlers(config):
    return [
        MytheresaCrawler(config),
        # 다른 사이트 크롤러 인스턴스들도 여기에 추가
    ]