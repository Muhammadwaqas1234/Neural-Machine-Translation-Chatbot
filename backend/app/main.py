from fastapi import FastAPI
from pydantic import BaseModel
from app.inference import translate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Neural Machine Translation API",
    description="Seq2Seq BiLSTM with Attention",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class TranslationInput(BaseModel):
    text: str


@app.post("/translate")
def translate_text(data: TranslationInput):
    translation = translate(data.text)
    return {"translation": translation}
