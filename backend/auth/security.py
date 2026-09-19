# Provides password validation, hashing, JWT creation, and user authentication.
from datetime import datetime, timedelta

import bcrypt
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database.connection import get_db, settings
from backend.database.models import User

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/login"
)

#hashed password will be stored in db
def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(password: str,password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"),password_hash.encode("utf-8")
    )

def validate_username(username: str) -> bool:

    #TODO:instead of boolean return we can return the exact not matching false type

    if len(username) < 5:
        return False

    if not username.isalpha():
        return False

    # Require both upper and lower case
    if not any(char.isupper() for char in username):
        return False

    if not any(char.islower() for char in username):
        return False

    return True

def validate_password(password: str) -> bool:

    if len(password) < 5:
        return False

    has_alpha = any(
        char.isalpha()
        for char in password
    )

    has_number = any(
        char.isdigit()
        for char in password
    )

    has_special = any(
        char in "$%*)"
        for char in password
    )

    return (
        has_alpha
        and has_number
        and has_special
    )

#JWT token creation
def create_access_token(user_id: int,username: str,role: str):

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )

#for the current logged user
def get_current_user( token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials")

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except Exception:
        raise credentials_exception

    user = (db.query(User).filter(User.id == int(user_id)).first())

    if user is None:
        raise credentials_exception

    return user

def require_admin(current_user: User = Depends(get_current_user)):

    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user