# backend/services/auth.py

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

# --- SIMPLIFIED USER DATABASE ---
# We now store the plain text password directly.
FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "password": "adminpass",  # Plain text password
        "role": "admin"
    },
    "user": {
        "username": "user",
        "password": "userpass",    # Plain text password
        "role": "user"
    }
}

# This function remains the same, it just gets the user data.
def get_user(db, username: str):
    if username in db:
        return db[username]
    return None

# This function is for creating the JWT after a successful login. It remains the same.
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# This function checks the JWT on subsequent requests. It remains the same.
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(FAKE_USERS_DB, username)
    if user is None:
        raise credentials_exception
    return user

# This function checks the user's role from the JWT. It remains the same.
def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user