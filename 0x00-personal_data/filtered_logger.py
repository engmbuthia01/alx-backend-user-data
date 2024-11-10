#!/usr/bin/env python3
"""
eturns the log message obfuscated
"""
import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Return an obfuscated log message
    Args:
        fields (list): list of strings indicating fields to obfuscate
        redaction (str): what the field will be obfuscated to
        message (str): the log line to obfuscate
        separator (str): the character separating the fields
    """
    pattern = f"({'|'.join(fields)})=.*?{separator}"
    return re.sub(
        pattern,
        lambda match: f"{match.group(1)}={redaction}{separator}",
        message
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Redact sensitive information from the log record message.
        """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    """
    Return a logging.Logger object configured for user data.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_db():
    """
    Returns a connector to the MySQL database using credentials
    from environment variables.
    """
    # Fetching database credentials from environment variables
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    
    # Establishing a connection to the MySQL database
    db_connection = mysql.connector.connect(
        host=db_host,
        user=db_username,
        password=db_password,
        database=db_name
    )
    
    return db_connection
