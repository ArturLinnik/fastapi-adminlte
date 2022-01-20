
from ..database import get_db
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .token import SECRET_KEY, ALGORITHM, oauth2_scheme
from .schemas import TokenData, CreateAccountFormRequest
from .models import Users
from .password import hash_pass


def get_user(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()


def get_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()


# def create_user(db: Session, user: CreateAccountFormRequest):

#     hashed_password = hash_pass(user.password)

#     db_user = Users(
#         username = user.username.lower(),
#         email = user.email.lower(),
#         password = hash_pass(hashed_password),
#         )

#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)

#     return db_user


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user