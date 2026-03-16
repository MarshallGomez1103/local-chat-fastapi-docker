from __future__ import annotations

import os
import datetime
from pathlib import Path
from typing import Dict, List, Any

from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI

from .database import get_session, ChatLog, init_db


MODEL_BASE_URL = os.getenv("MODEL_BASE_URL", "http://host.docker.internal:1234/v1")
MODEL_API_KEY = os.getenv("MODEL_API_KEY", "lm-studio")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-20b")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


def create_client(base_url: str, api_key: str) -> OpenAI:
    return OpenAI(base_url=base_url, api_key=api_key)


client = create_client(MODEL_BASE_URL, MODEL_API_KEY)

init_db()

app = FastAPI(title="Local Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "model_base_url": MODEL_BASE_URL,
        "model_name": MODEL_NAME,
        "time": datetime.datetime.utcnow().isoformat()
    }


@app.get("/api/chat")
async def chat(message: str = Query(..., description="Mensaje del usuario")) -> Dict[str, Any]:
    if not message.strip():
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message},
    ]

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
        )
        answer = completion.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando el modelo local: {str(e)}")

    timestamp = datetime.datetime.utcnow().isoformat()

    with get_session() as db:
        db_log = ChatLog(question=message, answer=answer)
        db.add(db_log)
        db.commit()

    return {
        "question": message,
        "answer": answer,
        "timestamp": timestamp,
    }


@app.get("/api/history")
async def history(limit: int = 50) -> List[Dict[str, Any]]:
    with get_session() as db:
        records = db.query(ChatLog).order_by(ChatLog.id.desc()).limit(limit).all()
        return [
            {
                "id": rec.id,
                "question": rec.question,
                "answer": rec.answer,
                "timestamp": rec.timestamp.isoformat(),
            }
            for rec in records
        ]


@app.get("/api/config")
async def update_config(
    base_url: str | None = None,
    api_key: str | None = None,
    model_name: str | None = None,
) -> Dict[str, Any]:
    global MODEL_BASE_URL, MODEL_API_KEY, MODEL_NAME, client

    if base_url:
        MODEL_BASE_URL = base_url
    if api_key:
        MODEL_API_KEY = api_key
    if model_name:
        MODEL_NAME = model_name

    client = create_client(MODEL_BASE_URL, MODEL_API_KEY)

    return {
        "base_url": MODEL_BASE_URL,
        "api_key": MODEL_API_KEY,
        "model_name": MODEL_NAME,
    }