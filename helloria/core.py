from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Arkalia-LUNA API active"}


@app.get("/status")
def status():
    return {
        "status": "ok",
        "version": "1.0.6",
        "modules_loaded": ["reflexia", "nyxalia", "helloria"],
    }
