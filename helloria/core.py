# /Volumes/T7/devstation/cursor/arkalia-luna-pro/helloria/core.py

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Bienvenue dans Arkalia-LUNA 🧠"}
