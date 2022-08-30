# -*- encoding: utf-8 -*-

# schemas.py

from typing import Optional

from fastapi import Form
from pydantic import BaseModel


class ResponseModel(BaseModel):
    class Config:
        orm_mode = True


# --- Register ---


class CreateAccountFormRequest(BaseModel):
    username: str
    email: str
    password: str

    @classmethod
    def create_account_form(
        cls,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
    ):

        return cls(
            username=username,
            email=email,
            password=password,
        )


class CreateAccountFormResponse(ResponseModel):
    username: str
    email: str


# --- Token ---


class TokenData(BaseModel):
    username: Optional[str] = None
