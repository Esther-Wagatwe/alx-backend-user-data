#!/usr/bin/env python3
"""
Authentication system
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hash password"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def _generate_uuid() -> str:
    """Generates unique ids"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user using email and password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Locates user by email"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if bcrypt.checkpw(password.encode(), user.hashed_password) is True:
            return True
        return False

    def create_session(self, email: str) -> str:
        """Takes an email and returns a session id as a string"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Returns User based on the session_id"""
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy session"""
        if user_id:
            self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates reset password token for valid user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the password after resetting"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            hashed_pwd = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=hashed_pwd, reset_token=None)
