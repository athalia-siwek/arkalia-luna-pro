# modules/helloria/core.py

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenue dans Helloria"}


@router.get("/status", tags=["Status"])
async def status():
    return {"status": "Helloria est opérationnel"}


app = FastAPI()
app.include_router(router)


@app.post("/echo", tags=["Test"])
async def echo(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "").strip()

        if not message:
            return JSONResponse(status_code=400, content={"error": "Message vide."})

        return {"echo": message}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Erreur : {str(e)}"})
