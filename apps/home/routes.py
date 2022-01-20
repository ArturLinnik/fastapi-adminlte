# -*- encoding: utf-8 -*-

# from re import template
# from apps.home import blueprint
# from flask import render_template, request
# from flask_login import login_required
# from jinja2 import TemplateNotFound


from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
# from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Header
from typing import Optional
from ..authentication.models import Users
from ..authentication.crud import get_current_user


router = APIRouter()

templates = Jinja2Templates(directory="apps/templates")

@router.get("/index", response_class=HTMLResponse)
async def index(request: Request, user: Users = Depends(get_current_user)):
    return templates.TemplateResponse("home/index.html", {"request": request, "current_user": user.username})


# @blueprint.route('/index')
# @login_required
# def index():

#     return render_template('home/index.html', segment='index')


# @blueprint.route('/<template>')
# @login_required
# def route_template(template):

#     try:

#         if not template.endswith('.html'):
#             template += '.html'

#         # Detect the current page
#         segment = get_segment(request)

#         # Serve the file (if exists) from app/templates/home/FILE.html
#         return render_template("home/" + template, segment=segment)

#     except TemplateNotFound:
#         return render_template('home/page-404.html'), 404

#     except:
#         return render_template('home/page-500.html'), 500


# # Helper - Extract current page name from request
# def get_segment(request):

#     try:

#         segment = request.path.split('/')[-1]

#         if segment == '':
#             segment = 'index'

#         return segment

#     except:
#         return None
