# -*- encoding: utf-8 -*-

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from apps.authentication import routes as auth_routes
from apps.home import routes as home_routes

from .database import Base, engine

from starlette.exceptions import HTTPException as StarletteHTTPException


def create_app():
    app = FastAPI()

    mount_static(app)
    custom_error_pages(app)
    register_routes(app)
    configure_database(app)

    return app


def mount_static(app):
    app.mount(
        "/static",
        StaticFiles(directory="apps/static"),
        name="static",
    )


def custom_error_pages(app):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):

        templates = Jinja2Templates(directory="apps/templates")

        if exc.status_code == 403 or exc.status_code == 404 or exc.status_code == 500:
            return templates.TemplateResponse(f"home/page-{exc.status_code}.html", {"request": request})

        if exc.status_code == 401:
            return templates.TemplateResponse("home/page-403.html", {"request": request})

        return templates.TemplateResponse("home/page-error.html", {"request": request, "exc": exc})

    
def register_routes(app):
    app.include_router(auth_routes.router)
    app.include_router(home_routes.router)


def configure_database(app):
    @app.on_event("startup")
    def startup():
        Base.metadata.create_all(bind=engine)