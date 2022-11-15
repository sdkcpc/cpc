import configparser
import os


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

