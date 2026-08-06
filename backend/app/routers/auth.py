from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    hashed_password = hash_password(
        user.password
    )


    new_user = User(
        email=user.email,
        password_hash=hashed_password
    )


    db.add(new_user) # Masuk ke POSTGRESQL
    db.commit()
    db.refresh(new_user)


    return new_user

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()


    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )


    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )


    token = create_access_token(
        {
            "sub": db_user.email
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }