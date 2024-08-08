import redis

# Redis 설정
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Redis 클라이언트 초기화
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

try:
    redis_client.ping()
    print("Connected to Redis!")
except redis.ConnectionError:
    print("Failed to connect to Redis.")