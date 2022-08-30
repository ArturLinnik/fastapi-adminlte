# -*- encoding: utf-8 -*-

# home/routes.py

from ..authentication.models import Users
from ..authentication.crud import get_current_user

from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request


router = APIRouter()

templates = Jinja2Templates(directory="apps/templates")


@router.get("/index", response_class=HTMLResponse)
async def index(request: Request, user: Users = Depends(get_current_user)):

    return templates.TemplateResponse(
        "home/index.html",
        {"request": request, "current_user": user, "segment": "index"},
    )


@router.get("/{template}", response_class=HTMLResponse)
async def route_template(
    request: Request, template: str, user: Users = Depends(get_current_user)
):

    if not template.endswith(".html"):
        template += ".html"

    # Detect the current page
    segment = get_segment(request)

    # Serve the file (if exists) from app/templates/home/FILE.html
    return templates.TemplateResponse(
        f"home/{template}",
        {"request": request, "current_user": user, "segment": segment},
    )


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.url.path.split("/")[-1]

        if segment == "":
            segment = "index"

        return segment

    except:
        return None
