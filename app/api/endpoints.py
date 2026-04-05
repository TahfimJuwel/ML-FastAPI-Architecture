from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# import all the pieces from every file in the "app"
from app.db.database import get_db
from app.models.sentiment import SentimentLogTable
from app.schemas.sentiment import TextInput
from app.core.security import verify_api_key
from app.services.ml_service import analyze_sentiment

# APIRouter is like a "Mini FastAPI" just for this file.
router = APIRouter()

@router.post("/analyze", status_code=201)
def analyze_text(
    request_data: TextInput, 
    db: Session = Depends(get_db), 
    api_key: str = Depends(verify_api_key)
):
    # 1. Get validated text
    raw_text = request_data.text
    
    # 2. Pass to ML Service
    score, label = analyze_sentiment(raw_text)
    
    # 3. Save to Database
    db_log = SentimentLogTable(
        user_text=raw_text,
        score=score,
        sentiment_label=label
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    return {"message": "Secured Analysis Complete", "data": db_log}