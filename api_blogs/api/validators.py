import re

from django.conf import settings
from django.core import exceptions


def validate_username(value):
    if value == 'me':
        raise exceptions.ValidationError('Using "me" is not allowed')
    prog = re.sub(settings.ALLOWED_SYMBOLS, repl='', string=value)
    if prog:
        string_val = ', '.join(set(prog))
        raise exceptions.ValidationError(f'Fobidden symbols: {string_val}')
    return value
