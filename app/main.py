from fastapi import FastAPI, HTTPException
from rq import Queue
from rq.job import Job

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
    return {
        "job_id": job.id,
        "status": "queued"
    }

@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job.id,
        "status": job.get_status(),
        "result": job.result,
        "created_at": job.created_at,
        "ended_at": job.ended_at,
        "exc_info": job.exc_info
    }
