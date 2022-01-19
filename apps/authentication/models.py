# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

# from apps import db, login_manager
from ..database import Base

from sqlalchemy import Column, String, Integer, LargeBinary

from apps.authentication.util import hash_pass
# from apps import login_manager



# class Users(db.Model, UserMixin):
class Users(Base):

    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    email = Column(String(64), unique=True)
    # password = Column(LargeBinary)
    password = Column(String(64))

    # def __init__(self, **kwargs):
    #     for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            # if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                # value = value[0]

            # if property == 'password':
            #     value = hash_pass(value)  # we need bytes here (not plain str)

            # setattr(self, property, value)

    # def __repr__(self):
    #     return str(self.username)

