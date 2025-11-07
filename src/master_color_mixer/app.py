# FastAPI stub for MasterColorMixer.

from fastapi import FastAPI

app = FastAPI(title="MasterColorMixer")

@app.get("/hello")
def say_hello():
    """Return a simple greeting as a JSON response."""
    return {"message": "Hello"}
