#!/usr/bin/env python3
"""Module with a function called filter_datum"""
import logging
import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates the fields in the log message.

    Args:
        fields (List[str]): Fields to obfuscate.
        redaction (str): The string to replace the field values.
        message (str): The log message.
        separator (str): The separator used in the log message.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(f"{field}=(.*?){separator}",
                         f"{field}={redaction}{separator}", message)
    return message
