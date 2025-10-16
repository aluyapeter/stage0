# Backend Wizards Stage 0 — Profile API (FastAPI)

## 📋 Task Summary
This is my HNG Stage 0 backend task. The goal was to build a `/me` endpoint returning:
- My profile info (email, name, stack)
- A random cat fact from [Cat Facts API](https://catfact.ninja/fact)
- A current UTC timestamp in ISO 8601 format

---

## ⚙️ Tech Stack
- Python 3.11
- FastAPI
- HTTPX (for async HTTP calls)
- Pydantic v2 + pydantic-settings (for env management)
- Slowapi (for rate limiting)

---

## 🚀 Running Locally

### 1️⃣ Clone and Install
```
git clone https://github.com/aluyapeter/stage0.git
cd stage0
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# 2️⃣ Start the server
```
uvicorn app.main:app --reload
```
Visit: http://127.0.0.1:8000/me

# ✅ Tests
Run:
```
pytest
```
