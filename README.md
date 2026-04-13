# 🧠 Enterprise ML Backend Architecture (FastAPI + PostgreSQL + Redis)

A high-performance, production-ready REST API designed to serve Machine Learning models at scale. This project demonstrates a complete "T-Shaped" engineering skillset: Deep **ML Integration** combined with robust **Backend Architecture**, **Cloud DevOps**, and **Automated SQA**.

---

## 🚀 Live Demo & Documentation

- **Live API URL:** [https://ml-fastapi-architecture.onrender.com](https://ml-fastapi-architecture.onrender.com)
- **Interactive Swagger UI:** [https://ml-fastapi-architecture.onrender.com/docs](https://ml-fastapi-architecture.onrender.com/docs)

---

## 🛠️ Industrial Tech Stack

- **Framework:** FastAPI (Asynchronous Python)
- **Primary Database:** PostgreSQL (Neon Cloud)
- **Caching Layer:** Redis (Upstash Serverless)
- **ORM:** SQLAlchemy (Relational Mapping)
- **Security:** JWT (JSON Web Tokens) & Bcrypt Hashing
- **Task Management:** FastAPI Background Tasks (Asynchronous execution)
- **Testing:** Pytest & HTTPX (Automated SQA)
- **Containerization:** Docker (Linux-slim environment)
- **Deployment:** Render.com (CI/CD Pipeline)

---

## 🏗️ Architectural Highlights

### 1. Modular Domain-Driven Design

The project is structured into logical modules to ensure maintainability and team collaboration:

- `app/api/`: Handles request routing and HTTP logic.
- `app/core/`: Centralized security, JWT, and configuration management.
- `app/services/`: Pure business logic and ML model inference (The "Chef").
- `app/db/`: Multi-database connection management (Postgres + Redis).
- `app/models/` & `app/schemas/`: Separation of Database Tables from API JSON validation.

### 2. Performance Optimization (The Library Analogy)

To handle heavy ML loads, I implemented a **Two-Tier Caching System**:

- **Redis Caching:** Frequently requested ML inputs are cached in RAM. This bypasses the ML model entirely for repeat queries, reducing response times from ~400ms to **<30ms**.
- **Background Processing:** Long-running tasks (like email notifications or heavy AI inference) are offloaded to background threads, allowing the user to receive an instant "202 Accepted" response.

### 3. Enterprise Security

- **Password Safety:** Zero storage of plain-text passwords using `bcrypt` salting and hashing.
- **Access Control:** All ML endpoints are protected by an `OAuth2` Bearer token scheme.
- **CORS Policy:** Pre-configured for cross-origin sharing with React/Flutter frontends.

---

## 📁 Project Structure

```text
/
├── app/
│   ├── api/             # API Endpoints (Auth & ML)
│   ├── core/            # JWT Security & .env management
│   ├── db/              # Postgres & Redis Connectors
│   ├── models/          # SQLAlchemy Database Tables
│   ├── schemas/         # Pydantic JSON Validators
│   ├── services/        # ML Logic & Password Hashing
│   └── main.py          # Entry point & CORS Middleware
├── tests/               # Automated Unit Test Suite
├── Dockerfile           # Container Blueprint
├── .dockerignore
├── .gitignore
└── requirements.txt     # Dependency Locking


💻 Local Setup & Development
1. Clone & Environment

git clone https://github.com/TahfimJuwel/ML-FastAPI-Architecture
cd ML-FastAPI-Architecture
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt

2. Setup Secrets (.env)

DB_URL=postgresql://user:pass@localhost:5432/db_name
REDIS_URL=rediss://default:pass@your-redis-url
JWT_SECRET_KEY=your_secret_string
JWT_ALGORITHM=HS256

3. Running & Testing

# Run the local server
uvicorn app.main:app --reload

# Run Automated SQA Tests
pytest


🧪 API Usage Flow
Register: POST /auth/register - Create an account (Triggers Background Email).
Login: POST /auth/login - Receive a secure JWT Access Token.
Analyze: POST /analyze - (Requires Token) Analyzes sentiment. Checks Redis Cache first. If missing, runs ML model and logs to PostgreSQL.
Analyze Heavy: POST /analyze-heavy - (Requires Token) Simulates a 10-second Deep Learning task processed entirely in the background.


🚢 Docker Deployment
This project is fully containerized. To build and run the entire stack:

docker build -t ml-backend .
docker run -p 8000:8000 --env-file .env ml-backend
```
