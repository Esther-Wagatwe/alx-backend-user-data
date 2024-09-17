#!/usr/bin/env python3
"""Authentication module."""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """Basic authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to determine if authentication is required for a given path.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        normalized_excluded_paths = [p if p.endswith('/') else p + '/'
                                     for p in excluded_paths]

        for excluded_path in normalized_excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to retrieve the Authorization header from the request.
        """
        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'): # type: ignore
        """
        Method to retrieve the current user based on the request.
        """
        return None
