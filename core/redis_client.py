import os
import redis

class RedisSettings:
    def __init__(self):
        self.REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
        self.REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
        self.REDIS_DB = int(os.getenv('REDIS_DB', 0))

class RedisClient:
    _instance = None

    def __new__(cls, settings: RedisSettings):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance._initialize(settings)
        return cls._instance

    def _initialize(self, settings: RedisSettings):
        self.client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

redis_settings = RedisSettings()
redis_client = RedisClient(redis_settings).client
