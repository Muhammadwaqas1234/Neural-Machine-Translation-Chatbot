# 📘 Neural Machine Translation Chatbot

## Overview

This project implements a **Neural Machine Translation (NMT) system** using **Seq2Seq BiLSTM with Attention**.
It provides a **FastAPI backend** for translation and a **dynamic, professional chatbot-style frontend** for user interaction.

Users can input **English sentences** and get **French translations** in a chat interface. The system is suitable for **demonstrations,  projects, or deployment**.

---

## Features

* Seq2Seq BiLSTM with Attention architecture
* Clean chatbot-style UI for interaction
* Dynamic frontend with instant response
* FastAPI REST API backend
* GPU/CPU inference supported
* Production-ready folder structure

---

## 📁 Project Structure

```
nmt_fastapi_project/
├── backend/
│   └── app/
│       ├── main.py          # FastAPI entry point
│       ├── model.py         # Encoder, Decoder, Seq2Seq classes
│       ├── inference.py     # Translation logic
│       ├── vocab.py         # Tokenization and vocabulary
│       └── nmt_model.pth    # Pre-trained PyTorch model
│
├── frontend/
│   ├── index.html           # Chatbot UI
│   ├── script.js            # JS for API calls
│   └── style.css            # Professional styling
│
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/nmt_fastapi_project.git
cd nmt_fastapi_project/backend
```

---

### 2. Create Python virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r app/requirements.txt
```

Install tokenizers:

```bash
python -m spacy download en_core_web_sm
python -m spacy download fr_core_news_sm
```

---

### 4. Run FastAPI backend

```bash
uvicorn app.main:app --reload
```

Visit:

```
http://127.0.0.1:8000/docs
```

to see interactive API documentation.

---

### 5. Open Frontend

Open `frontend/index.html` in your browser (or use VS Code Live Server).
Type English sentences and get French translations in **chatbot style**.

---

## 🔧 How It Works

1. User inputs English text in the frontend.
2. Frontend sends request to FastAPI `/translate` endpoint.
3. Backend loads **pre-trained Seq2Seq BiLSTM model with Attention** and translates the sentence.
4. Backend returns translation JSON to frontend.
5. Frontend displays response in a professional chat bubble.

---

## 💻 Technologies Used

* **Python 3.12**
* **PyTorch** (Seq2Seq BiLSTM with Attention)
* **FastAPI** for backend REST API
* **HTML, CSS, JavaScript** for dynamic frontend
* **spaCy** for English/French tokenization

---

## 🏗 Folder Responsibilities

| Folder        | Responsibility                                       |
| ------------- | ---------------------------------------------------- |
| backend/app   | Contains API, model, vocabulary, and inference logic |
| frontend      | Chatbot-style UI and API integration                 |
| nmt_model.pth | Pre-trained PyTorch model weights                    |

---

## 🔹 Notes

* Ensure the backend is running before using the frontend.
* The chatbot UI distinguishes **user messages** (left, casual) and **model responses** (right, professional).
* GPU is optional; CPU works but may be slower.

---

## 📈 Future Improvements

* Multi-language translation
* Beam search for better translations
* BLEU score evaluation endpoint
* Deploy using Docker / AWS / Railway
* Streaming chatbot responses

---

## 📄 Author

**Muhammad Waqas**
Machine Learning & NLP Enthusiast


Do you want me to do that?
