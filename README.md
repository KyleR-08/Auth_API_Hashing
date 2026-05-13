# Auth API Hashing

API de autenticación segura con FastAPI, SQLModel, bcrypt y pepper.

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar: `venv\Scripts\activate`
4. Instalar dependencias: `pip install fastapi uvicorn sqlmodel bcrypt python-dotenv`
5. Crear archivo `.env` con: `PEPPER=tuValorSecreto`

## Correr el servidor

```bash
fastapi dev main.py
```

## Endpoints

- `POST /register` — Registra un usuario
- `POST /login` — Autentica un usuario
