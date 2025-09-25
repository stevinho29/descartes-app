# Descartes Underwriting – Contact Management App

This project implements a simple 3-tier application to manage contacts as part of the Descartes Underwriting technical test.

---

## 📦 Installation

### Run with Docker

```bash
# Clone repository
git clone git@github.com:<your-username>/descartes-app.git
cd descartes-app

# Start all services
docker compose up --build
```

This will start:

Frontend (React) → http://localhost:3000

Backend (FastAPI) → http://localhost:8000

PostgreSQL DB (with persistent volume)


### Run locally (without Docker)

Backend
```bash
cd server
python -m venv .venv
source .venv/bin/activate
uv sync
fastapi run app/main.py
```

Frontend
```bash
cd client
npm install
npm start
```

---

### Tests
Backend

```bash
cd server
pytest
```

Frontend
```bash
cd client
npm test
```