import os
from dotenv import load_dotenv
from supabase import create_client, Client

class Config:
    def __init__(self):
        load_dotenv()
        self.SUPABASE_URL = os.getenv('SUPABASE_URL')
        self.SUPABASE_KEY = os.getenv('SUPABASE_KEY')
        self.supabase = self.initialize_supabase()

    def initialize_supabase(self) -> Client:
        if not self.SUPABASE_URL or not self.SUPABASE_KEY:
            raise ValueError("Supabase URL and key must be set in the .env file")
        return create_client(self.SUPABASE_URL, self.SUPABASE_KEY)

    def __str__(self):
        return f"Config(SUPABASE_URL={self.SUPABASE_URL}, SUPABASE_KEY={'*' * len(self.SUPABASE_KEY)})"

    def get_site_config(self, site_name):
        configs = {
            '마이테레사': {
                'url': 'https://www.mytheresa.com',
                'selector': '.pricing__prices__price'
            },
            # 다른 사이트 설정들...
        }
        return configs.get(site_name, {})