import sys
import os
import re
import inquirer
from inquirer import errors


def phone_validation(answers, current):
    if not re.match('\+?\d[\d ]+\d', current):
        raise errors.ValidationError('', reason='I don\'t like your phone number!')

    return True


def validate_ip(answers, current):
    if not re.match('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', current):
        raise errors.ValidationError('', reason='Not a valid IP!')

    return True


def project_name_validation_no(answers, current):
    if not re.match("^\w+$", current):
        raise errors.ValidationError('', reason='Not a valid project name (no spaces and no special characters)!')

    return True


def project_name_validation_yes(answers, current):
    if not re.match("^[\w+]{1,8}$", current):
        raise errors.ValidationError('', reason='Not a valid project name (no spaces and no special characters)!')

    return True


def bas_name_validation_yes(answers, current):
    file_name, file_extension = os.path.splitext(current)
    if len(file_name) > 8 or file_extension.upper() != ".BAS":
        raise errors.ValidationError('', reason='File name or extension is not valid!')
    return True


def bas_name_validation_no(answers, current):
    file_name, file_extension = os.path.splitext(current)
    if len(file_name) < 1 or file_extension.upper() != ".BAS":
        raise errors.ValidationError('', reason='File name or extension is not valid!')

    if ' ' in current:
        raise errors.ValidationError('', reason='File name or extension is not valid!')

    return True
