import redis.asyncio as aioredis
from rq import Queue

from redis import Redis

from settings import config

redis_instance = Redis.from_url(config.REDIS_URL)

summarize_queue = Queue("summarization", connection=redis_instance)