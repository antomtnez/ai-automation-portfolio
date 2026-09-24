from fastapi import FastAPI, Request, HTTPException
from datetime import datetime
import hmac
import hashlib
import json

app = FastAPI()

SECRET = "mi_secreto_compartido"

@app.post("/webhook")
async def receive_webhook(request: Request):
    payload_bytes = await request.body()
    firma_recibida = request.headers.get("X-Signature")
    
    firma_esperada = hmac.new(
        SECRET.encode(),
        payload_bytes,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(firma_recibida or "", firma_esperada):
        raise HTTPException(status_code=401, detail="Firma inválida")
    
    payload = json.loads(payload_bytes)
    print(f"[{datetime.now()}] Webhook verificado: {payload}")
    return {"recibido": True}