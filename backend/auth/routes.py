# Provides API endpoints for user registration and login.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import User

from .security import hash_password,verify_password,validate_username,validate_password,create_access_token

router = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)

# handles the username and password schema on register
@router.post("/register")
def register(
    username: str,
    password: str,
    role: str = "PLAYER",
    db: Session = Depends(get_db)
):

    role = role.upper()

    if role not in {"PLAYER", "ADMIN"}:
        raise HTTPException(
            status_code=400,
            detail="Role must be PLAYER or ADMIN."
        )

    if not validate_username(username):
        raise HTTPException(
            status_code=400,
            detail=(
                "Username must contain at least 5 letters "
                "and include uppercase and lowercase letters."
            )
        )

    if not validate_password(password):
        raise HTTPException(
            status_code=400,
            detail=(
                "Password must be at least 5 characters "
                "and contain letters, numbers and "
                "$, %, *, or )."
            )
        )

    existing_user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    user = User(
        username=username,
        password_hash=hash_password(password),
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration successful",
        "username": user.username
    }


@router.post("/login")
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        user.id,
        user.username,
        user.role
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role
    }

