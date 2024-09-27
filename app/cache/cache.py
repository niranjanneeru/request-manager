import redis


class Cache:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, host='localhost', port=6379, db=0):
        if not hasattr(self, 'redis_client'):
            self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def get_client(self):
        return self.redis_client

    def set(self, key, value, ex=None):
        # Set a value in Redis
        self.redis_client.set(key, value, ex)

    def get(self, key):
        # Get a value from Redis
        return self.redis_client.get(key)

    def rpush(self, key, value):
        # Push a value to the end of a list in Redis
        self.redis_client.rpush(key, value)

    def lrange(self, key, start, end):
        # Get a range of values from a list in Redis
        return self.redis_client.lrange(key, start, end)

    def delete(self, key):
        # Delete a key from Redis
        self.redis_client.delete(key)
