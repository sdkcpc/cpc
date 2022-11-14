import sys
import os
import re
import inquirer
import requests
import json
import os.path
import emoji
from .common import *
from inquirer import errors
from cerberus import Validator
from datetime import datetime
from assertpy import assert_that
from rich.console import Console
from .common import *

console = Console()


def validateAll():
    validate_data_project()
    validate_folder_project()
    if GetValidate83():
        validate_files(True)
    else:
        validate_files(False)


def validate_data_project():
    if not os.path.exists(PWD + MAKEFILE):
        validateError("File " + MAKEFILE + " does not exist in current path", "red")
        sys.exit(1)

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
        "validate83": {'type': 'boolean', 'required': True},
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
        "concatenate": {'type': 'boolean', 'required': True},
        "bas_file": {
            'type': 'string',
            'empty': False,
            'required': True,
            'regex': '^([a-zA-Z0-9])+(.bas|.BAS)$',
        },
        "model.cpc": {
            'type': 'string',
            'empty': False,
            'required': True,
            'allowed': ["464", "664", "6128"]
        },
        "m4_ip": {
            'type': 'string',
            'empty': False,
            'required': True,
            'regex': '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        }
    }

    v = Validator(schema)
    f = open(PWD + MAKEFILE)
    data = json.load(f)

    if GetValidate83():
        file_name, file_extension = os.path.splitext(data["bas_file"])
        if len(file_name) > 8:
            validateOK("Bas file does not conform to 8.3 format!")
            sys.exit(1)

    if not v.validate(data):
        validateOK(str(v.errors))
        sys.exit(1)
    else:
        validateOK(MAKEFILE + " file successfully!")


def GetValidate83():
    f = open(PWD + MAKEFILE)
    data = json.load(f)
    return data["validate83"]


def validate_files(format_83_files):
    for i in FOLDERS_PROJECT_NEW:
        arr = next(os.walk(PWD + i))[2]

        # if len(arr) == 0:
        #     print("[ - ] No files in folder " + i)
        for x in range(0, len(arr)):
            # validate format 8.3 files
            if format_83_files:
                if len(os.path.splitext(arr[x])[1]) != 4 or len(os.path.splitext(arr[x])[0]) > 8:
                    validateError("./" + i + "/" + arr[x] + " does not conform to 8:3 file format.")
                else:
                    validateOK("Format file 8.3 ./" + i + "/" + arr[x])
            # Validate spaces in files
            if ' ' in arr[x]:
                validateError("./" + i + "/" + arr[x] + " contains spaces.")

            if i == "src":
                if not os.path.splitext(arr[x])[1].upper() == ".BAS":
                    validateError("./" + i + "/" + arr[x] + " Does not have .BAS extension.")


def validate_folder_project():
    for i in FOLDERS_PROJECT_NEW:
        if not os.path.isdir(PWD + i):
            validateError(i + " Folder not exist in this project.")
            sys.exit(1)
        else:
            validateOK("Exist folder ./" + i)


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


def validateOK(message):
    print(emoji.emojize("[ ✔ ] " + message))


def validateError(message):
    print(emoji.emojize("[:boom: ][red] " + message))
    sys.exit(1)
