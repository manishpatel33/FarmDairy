import re


def validate_email(email):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    return EMAIL_REGEX.match(email)


def validate_mobile(mobile_no):
    MOBILE_REGEX = re.compile(r'^\+?1?\d{9,15}$')
    return MOBILE_REGEX.match(mobile_no)
