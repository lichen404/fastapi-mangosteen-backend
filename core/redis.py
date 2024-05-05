import os
import redis

environment = os.getenv("ENVIRONMENT", "development")

def get_redis():
    return redis.from_url(environment == 'production' and 'redis://my-redis-container' or 'redis://localhost')


