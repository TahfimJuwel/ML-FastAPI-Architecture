# 🧠 Enterprise ML Backend Architecture (FastAPI + PostgreSQL)

A production-ready REST API bridging Machine Learning models with Front-End applications. Engineered with **FastAPI** and **PostgreSQL**, this project demonstrates Senior-level backend architecture including JWT Authentication, Asynchronous Background Tasks, Test-Driven Development (TDD), and Modular Domain-Driven Design.

## 🚀 Enterprise Features

- **🔐 JWT Authentication:** Secure User Registration and Login flow with Bcrypt password hashing and Bearer token route protection.
- **🏗️ Modular Architecture:** Codebase structured for scalability, separating Routers, Services (Business Logic), Schemas (Validation), and Models (Database).
- **⚡ Asynchronous Background Tasks:** Heavy ML processing and simulated I/O tasks are offloaded to background threads to prevent API blocking, ensuring sub-millisecond response times.
- **🤖 ML Integration:** Seamlessly feeds validated JSON payloads into NLP models (TextBlob) and translates mathematical polarities into business-friendly labels.
- **🗄️ Relational Database (ORM):** Utilizes SQLAlchemy to map users to their specific ML predictions using Foreign Keys in a local PostgreSQL database.
- **🧪 Automated SQA Testing:** Complete Unit Test coverage using `pytest` and `httpx` to automatically verify authentication and endpoint integrity.

## 📁 Industrial Folder Structure

````text
/
├── app/
│   ├── api/             # API Routers & Endpoints
│   ├── core/            # Security, JWT, config, and Bouncer logic
│   ├── db/              # Database engine and session manager
│   ├── models/          # SQLAlchemy Database Schemas (Postgres Tables)
│   ├── schemas/         # Pydantic Models for JSON validation
│   ├── services/        # ML logic, Password Hashing, Background Tasks
│   └── main.py          # Application entry point & CORS configuration
├── tests/               # Pytest automated test suites
├── .env                 # Environment variables (Ignored by Git)
├── .gitignore
└── requirements.txt     # Dependency locking


💻 Local Setup & Installation
1. Prerequisites
Python 3.8+
PostgreSQL running locally on port 5432
2. Clone & Environment Setup

```text
git clone https://github.com/YOUR_GITHUB_USERNAME/ML-FastAPI-Architecture.git
cd ML-FastAPI-Architecture
python -m venv venv

# Activate the venv (Windows):
venv\Scripts\activate

# Install Dependencies:
pip install -r requirements.txt
3. Environment Variables
Create a .env file in the root directory:

Env
DB_URL=postgresql://postgres:admin123@localhost:5432/ml_backend_db
JWT_SECRET_KEY=your_secure_random_string
JWT_ALGORITHM=HS256
4. Run the Application


# Start the server
uvicorn app.main:app --reload

# Run Automated SQA Tests
pytest
🧪 API Flow Overview
POST /auth/register: Creates user, hashes password, triggers background welcome email.
POST /auth/login: Verifies hash, returns short-lived JWT Bearer Token.
POST /analyze: (Requires JWT) Validates text, runs ML model, permanently logs result to DB with Foreign Key to user.
POST /analyze-heavy: Triggers Asynchronous ML processing in the background, instantly returning a 202 Accepted status.
````
