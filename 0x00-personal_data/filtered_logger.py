#!/usr/bin/env python3
"""
eturns the log message obfuscated
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Args:
        fields (list): list of strings indicating fields to obfuscate
        redaction (str): what the field will be obfuscated to
        message (str): the log line to obfuscate
        separator (str): the character separating the fields
        """
    pattern = f"({'|'.join(fields)})=.*?{separator}"
    return re.sub(pattern, lambda match: f"{match.group(1)}={redaction}{separator}", message)
