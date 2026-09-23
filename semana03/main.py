from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date

app = FastAPI()

class Contact(BaseModel):
    name: str
    email: str
    message: str
    init_date: date

contacts_db = []

@app.get("/")
def read_root():
    return {"status":"ok", "message":"API funcionando" }

@app.get("/greeting/{name}")
def read_name(name: str):
    return {"saludo": f"Hola, {name}"}

@app.post("/contact/")
def create_item(item: Contact):
    if "@" in item.email:
        contacts_db.append(item.dict())
        return{"recibido": True, "name": item.name}
    else:
        raise HTTPException(status_code=400, detail="Email no encontrado")

@app.get("/contacts/")
def get_contacts(date: date | None = None):
    if date:
        return [c for c in contacts_db if c["init_date"] == date]
    return contacts_db
