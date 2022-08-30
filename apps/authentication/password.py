# -*- encoding: utf-8 -*-

# password.py

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash a password for storing.
def hash_pass(password):
    return pwd_context.hash(password)


# Verify a stored password against one provided by user
def verify_pass(provided_password, stored_password):
    return pwd_context.verify(provided_password, stored_password)
