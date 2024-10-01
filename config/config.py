import os
from supabase import create_client, Client

class Config:
    def __init__(self):
        self.SUPABASE_URL = os.getenv('SUPABASE_URL')
        self.SUPABASE_KEY = os.getenv('SUPABASE_KEY')
        self._supabase = None

    @property
    def supabase(self) -> Client:
        if self._supabase is None:
            self._supabase = create_client(self.SUPABASE_URL, self.SUPABASE_KEY)
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