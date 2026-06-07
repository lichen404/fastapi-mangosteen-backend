import os
import redis.asyncio as aioredis

environment = os.getenv("ENVIRONMENT", "development")

def get_redis():
    url = 'redis://my-redis-container' if environment == 'production' else 'redis://localhost'
    return aioredis.from_url(url)


