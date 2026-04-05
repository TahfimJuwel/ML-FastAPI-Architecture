from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints, auth_routes
from app.db.database import engine, Base
from app.models.user import UserTable
from app.models.sentiment import SentimentLogTable

# Create tables in Postgres if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ML Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the "Waiters" to the main restaurant
app.include_router(endpoints.router)
app.include_router(auth_routes.router)