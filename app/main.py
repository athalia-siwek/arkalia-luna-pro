from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Arkalia": "IA Kernel Devstation Active ✅"}


def print_status():
    from rich import print

    print("[green bold]Arkalia-LUNA is active and running.[/green bold]")
