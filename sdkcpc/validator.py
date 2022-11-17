import os.path
import configparser
import os


def isExist(file):
    """
    Check if there is a file

    Args:
        file (string): Path of file
    """
    if not os.path.exists(file):
        return False
    return True


def isSdkProject():
    """Check if there is a file"""
    return os.path.exists(os.getcwd() + "/.sdkcpc")


def getModel():
    """Check if there is a file"""
    return readConfigKey("rvm", "model")


def getVersion():
    """Check if there is a file"""
    return readConfigKey("compilation", "version")


def getDSK():
    """Check if there is a file"""
    return readConfigKey("files", "dsk")


def getBuild():
    """Check if there is a file"""
    return readConfigKey("compilation", "build")


def getConcat():
    """Check if there is a file"""
    file = readConfigKey("files", "concat")
    if file:
        return file
    return False


def getHeader():
    """Check if there is a file"""
    return readConfigKey("header", "show")


def getFooter():
    """Check if there is a file"""
    return readConfigKey("footer", "show")


def readConfigKey(section, key):
    """
    read key value ini file

    Args:
        file (string): Path of file
        section (string): section ini file
        key (string): key section ini file

    """
    config = configparser.RawConfigParser()
    config.read(os.getcwd() + "/.sdkcpc/config")
    return config.get(section, key)


def updateConfigKey(section, key, value):
    """
    update key value ini file

    Args:
        file (string): Path of file
        section (string): section ini file
        key (string): key section ini file
        value (string): section key value ini file

    """
    config = configparser.RawConfigParser()
    config.read(os.getcwd() + "/.sdkcpc/config")
    config.set(section, key, value)
    with open(os.getcwd() + "/.sdkcpc/config", 'w') as configfile:
        config.write(configfile)


def createConfigKey(section, key, value):
    """
    create file ini config

    Args:
        file (string): Path of file
        section (string): section ini file
        key (string): key section ini file
        value (string): section key value ini file

    """
    config = configparser.ConfigParser()
    config.add_section(section)
    config.set(section, key, value)
    with open(os.getcwd() + "/.sdkcpc/config", 'a') as configfile:
        config.write(configfile)
