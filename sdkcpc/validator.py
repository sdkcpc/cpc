import os
import os.path
from .init import *


def isExist(file):
    """
    Check if there is a file

    Args:
        file (string): Path of file
    """
    if not os.path.exists(file):
        return False
    return True


def isConfig():
    """Check if there is a file"""
    return os.path.exists(os.getcwd() + "/.sdkcpc")


def isModel():
    """Check if there is a file"""
    return readConfigKey("rvm", "model")


def isVersion():
    """Check if there is a file"""
    return readConfigKey("compilation", "version")


def isDSK():
    """Check if there is a file"""
    return readConfigKey("files", "dsk")


def isBuild():
    """Check if there is a file"""
    return readConfigKey("compilation", "build")


def isConcat():
    """Check if there is a file"""
    file = readConfigKey("files", "concat")
    if file:
        return file
    return False
