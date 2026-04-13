# app/core/security.py
import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

load_dotenv()

# 1. Fetching the secrets from .env
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

# 2. THE TOKEN GENERATOR FUNCTION (The Wristband Machine)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


# Tells FastAPI to look in the HTTP Headers for 'Authorization: Bearer <token>'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Try to open the wristband using our secret key
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        # Read the email ("sub") written inside the wristband
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token does not contain user info")
            
        return email # Return the user's email if valid
        
    except PyJWTError:
        # If the token is fake or expired
        raise HTTPException(status_code=401, detail="Could not validate credentials. Token may be expired.")