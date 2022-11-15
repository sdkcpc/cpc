import os
import os.path


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
    return isExist(os.getcwd() + "/.config")
