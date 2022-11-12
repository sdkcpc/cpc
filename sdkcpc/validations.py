import sys
import os
import re
import inquirer
from .common import *
from inquirer import errors
from cerberus import Validator
from datetime import datetime


def validate_data_project():
    schema = {
        "compilation": {
                'required': True,
                'type': 'string',
                'regex': '^(?!\s*$).+',
            },
        "version": {
                'type': 'string',
                'empty': False,
                'required': True,
                'regex': '^(?:(0\\.|([1-9]+\\d*)\\.))+(?:(0\\.|([1-9]+\\d*)\\.))+((0|([1-9]+\\d*)))$',
            },
        "validate83": {'type': 'string'},
        "name_project": {
                'type': 'string',
                'empty': False,
                'required': True
            },
        "description": {
                'type': 'string',
                'empty': True,
                'required': True
            },
        "template": {
                'type': 'string',
                'empty': False,
                'required': True,
                'allowed': ["BASIC", "8BP"]
            },
        "author": {
                'type': 'string',
                'empty': False,
                'required': True,
                'regex': '^(?!\s*$).+',
            },
        "concatenate": {'type': 'string'},
        "bas_file": {'type': 'date'},
        "model.cpc": {'type': ['string', 'list']},
        "m4_ip": {'type': ['string', 'list']}
    }

    response = requests.get("https://www.anapioficeandfire.com/api/books/1")

    v = Validator(schema)
    validate_response = v.validate(response.json())
    assert_that(validate_response, description=v.errors).is_true()

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


def project_name_validation(answers, current):
    if os.path.isdir(PWD + current):
        raise errors.ValidationError('', reason='The project name exists in this path!')

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
