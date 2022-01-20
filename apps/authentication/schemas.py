# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

from fastapi import Form
from pydantic import BaseModel

from typing import Optional

class ResponseModel(BaseModel):
    class Config:
        orm_mode = True

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



class TokenData(BaseModel):
    username: Optional[str] = None

# login and registration

# class LoginForm(FlaskForm):
#     username = StringField('Username',
#                          id='username_login',
#                          validators=[DataRequired()])
#     password = PasswordField('Password',
#                              id='pwd_login',
#                              validators=[DataRequired()])


# class CreateAccountForm(FlaskForm):
#     username = StringField('Username',
#                          id='username_create',
#                          validators=[DataRequired()])
#     email = StringField('Email',
#                       id='email_create',
#                       validators=[DataRequired(), Email()])
#     password = PasswordField('Password',
#                              id='pwd_create',
#                              validators=[DataRequired()])

