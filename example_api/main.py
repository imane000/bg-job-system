from fastapi import FastAPI, HTTPException
from rq.job import Job

from bg_jobs import enqueue_job
from bg_jobs.redis_conn import redis_conn
from bg_jobs.tasks import slow_task

app = FastAPI()


@app.get("/")
def root():
    return {"status": "Background Job System is alive"}


@app.post("/jobs")
def create_job(name: str):
    job = enqueue_job(slow_task, name)
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