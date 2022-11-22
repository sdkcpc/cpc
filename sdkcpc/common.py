import os.path
import configparser
import os
import sys
from rich.console import Console
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style

style = Style.from_dict({
    'red': '#ff0066',
    'green': '#44ff00',
    'yellow': '#ffff00',
    'blue': '#0000FF'
})

console = Console()


def get_configuration():
    #     print(get_configuration()["SOFTWARE_PATH"])
    values = None
    values = {
        "PROJECT_PATH": os.getcwd() + "/",
        "PROJECT_TMP": os.getcwd() + "/TMP/",
        "PROJECT_OUT": os.getcwd() + "/OUT/",
        "PROJECT_M4": os.getcwd() + "/OUT/M4",
        "PROJECT_CONFIG": os.getcwd() + "/.sdkcpc/",
        "FILE_CONFIG": os.getcwd() + "/.sdkcpc/config",
        "FILE_M4": os.getcwd() + "/.sdkcpc/.M4",
        "FILE_CDT": os.getcwd() + "/.sdkcpc/CDT",
        "LIBRARY_8BP": os.getcwd() + "/.sdkcpc/8bp.dsk",
        "iDSK_WIN": "idsk.exe",
        "iDSK_LINUX": "iDSK",
        "iDSK_OSX": "iDSK",
        "SOFTWARE_PATH": os.environ['HOME'] + "/sdkcpc/resources/",
        "URL_IDSK_WIN": "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-windows.zip",
        "URL_IDSK_LINUX": "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-linux.zip",
        "URL_IDSK_OSX": "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-OSX.zip",
        "URL_CDT_WIN": "https://github.com/sdkcpc/2cdt/raw/main/binary/win/2cdt.exe",
        "URL_CDT_LINUX": "https://github.com/sdkcpc/2cdt/raw/main/binary/linux/2cdt",
        "URL_CDT_OSX": "https://github.com/sdkcpc/2cdt/raw/main/binary/darwin/2cdt",
        "": "",
        "COMMANDS_8BP": ['8BP.BIN', '|3D', '|ANIMA', '|ANIMALL', '|AUTO', '|AUTOALL', '|COLAY', '|COLSP', '|COLSPALL',
                         '|LAYOUT',
                         '|LOCATESP', '|MAP2SP', '|MOVER', '|MOVERALL', 'MUSIC', '|MUSIC', '|PEEK', '|POKE', '|PRINTAT',
                         '|PRINTSP', '|PRINTSPALL', '|RINK', '|ROUTESP', '|ROUTEALL', '|SETLIMITS', '|SETUPSP',
                         '|UMAP', ],

    }

    return values


def okMessage(message):
    """
    Show info messages

    Args:
        message (string): Text to show
    """

    # if getMessageColor().upper() == "ON":
    print_formatted_text(HTML('<green>[✔]</green> <yellow>' + message + '</yellow>'), style=style)
    # else:
    #    print_formatted_text(HTML('<white>[✔] ' + message + '</white>'), style=style)


def errMessage(message):
    """
    Show info messages

    Args:
        message (string): Text to show
    """
    # if getMessageColor().upper() == "ON":
    print_formatted_text(HTML('<red>[X] ' + message + '</red>'), style=style)
    # else:
    # print_formatted_text(HTML('<white>[X] ' + message + '</white>'), style=style)


def commandFileExist(file):
    """
    Check if there is a file that is passed to the command.

    Args:
        file (string): File to find
    """

    if not isExist(os.getcwd() + "/" + file):
        file_split = os.path.splitext(file.upper())
        if len(file_split[0]) > 8:
            file83 = file_split[0][0:7] + "~"
        else:
            file83 = file_split[0]
        line = '{:<8s}{:>3s} Not found'.format(file83.ljust(8, " "), file_split[1])
        print_formatted_text(HTML('<yellow>' + line + '</yellow>'), style=style)
        return False
    return True


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


def getMessageColor():
    """Check if there is a file"""
    return readConfigKey("messages", "color")


def getModel():
    """Check if there is a file"""
    return readConfigKey("rvm", "model")


def getVersion():
    """Check if there is a file"""
    return readConfigKey("compilation", "version")


def getRun():
    """Check if there is a file"""
    return readConfigKey("files", "run")


def getDSK():
    """Check if there is a file"""
    return readConfigKey("files", "dsk")


def getCDT():
    """Check if there is a file"""
    return readConfigKey("files", "cdt")


def getBuild():
    """Check if there is a file"""
    return readConfigKey("compilation", "build")


def getM4():
    """Check if there is a file"""
    return readConfigKey("m4", "ip")


def getConcat():
    """Check if there is a file"""
    file = readConfigKey("files", "concat")
    if file:
        return file
    return False


def getHeader():
    """Check if there is a file"""
    return readConfigKey("header", "show")


def getHeaderColor():
    """Check if there is a file"""
    return readConfigKey("header", "color")


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


def updateConfigKey(section, key, value, path=os.getcwd() + "/.sdkcpc"):
    """
    update key value ini file

    Args:
        file (string): Path of file
        section (string): section ini file
        key (string): key section ini file
        value (string): section key value ini file

    """
    config = configparser.RawConfigParser()
    config.read(path + "/config")
    config.set(section, key, value)
    with open(path + "/config", 'w') as configfile:
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


def searchCommand(file_path, word):
    """
    find word in bas files

    Args:
        file (string): Path of file
        word (string): word top search

    """
    with open(file_path, 'r') as file:
        # read all content of a file
        content = file.read()
        # check if string present in a file
        if word in content:
            return True
        else:
            return False
