# 🧠 Machine Learning Backend Architecture (FastAPI + PostgreSQL)

An enterprise-grade REST API designed to bridge the gap between Machine Learning models and Web/Mobile Applications. Built with **FastAPI** and **PostgreSQL**, featuring secure API key authentication, ORM database logging, and automated CORS handling.

## 🚀 Features

- **⚡ High-Performance Framework:** Built with FastAPI, utilizing asynchronous architecture for maximum speed.
- **🤖 ML Integration:** Seamlessly receives raw text, validates it via Pydantic, and feeds it into an NLP model (TextBlob).
- **🗄️ Relational Database Logging:** Utilizes SQLAlchemy (ORM) to permanently log user inputs and ML predictions into a local PostgreSQL database.
- **🔐 API Security:** Protected by Header-based API Key Authentication to prevent unauthorized access and resource exhaustion.
- **🌐 Web Ready:** Pre-configured with CORS Middleware to allow secure cross-origin requests from React/Vue/Angular frontends.
- **🛡️ Secrets Management:** Environment variables (`.env`) used to keep database URIs and API keys completely hidden from source control.

## 🏗️ Architecture Flow

1.  **Client Request:** Frontend sends a POST request with a JSON payload.
2.  **Security Check:** The Dependency Injector checks the HTTP Headers for a valid `x-api-key`. (Rejects with `401 Unauthorized` if invalid).
3.  **Data Validation:** Pydantic validates the JSON payload to ensure strict data types.
4.  **ML Processing:** The NLP model analyzes the text and calculates a sentiment polarity score.
5.  **Database Transaction:** SQLAlchemy opens a secure session, logs the original text, score, and label into PostgreSQL, and closes the session.
6.  **Response:** The client receives a clean `201 Created` JSON response.

## 💻 Local Setup & Installation

Follow these steps to run this architecture on your local machine.

### 1. Prerequisites

- Python 3.8+
- PostgreSQL installed and running locally on port `5432`

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/ML-FastAPI-Architecture.git
cd ML-FastAPI-Architecture
```
