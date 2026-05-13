from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from pydantic import BaseModel
import bcrypt
import os
from dotenv import load_dotenv


load_dotenv()
PEPPER = os.getenv("PEPPER")


engine = create_engine("sqlite:///usuarios.db")


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str


class Credenciales(BaseModel):
    username: str
    password: str


SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.post("/register")
def register(credenciales: Credenciales):
  
    password_con_pepper = credenciales.password + PEPPER
   
    hashed = bcrypt.hashpw(password_con_pepper.encode("utf-8"), bcrypt.gensalt())
  
    usuario = Usuario(username=credenciales.username, hashed_password=hashed.decode("utf-8"))
    with Session(engine) as session:
        session.add(usuario)
        session.commit()
    return {"mensaje": "Usuario registrado correctamente"}

@app.post("/login")
def login(credenciales: Credenciales):
   
    with Session(engine) as session:
        usuario = session.exec(select(Usuario).where(Usuario.username == credenciales.username)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
   
    password_con_pepper = credenciales.password + PEPPER
    valido = bcrypt.checkpw(password_con_pepper.encode("utf-8"), usuario.hashed_password.encode("utf-8"))
    if not valido:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    return {"mensaje": "Login exitoso"}
