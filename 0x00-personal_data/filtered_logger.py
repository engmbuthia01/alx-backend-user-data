#!/usr/bin/env python3
"""
eturns the log message obfuscated
"""
import re
from typing import List
import logging


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
