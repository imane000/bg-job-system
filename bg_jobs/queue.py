from rq import Queue
from bg_jobs.redis_conn import redis_conn

queue = Queue(connection=redis_conn)

def enqueue_job(func, *args, **kwargs):
    return queue.enqueue(func, *args, **kwargs)