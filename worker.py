from rq import SimpleWorker, Queue
from app.workers.redis_conn import redis_conn

if __name__ == "__main__":
    queue = Queue("default", connection=redis_conn)
    worker = SimpleWorker([queue], connection=redis_conn)
    worker.work()