from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
import json
import os
import uuid

load_dotenv()

app = FastAPI()

class SessionWithTimeout(requests.Session):
    def __init__(self, timeout=5):
        super().__init__()
        self.timeout = timeout

    def request(self, method, url, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        return super().request(method, url, **kwargs)

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

@app.post("/busqueda")
def download_news_from(topic: str):
    try:
        news_key = os.getenv("NEWS_API_KEY")

        s = SessionWithTimeout()
        s.mount('https://', adapter)
        s.mount('http://', adapter)

        payload = {'User-Agent':'ai-automation-portfolio/1.0'}
        s.headers.update(payload)

        payload = {'language':'en', 'apiKey':news_key, "q": topic}
        r = s.get("https://newsapi.org/v2/top-headlines", params=payload)
        r.raise_for_status()
        newsList = r.json()

        if newsList['status'] == 'ok':
                if newsList['totalResults'] == 0:
                    return('WARNING: No hay ningún resultado')
                else:
                    for n in newsList["articles"]: n['id'] = str(uuid.uuid4())
                    with open("news.json", "w") as f:
                        json.dump(newsList["articles"], f, indent=4)
                    return(f"Se han obtenido {newsList['totalResults']} resultados")

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Error de conexión")
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Timeout")
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Error HTTP: {e}")

@app.get("/")
def read_root():
    return {"status":"ok", "message":"API funcionando"}

@app.get("/noticias")
def read_news(source: str | None = None):
    with open("news.json", "r") as f:
        news = json.load(f)
    if source:
        return [n for n in news if n.get('source',{}).get('name') == source]
    return news

@app.get("/noticias/{id}")
def read_news_by_id(id: str):
    with open("news.json", "r") as f:
        news = json.load(f)
    result = [n for n in news if n.get("id") == id]
    if not result:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    return result[0]

@app.delete("/noticias/{id}")
def delete_news_by_id(id: str):
    with open("news.json", "r") as f:
        news = json.load(f)

    if isinstance(news, list):
        news = [n for n in news if n.get("id") != id]

    with open("news.json", "w") as f:
        json.dump(news, f, indent=4)

    return {f"La noticia con el id {id} se ha borrado"}