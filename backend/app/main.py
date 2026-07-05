"""Neural Machine Translation API + chat frontend."""

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app import inference

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Neural Machine Translation API",
    description="English → French translation with a Seq2Seq BiLSTM + Attention model",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


class TranslationInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)


class TranslationOutput(BaseModel):
    translation: str
    source_lang: str = "en"
    target_lang: str = "fr"


@app.get("/health")
def health():
    available = inference.is_available()
    return {
        "status": "ok",
        "model_ready": available,
        "model_error": inference.load_error(),
    }


@app.post("/translate", response_model=TranslationOutput)
def translate_text(data: TranslationInput):
    try:
        translation = inference.translate(data.text.strip())
    except inference.TranslatorUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    return TranslationOutput(translation=translation)


# Serve the chat frontend from the same server: http://127.0.0.1:8000/
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:  # pragma: no cover

    @app.get("/", response_class=HTMLResponse)
    def missing_frontend():
        return "<h1>Frontend directory not found</h1>"
