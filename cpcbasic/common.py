import os.path
import configparser
import os
import sys
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style
import os.path
import re
import configparser
from jinja2 import Environment, FileSystemLoader


class MyParser(configparser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


style = Style.from_dict({
    'red': '#ff0066',
    'green': '#44ff00',
    'yellow': '#ffff00',
    'blue': '#0000FF'
})


def get_configuration():
    #     print(get_configuration()["FILE_CONFIG"])
    values = None
    values = {
        "PROJECT_FOLDERS": ["src", "assets", "assets/8bp", "assets/images", "out", "obj"],
        "PROJECT_PATH": os.getcwd() + "/",
        "PROJECT_TMP": os.getcwd() + "/tmp/",
        "PROJECT_OUT": os.getcwd() + "/out/",
        "PROJECT_M4": os.getcwd() + "/out/m4/",
        "PROJECT_CONFIG": os.getcwd() + "/",
        "LOCAL_RESOURCES_TEMPLATES": os.path.dirname(os.path.abspath(__file__)) + "/resources/templates/",
        "LOCAL_RESOURCES_VSCODE": os.path.dirname(os.path.abspath(__file__)) + "/resources/vscode",
        "LOCAL_RESOURCES_SOFTWARE": os.path.dirname(os.path.abspath(__file__)) + "/resources/software/",
        "SOFTWARE_TOOLS": os.path.dirname(os.path.abspath(__file__)) + "/resources/software/" + sys.platform,
        "FILE_CONFIG": os.getcwd() + "/config",
        "FILE_M4": os.getcwd() + "/.m4",
        "FILE_CDT": os.getcwd() + "/cdt",
        "FILE_HISTORY": os.getcwd() + '/.history',
        "LIBRARY_8BP": os.getcwd() + "/assets/8bp/8bp.dsk",
        "iDSK_WIN": "idsk.exe",
        "iDSK_LINUX": "iDSK",
        "iDSK_OSX": "iDSK",
        "SOFTWARE_PATH": os.environ['HOME'] + "/cpcbasic/resources/",
        "VERSION_TOOLS": "1.1",
        "TOOLS": "https://github.com/cpcbasic/cpc-tools/releases/download/1.2/tools-" + sys.platform + ".zip",
        "URL_RVM_WIN": "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7"
                       ".windows.x86.zip",
        "URL_RVM_LINUX": "https://static.retrovm.org/release/beta1/linux/x64/RetroVirtualMachine.2.0.beta-1.r7.linux"
                         ".x64.zip",
        "URL_RVM_OSX": "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7"
                       ".windows.x86.zip",
        "COMMAND_LIST": ["ABOUT", "MAKE", "MACHINE", "CAT", "RUN", "LOAD", "SAVE", "CLS", "CONCAT", "SCR", "PAL"],
        "COMMANDS_8BP": ['8BP.BIN', '|3D', '|ANIMA', '|ANIMALL', '|AUTO', '|AUTOALL', '|COLAY', '|COLSP', '|COLSPALL',
                         '|LAYOUT',
                         '|LOCATESP', '|MAP2SP', '|MOVER', '|MOVERALL', 'MUSIC', '|MUSIC', '|PEEK', '|POKE', '|PRINTAT',
                         '|PRINTSP', '|PRINTSPALL', '|RINK', '|ROUTESP', '|ROUTEALL', '|SETLIMITS', '|SETUPSP',
                         '|UMAP', ],

    }

    return values


def dataProject():
    """
    get data project

    """
    data = MyParser()
    data.read(get_configuration()["FILE_CONFIG"])
    d = data.as_dict()
    return d


def Message(message):
    """
    Show info messages

    Args:
        message (string): Text to show
    """
    print_formatted_text(HTML('<yellow>' + message + '</yellow>'), style=style)


def MessageRed(message):
    """
    Show info messages

    Args:
        message (string): Text to show
    """
    print_formatted_text(HTML('<red>' + message + '</red>'), style=style)


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

    if not isExist(get_configuration()["PROJECT_PATH"] + file):
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
    return os.path.exists(get_configuration()["PROJECT_CONFIG"])


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
    config.read(get_configuration()["FILE_CONFIG"])
    return config.get(section, key)


def updateConfigKey(section, key, value, path=get_configuration()["PROJECT_CONFIG"]):
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
    with open(get_configuration()["FILE_CONFIG"], 'a') as configfile:
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


def createFile(file, text):
    """
    create file

    Args:
        file (string): Path of file
        text (string): file text

    """
    fp = open(file, 'w')
    fp.write(text)
    fp.close()


def validate_path(filepath):
    """
    Validate path folder

    Args:
        filepath (string): Path of folder

    """
    pattern = ""
    if sys.platform == "darwin" or sys.platform == "linux":
        pattern = r"^\/([A-z0-9-_+]+\/)*([A-z0-9])"
    elif sys.platform == "win32" or sys.platform == "win64":
        pattern = r"/^(?:[\w]\:|\/)(\/[a-z_\-\s0-9\.]+)/i"

    if re.match(pattern, filepath):
        return True
    else:
        return False
