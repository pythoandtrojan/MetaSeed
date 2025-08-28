import diskcache as dc
from pathlib import Path

class ExploitCache:
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache = dc.Cache(str(self.cache_dir))
        
    def get_exploit(self, exploit_id):
        return self.cache.get(exploit_id)
        
    def store_exploit(self, exploit_id, data, expire=3600):
        self.cache.set(exploit_id, data, expire)
        
    def get_api_data(self, api_name, query):
        cache_key = f"{api_name}_{query}"
        return self.cache.get(cache_key)
        
    def store_api_data(self, api_name, query, data, expire=86400):
        cache_key = f"{api_name}_{query}"
        self.cache.set(cache_key, data, expire)
        
    def clear_cache(self):
        self.cache.clear()
        return True
