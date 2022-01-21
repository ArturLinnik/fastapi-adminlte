# -*- encoding: utf-8 -*-

# crud.py

from ..database import get_db
from .token import SECRET_KEY, ALGORITHM, oauth2_scheme
from .schemas import TokenData
from .models import Users

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session


def get_user(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()


def get_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode the token and check if user's username is the same as the username the token is carrying
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = get_user(db, token_data.username)

    # If user doesn't exist in database rasie error 
    if user is None:
        raise credentials_exception

    return user