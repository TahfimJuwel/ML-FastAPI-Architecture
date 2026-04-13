from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
import os
# import all the pieces from every file in the "app"
from app.db.database import get_db
from app.models.sentiment import SentimentLogTable
from app.schemas.sentiment import TextInput
# from app.core.security import verify_api_key
from app.core.security import get_current_user 
from app.services.ml_service import analyze_sentiment, run_heavy_ml_in_background
from app.models.user import UserTable
import redis
import json

# APIRouter is like a "Mini FastAPI" just for this file.
router = APIRouter()

# Connect to Redis
redis_client = redis.from_url(os.getenv("REDIS_URL"))

@router.post("/analyze", status_code=201)
def analyze_text(
    request_data: TextInput, 
    db: Session = Depends(get_db), 
    # api_key: str = Depends(verify_api_key)
    current_user_email: str = Depends(get_current_user) 
):

    # 1. Get validated text
    raw_text = request_data.text

    # CHECK THE STICKYNOTE
    cached_result = redis_client.get(raw_text)
    
    if cached_result:
        print("⚡ [CACHE HIT] Found the answer on the sticky note!")
        # Redis stores data as a string, so we convert it back to a Python dictionary
        result_dict = json.loads(cached_result)
        return {"message": "Instant Cache Response!", "data": result_dict}
        
    print("🐢 [CACHE MISS] Not found. Waking up the ML model...")

    # DO THE HEAVY WORK (If not found)
    # Find the actual User in the database using the email from the Token
    user = db.query(UserTable).filter(UserTable.email == current_user_email).first()

    
    # Pass to ML Service
    score, label = analyze_sentiment(raw_text)
    
    # Save to Database
    db_log = SentimentLogTable(
        user_text=raw_text,
        score=score,
        sentiment_label=label,
        user_id=user.id  # Associate log with the User's ID
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    # Create the result we want to save
    final_result = {
        "text": raw_text,
        "score": score,
        "label": label
    }
    
    # Save the result to Redis
    redis_client.setex(raw_text, 3600, json.dumps(final_result))  # Cache for 1 hour

    return {
        "message": f"Analysis complete, saved to cache and linked to user for user: {current_user_email}", 
        "data": final_result
    }

@router.post("/analyze-heavy", status_code=202)
def analyze_heavy_text(
    request_data: TextInput, 
    background_tasks: BackgroundTasks,
    current_user_email: str = Depends(get_current_user) 
):
    
    background_tasks.add_task(run_heavy_ml_in_background, request_data.text, current_user_email)
    
    # Return an INSTANT response to the user
    return {
        "message": "We have received your massive dataset. The AI is processing it in the background. We will email you when it finishes!",
        "status": "Processing..."
    }
