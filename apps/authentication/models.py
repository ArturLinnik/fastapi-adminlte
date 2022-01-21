# -*- encoding: utf-8 -*-

# models.py

from ..database import Base

from sqlalchemy import Column, String, Integer


class Users(Base):

    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    email = Column(String(64), unique=True)
    password = Column(String(64))