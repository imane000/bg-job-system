from fastapi import FastAPI
from rq import Queue

from app.workers.redis_conn import redis_conn
from app.jobs.tasks import slow_task

app = FastAPI()
queue = Queue("default", connection=redis_conn)

@app.get("/")
def root():
    return {"status": "Background Job System is alive"}

@app.post("/jobs")
def create_job(name: str):
    job = queue.enqueue(slow_task, name)
    return {"job_id": job.id, "status": "queued"}
