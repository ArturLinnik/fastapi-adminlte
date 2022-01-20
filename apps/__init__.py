# -*- encoding: utf-8 -*-

# from urllib.request import Request
# from flask import Flask
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
# from importlib import import_module



#######
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apps.authentication import routes as auth_routes
from apps.home import routes as home_routes

from .database import Base, engine

from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates

# from fastapi_login import LoginManager
#######





# db = SQLAlchemy()


# def register_extensions(app):
#     db.init_app(app)
#     login_manager.init_app(app)


# def register_blueprints(app):
#     for module_name in ('authentication', 'home'):
#         module = import_module('apps.{}.routes'.format(module_name))
#         app.register_blueprint(module.blueprint)


# def configure_database(app):

#     @app.before_first_request
#     def initialize_database():
#         db.create_all()

#     @app.teardown_request
#     def shutdown_session(exception=None):
#         db.session.remove()


# # def create_app(config):
# def create_app():
#     app = Flask(__name__)
#     # app.config.from_object(config)
#     register_extensions(app)
#     register_blueprints(app)
#     configure_database(app)
#     return app



###################################


# Fastapi

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="apps/static"),
    name="static",
)

app.include_router(auth_routes.router)
app.include_router(home_routes.router)

templates = Jinja2Templates(directory="apps/templates")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):

    if exc.status_code == 403 or exc.status_code == 404 or exc.status_code == 500:
        return templates.TemplateResponse(f"home/page-{exc.status_code}.html", {"request": request})

    if exc.status_code == 401:
        return templates.TemplateResponse("home/page-403.html", {"request": request})

    return templates.TemplateResponse("home/page-error.html", {"request": request, "status_code": exc.status_code, "detail": exc.detail})


# @app.get("/")
# async def route_default(response: Response):
#     response = RedirectResponse(url="/login")
#     return response

# @app.get("/login", response_class=HTMLResponse)
# async def login(request: Request):
#     return templates.TemplateResponse("accounts/login.html", {"request": request})

# @app.get("/register", response_class=HTMLResponse)
# async def register(request: Request):
#     return templates.TemplateResponse("accounts/register.html", {"request": request})