import os

from core import app

if __name__ == "__main__":
    import uvicorn

    host = "0.0.0.0" if os.getenv("ENV") == "prod" else "127.0.0.1"  # nosec@main.py
    uvicorn.run(app, host=host, port=8000)
