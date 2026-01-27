from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Background Job System is alive"}
