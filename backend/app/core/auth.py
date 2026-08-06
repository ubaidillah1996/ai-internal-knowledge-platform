from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from jose import jwt, JWTError

from app.core.security import (
    SECRET_KEY,
    ALGORITHM
)

from app.core.dependencies import get_db
from app.models.user import User


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials


    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        email = payload.get("sub")


        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )


        user = db.query(User).filter(
            User.email == email
        ).first()


        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )


        return user


    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )