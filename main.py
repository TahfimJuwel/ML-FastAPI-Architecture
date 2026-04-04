from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, DBModel, SentimentAnalysis 
from textblob import TextBlob
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # replace "*" with the actual frontend URL (e.g., ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, POST, PUT, DELETE
    allow_headers=["*"], # Allows custom x-api-key header
)

class TextInput(BaseModel):
    text: str

def get_db():
    db = SessionLocal() # Open the connection
    try:
        yield db        # "Yield" means pause here, hand the connection to the API endpoint, and wait until the endpoint finishes.
    finally:
        db.close()      # Once the API is done sending the response to the user, CLOSE the connection to free up RAM.

SECRET_API_KEY = os.getenv("API_SECRET_KEY")

def verify_api_key(api_key: str = Header(None)):
    if api_key != SECRET_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

@app.post("/analyze", status_code=201)
def create_model(model: TextInput, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    raw_text = model.text
    blob = TextBlob(raw_text)
    polarity_score = blob.sentiment.polarity

    if polarity_score > 0:
        final_label = "Positive"
    elif polarity_score < 0:
        final_label = "Negative"
    else:
        final_label = "Neutral"

    db_log = SentimentAnalysis(
        user_text=raw_text,
        score=polarity_score,
        sentiment_label=final_label
    )

    # 2. Add to Session Workspace
    db.add(db_log)
    # 3. Permanently save it
    db.commit()
    # 4. Refresh to get the auto-generated ID
    db.refresh(db_log)
    
    return {"message": "Analysis complete", "data": db_log}
