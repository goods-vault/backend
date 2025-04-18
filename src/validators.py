import re


def check_valid_code(code: str):
    if not re.fullmatch(r"^(?:\d{8}|\d{13})$", code):
        raise ValueError("The code type must be either EAN-8 or EAN-13.")
    return code
