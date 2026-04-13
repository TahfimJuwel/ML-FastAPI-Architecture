from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import UserTable
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import get_password_hash, verify_password
from app.core.security import create_access_token
from app.services.email_service import send_welcome_email 


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
def register_user(user_data: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

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

    background_tasks.add_task(send_welcome_email, new_user.email)

    return {"message": "User registered successfully", "user_id": new_user.id, "email": new_user.email}


@router.post("/login", status_code=200)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    
    # Check if the email exists in the database
    user = db.query(UserTable).filter(UserTable.email == user_data.email).first()
    
    # If the user is None, it means the email isn't in our system
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Email or Password")

    # Check if the password matches
    # user.hashed_password is the scrambled password from Postgres
    # user_data.password is the normal password they just typed in Postman
    is_password_correct = verify_password(user_data.password, user.hashed_password)
    
    if not is_password_correct:
        raise HTTPException(status_code=401, detail="Invalid Email or Password")

    # Create the JWT Token
    jwt_token = create_access_token(data={"sub": user.email})

    # Give the token to the user
    # "bearer" is the industry-standard word meaning "The person bearing (holding) this token is allowed in."
    return {"access_token": jwt_token, "token_type": "bearer"}