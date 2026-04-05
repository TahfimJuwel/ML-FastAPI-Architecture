from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 1. Function to scramble the password before saving to DB
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 2. Function to check if a login password matches the scrambled DB password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)