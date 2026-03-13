# FastAPI Background Job System

A lightweight background job processing system built with **FastAPI**, **Redis**, **RQ**, and **Docker**.

This project allows you to enqueue long-running tasks through an API, process them asynchronously using a worker, and retrieve the result later using a job ID.

---

## Features

- Submit background jobs through a FastAPI API
- Process jobs asynchronously using an RQ worker
- Track job status and results
- Redis-backed job queue
- Dockerized setup for easy startup
- Modular architecture with reusable `bg_jobs` package

---

## Architecture

```mermaid
flowchart LR
  U[Client / Browser / curl] -->|POST /jobs| API[FastAPI API]
  API -->|enqueue job| Q[RQ Queue]
  Q --> R[(Redis)]
  W[Worker] -->|pull job| R
  W -->|execute task| T[slow_task]
  W -->|store result| R
  API -->|GET /jobs/{id}| R
```

---

## Project Structure

```
bg-job-system/
├── bg_jobs/              # reusable background job engine
│   ├── __init__.py
│   ├── queue.py
│   ├── redis_conn.py
│   └── tasks.py
│
├── example_api/          # demo FastAPI integration
│   └── main.py
│
├── worker.py             # RQ worker entry point
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Quick Start (Recommended)

### 1. Clone the repository

```bash
git clone https://github.com/imane000/bg-job-system.git
cd bg-job-system
```

### 2. Start the system with Docker

```bash
docker compose up --build
```

This command starts:

- Redis
- FastAPI API
- Worker

### 3. Open the API documentation

Open your browser and go to:

```
http://127.0.0.1:8000/docs
```

You can now interact with the API through the Swagger interface.

---

## Usage

### Create a job

Using Swagger or curl:

```bash
curl -X POST "http://127.0.0.1:8000/jobs?name=Imane"
```

Example response:

```json
{
  "job_id": "example-job-id",
  "status": "queued"
}
```

---

### Check job status

```bash
curl "http://127.0.0.1:8000/jobs/<JOB_ID>"
```

Example response:

```json
{
  "job_id": "example-job-id",
  "status": "finished",
  "result": {
    "message": "Job done for Imane"
  },
  "created_at": "...",
  "ended_at": "...",
  "exc_info": null
}
```

---

## Using the `bg_jobs` package

The `bg_jobs` module provides a simple interface for enqueueing background tasks.

Example:

```python
from bg_jobs import enqueue_job
from bg_jobs.tasks import slow_task

job = enqueue_job(slow_task, "Imane")
print(job.id)
```

---

## Tech Stack

- Python
- FastAPI
- Redis
- RQ (Redis Queue)
- Docker

---

## Notes

- Jobs are processed asynchronously by a background worker.
- Redis stores the queue and job results.
- The `example_api` folder demonstrates how to integrate the `bg_jobs` package with FastAPI.

---

## Future Improvements

- Add more real-world task examples
- Add request validation with Pydantic
- Add environment variable configuration
- Add automated tests
- Package `bg_jobs` as an installable Python module