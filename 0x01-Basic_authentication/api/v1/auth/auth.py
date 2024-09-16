#!/usr/bin/env python3
"""Authentication module."""
from flask import request
from typing import List, TypeVar


class Auth:
    """Basic authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to determine if authentication is required for a given path.
        """
        return False
    
    def authorization_header(self, request=None) -> str:
        """
        Method to retrieve the Authorization header from the request.
        """
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to retrieve the current user based on the request.
        """
        return None