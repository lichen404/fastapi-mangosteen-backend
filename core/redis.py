import redis


def get_redis():
    return redis.from_url('redis://localhost')


