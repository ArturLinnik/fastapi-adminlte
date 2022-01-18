# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# from urllib import response
# from flask import render_template, redirect, request, url_for
# from flask_login import (
#     current_user,
#     login_user,
#     logout_user
# )

# from apps import db, login_manager
# from apps.authentication import blueprint
# from apps.authentication.forms import LoginForm, CreateAccountForm
# from apps.authentication.models import Users

# from apps.authentication.util import verify_pass


# @blueprint.route('/')
# def route_default():
#     return redirect(url_for('authentication_blueprint.login'))


#####################
from copy import deepcopy
from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from .forms import CreateAccountFormRequest, CreateAccountFormResponse
from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .models import Users
#####################



router = APIRouter()

templates = Jinja2Templates(directory="apps/templates")

@router.get("/")
async def route_default(response: Response):
    response = RedirectResponse(url="/login")
    return response

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("accounts/register.html", {"request": request})

@router.post("/register", response_model=CreateAccountFormResponse)
async def create_user(form_data: CreateAccountFormRequest = Depends(CreateAccountFormRequest.create_account_form), db: Session = Depends(get_db)):
    # db_user = get_user_by_email(db, email=form_data.email)

    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")

    db_user = Users(
        username = form_data.username,
        email = form_data.email,
        password = form_data.password,
        )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("accounts/login.html", {"request": request})






# Login & Registration

# @blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     login_form = LoginForm(request.form)
#     if 'login' in request.form:

#         # read form data
#         username = request.form['username']
#         password = request.form['password']

#         # Locate user
#         user = Users.query.filter_by(username=username).first()

#         # Check the password
#         if user and verify_pass(password, user.password):

#             login_user(user)
#             return redirect(url_for('authentication_blueprint.route_default'))

#         # Something (user or pass) is not ok
#         return render_template('accounts/login.html',
#                                msg='Wrong user or password',
#                                form=login_form)

#     if not current_user.is_authenticated:
#         return render_template('accounts/login.html',
#                                form=login_form)
#     return redirect(url_for('home_blueprint.index'))


# @blueprint.route('/register', methods=['GET', 'POST'])
# def register():
#     create_account_form = CreateAccountForm(request.form)
#     if 'register' in request.form:

#         username = request.form['username']
#         email = request.form['email']

#         # Check usename exists
#         user = Users.query.filter_by(username=username).first()
#         if user:
#             return render_template('accounts/register.html',
#                                    msg='Username already registered',
#                                    success=False,
#                                    form=create_account_form)

#         # Check email exists
#         user = Users.query.filter_by(email=email).first()
#         if user:
#             return render_template('accounts/register.html',
#                                    msg='Email already registered',
#                                    success=False,
#                                    form=create_account_form)

#         # else we can create the user
#         user = Users(**request.form)
#         db.session.add(user)
#         db.session.commit()

#         return render_template('accounts/register.html',
#                                msg='User created please <a href="/login">login</a>',
#                                success=True,
#                                form=create_account_form)

#     else:
#         return render_template('accounts/register.html', form=create_account_form)


# @blueprint.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('authentication_blueprint.login'))


# # Errors

# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return render_template('home/page-403.html'), 403


# @blueprint.errorhandler(403)
# def access_forbidden(error):
#     return render_template('home/page-403.html'), 403


# @blueprint.errorhandler(404)
# def not_found_error(error):
#     return render_template('home/page-404.html'), 404


# @blueprint.errorhandler(500)
# def internal_error(error):
#     return render_template('home/page-500.html'), 500

