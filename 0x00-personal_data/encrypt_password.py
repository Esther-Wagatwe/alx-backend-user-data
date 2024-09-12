#!/usr/bin/env python3
""" Returns a salted, hashed password, byte in string """
import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with a salt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        bytes: The salted and hashed password.
    """
    password_bytes = password.encode('utf-8')
    
    salt = bcrypt.gensalt()
    
    return bcrypt.hashpw(password_bytes, salt)

