#!/usr/bin/env python3

import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Redacts specified fields in a log message by replacing the field values
    with a redaction string.

    Args:
        fields (List[str]): A list of field names to redact.
        redaction (str): The string to replace the field values with.
        message (str): The original log message.
        separator (str): The field separator in the log message.

    Returns:
        str: The log message with specified fields redacted.
    """
    # Create a regex pattern to match each field to redact
    pattern = (
        r"(" + "|".join(f"{field}=" for field in fields) + r")[^"
        + re.escape(separator) + r"]+"
    )

    # Use re.sub with a lambda to replace matched fields with the redaction
    return re.sub(pattern, lambda m: m.group(1) + redaction, message)
