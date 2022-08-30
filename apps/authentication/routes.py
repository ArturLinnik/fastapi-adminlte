# -*- encoding: utf-8 -*-

# authentication/routes.py

from datetime import timedelta

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from ..database import get_db
from .schemas import CreateAccountFormRequest, CreateAccountFormResponse
from .models import Users
from .password import verify_pass, hash_pass
from .crud import get_user, get_email
from .token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter()

templates = Jinja2Templates(directory="apps/templates")

# --- Root ---

# Redirect to /login
@router.get("/")
async def route_default(response: Response):
    response = RedirectResponse(url="/login")

    return response


# --- Register ---


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):

    return templates.TemplateResponse("accounts/register.html", {"request": request})


@router.post("/register", response_model=CreateAccountFormResponse)
async def create_user(
    request: Request,
    form_data: CreateAccountFormRequest = Depends(
        CreateAccountFormRequest.create_account_form
    ),
    db: Session = Depends(get_db),
):

    # Read form data
    username = form_data.username
    email = form_data.email
    password = form_data.password

    # Check if username exists
    user = get_user(db, username)
    if user:
        return templates.TemplateResponse(
            "accounts/register.html",
            {
                "request": request,
                "msg": "Username already registered",
                "success": False,
            },
        )

    # Check email exists
    user = get_email(db, email)
    if user:
        return templates.TemplateResponse(
            "accounts/register.html",
            {"request": request, "msg": "Email already registered", "success": False},
        )

    # Else we can create the user
    user = Users(
        username=username.lower(),
        email=email.lower(),
        password=hash_pass(password),
    )

    # Add user to database
    db.add(user)
    db.commit()
    db.refresh(user)

    return templates.TemplateResponse(
        "accounts/register.html",
        {
            "request": request,
            "msg": "User created please <a href='/login'>login</a>",
            "success": True,
        },
    )


# --- Login ---


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):

    return templates.TemplateResponse("accounts/login.html", {"request": request})


@router.post("/login")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    # Read form data
    username = form_data.username
    password = form_data.password

    # Locate user
    user = db.query(Users).filter(Users.username == username).first()

    # Check the password
    if user and verify_pass(password, user.password):

        # Create token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        # Redirect to /index and set cookie with the access token setting httponly to True
        response = RedirectResponse(url="/index", status_code=303)
        response.set_cookie(
            key="access_token", value=f"Bearer {access_token}", httponly=True
        )

        return response

    # Something (user or pass) is not ok
    return templates.TemplateResponse(
        "accounts/login.html",
        {"request": request, "msg": "Wrong user or password", "success": False},
    )


# --- Logout ---


@router.get("/logout")
async def logout():

    # Delete cookie and redirect to login
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="access_token")

    return response
