import requests


def trigger_reflexia_check() -> None:
    try:
        response = requests.get("http://arkalia-api:8000/reflexia/check", timeout=3)
        data = response.json()
        print(f"🧠 ReflexIA check: {data}")
        return data
    except Exception as e:
        print(f"⚠️ ReflexIA unreachable: {e}")
        return None
