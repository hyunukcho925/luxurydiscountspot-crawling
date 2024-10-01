import os
from supabase import create_client, Client
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()  # .env 파일이 있다면 로드합니다.
        self.SUPABASE_URL = os.getenv('SUPABASE_URL')
        self.SUPABASE_KEY = os.getenv('SUPABASE_KEY')
        self._supabase = None

        if not self.SUPABASE_URL or not self.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

    @property
    def supabase(self) -> Client:
        if self._supabase is None:
            try:
                self._supabase = create_client(self.SUPABASE_URL, self.SUPABASE_KEY)
            except Exception as e:
                raise ConnectionError(f"Failed to create Supabase client: {str(e)}")
        return self._supabase

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