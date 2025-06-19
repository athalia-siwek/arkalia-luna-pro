from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Arkalia AssistantIA",
    description="🧠 Module d’assistance interactive — Arkalia Luna Pro",
    version="1.0.0",
)

# Middleware CORS — accepte tous les domaines (à sécuriser plus tard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🌐 Route de test GET /
@app.get("/", tags=["Système"])
def read_root():
    return JSONResponse(
        content={"message": "🤖 AssistantIA module actif — Arkalia Luna Pro."}
    )


# 🤖 Route POST /chat — placeholder pour future IA
@app.post("/chat", tags=["IA"])
async def chat(request: Request):
    try:
        data = await request.json()
        prompt = data.get("message", "").strip()

        if not prompt:
            return JSONResponse(
                status_code=400, content={"error": "Aucun message reçu."}
            )

        # Réponse temporaire à remplacer par IA réelle
        response_text = f"Tu as dit : '{prompt}' (réponse IA à coder 🎯)"
        return {"response": response_text}

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"error": f"Erreur interne : {str(e)}"}
        )
