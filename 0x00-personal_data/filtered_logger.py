#!/usr/bin/env python3
"""Use regex to replace occurrences of certain field values in log messages."""

import logging
from typing import List
import re
import mysql.connector
import os


# Define the PII fields
PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns regex-obfuscated log messages."""
    pattern = f"({'|'.join(fields)})=(.*?){separator}"
    return re.sub(
        pattern,
        lambda m: f"{m.group(1)}={redaction}{separator}",
        message
    )


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class to obfuscate specified PII fields in logs."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats log record with PII fields obfuscated."""
        original_message = super().format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            original_message,
            self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    """Returns a logger configured to filter PII fields."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # StreamHandler with RedactingFormatter
    target_handler = logging.StreamHandler()
    target_handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))
    target_handler.setFormatter(formatter)

    logger.addHandler(target_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connects to a secure MySQL database using environment variables."""
    db_connect = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    return db_connect
