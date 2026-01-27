import time

def slow_task(name: str) -> dict:
    # simulate heavy work
    time.sleep(5)
    return {"message": f"Job done for {name}"}
