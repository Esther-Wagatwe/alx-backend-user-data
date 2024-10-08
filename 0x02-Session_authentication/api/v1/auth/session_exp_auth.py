#!/usr/bin/env python3
"""Module to add an expiration date to a Session ID"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """Class that sets the expiration date of a session ID"""
    def __init__(self):
        """
        Initialize the session expiration class.
        """
        super().__init__()
        self.session_duration = int(os.getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """
        Create a session with a session expiration feature.
        It stores the user_id and the time the session was created.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID from the session dictionary,
        handling session expiration.
        """
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        if self.session_duration <= 0:
            return session_data.get("user_id")

        created_at = session_data.get("created_at")
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return session_data.get('user_id')
