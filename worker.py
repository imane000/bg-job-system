from rq import Worker
from bg_jobs.redis_conn import redis_conn

if __name__ == "__main__":
    worker = Worker(["default"], connection=redis_conn)
    worker.work()