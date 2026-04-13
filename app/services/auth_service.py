import bcrypt

# 1. Function to scramble the password
def get_password_hash(password: str) -> str:
    # Convert the normal string into "bytes"
    pwd_bytes = password.encode('utf-8')
    
    # Generate a "Salt"
    salt = bcrypt.gensalt()
    
    # Hash the password with the salt
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    
    # Convert the bytes back to a normal string so can save it in Postgres
    return hashed_bytes.decode('utf-8')

# Function to check the login password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convert both passwords into bytes
    plain_pwd_bytes = plain_password.encode('utf-8')
    hashed_pwd_bytes = hashed_password.encode('utf-8')
    
    # Let bcrypt check if they match!
    return bcrypt.checkpw(plain_pwd_bytes, hashed_pwd_bytes)