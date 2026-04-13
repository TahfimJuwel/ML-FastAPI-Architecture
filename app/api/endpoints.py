from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

# import all the pieces from every file in the "app"
from app.db.database import get_db
from app.models.sentiment import SentimentLogTable
from app.schemas.sentiment import TextInput
# from app.core.security import verify_api_key
from app.core.security import get_current_user 
from app.services.ml_service import analyze_sentiment, run_heavy_ml_in_background
from app.models.user import UserTable

# APIRouter is like a "Mini FastAPI" just for this file.
router = APIRouter()

@router.post("/analyze", status_code=201)
def analyze_text(
    request_data: TextInput, 
    db: Session = Depends(get_db), 
    # api_key: str = Depends(verify_api_key)
    current_user_email: str = Depends(get_current_user) 
):
    
    # Find the actual User in the database using the email from the Token
    user = db.query(UserTable).filter(UserTable.email == current_user_email).first()


    # 1. Get validated text
    raw_text = request_data.text
    
    # 2. Pass to ML Service
    score, label = analyze_sentiment(raw_text)
    
    # 3. Save to Database
    db_log = SentimentLogTable(
        user_text=raw_text,
        score=score,
        sentiment_label=label,
        user_id=user.id  # Associate log with the User's ID
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    return {
        "message": f"Analysis complete and linked to user for user: {current_user_email}", 
        "data": db_log
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