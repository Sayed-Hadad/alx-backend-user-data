#!/usr/bin/env python3

""" Use of regex in replacing occurrences of certain field values """

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Replaces occurrences of specified field values with a redacted value.

    Args:
        fields (List[str]): List of field names (e.g., ['password', 'ssn']).
        redaction (str): The string to replace field values with.
        message (str): The log message to redact.
        separator (str): The separator between field-value pairs.
    """
    for field in fields:
        # Replace the field value with redacted value using regex
        message = re.sub(
            f'{field}=(.*?){separator}',
            f'{field}={redaction}{separator}',
            message
        )
    return message
