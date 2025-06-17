from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Arkalia": "IA Kernel Devstation Active ✅"}