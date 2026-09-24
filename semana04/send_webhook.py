import hmac
import hashlib
import requests
import json

SECRET = "mi_secreto_compartido"
URL = "https://emblem-expenses-word.ngrok-free.dev/webhook"

payload = {"evento": "pago", "cantidad": 50, "usuario": "Antonio"}
payload_bytes = json.dumps(payload).encode()

firma = hmac.new(
    SECRET.encode(),
    payload_bytes,
    hashlib.sha256
).hexdigest()

r = requests.post(
    URL,
    data=payload_bytes,
    headers={
        "Content-Type": "application/json",
        "X-Signature": firma
    }
)

print(f"Status: {r.status_code}")
print(f"Respuesta: {r.json()}")