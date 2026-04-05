from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import UserTable
from app.schemas.user import UserCreate
from app.services.auth_service import get_password_hash

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(UserTable).filter(UserTable.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = get_password_hash(user_data.password)

    new_user = UserTable(
        email=user_data.email,
        hashed_password=hashed_pwd
    )

    db.add(new_user)
    db.commit() 
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id, "email": new_user.email}