#!/usr/bin/python
import os.path
import json
import sys
import os
import configparser
from rich import print
from . import __version__

from rich.console import Console
console = Console(width=80, color_system="windows", force_terminal=True)

# DEFINE VARIABLES

PWD = os.getcwd() + "/"
MAKEFILE = "Project.cfg"
MY_HOME = os.environ['HOME']+"/sdkcpc/resources"
FOLDERS_PROJECT_NEW = ["resources", "ascii", "bin", "src", "obj"]
MODELS_CPC = ["464", "664", "6128"]
BAS_PATH = PWD + "src"
OBJ_PATH = PWD + "obj"
LOG_FILE = "project.log"
APP_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = APP_PATH + "/resources/templates/"
SOFTWARE = MY_HOME + "/resources/"

# Variables for platform
if sys.platform == "darwin":
    DOWNLOAD_IDSK = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-OSX.zip"
    COMMANDO_IDSK = MY_HOME + "/iDSK"
    RETROVIRTUALMACHINE = MY_HOME + "/RetroVirtualMachine"
    URL = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "win32" or sys.platform == "win64":
    DOWNLOAD_IDSK = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-windows.zip"
    COMMANDO_IDSK = MY_HOME + "/iDSK.exe"
    RETROVIRTUALMACHINE = MY_HOME + "/RetroVirtualMachine.exe"
    URL = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "linux":
    DOWNLOAD_IDSK = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-linux.zip"
    COMMANDO_IDSK = MY_HOME + "/iDSK"
    RETROVIRTUALMACHINE = MY_HOME + "/RetroVirtualMachine"
    URL = "https://static.retrovm.org/release/beta1/linux/x64/RetroVirtualMachine.2.0.beta-1.r7.linux.x64.zip"


# Get data project in dict
def Get_data_project_dict():
    f = open(PWD + MAKEFILE)
    data = json.load(f)
    return data

# Leer propiedad del proyecto
#   @Param Seccion
#   @Param Value
def readCfgKey(section, key):
    try:
        config = configparser.RawConfigParser()
        config.read(PWD + MAKEFILE)
    except:
        console.print("[red bold]\[ERROR]: Key not exist in " + MAKEFILE)
        sys.exit(1)
    return config.get(section, key)


# Leer todas las keys de una seccion
#   @Param Seccion
def readCfgSection(section):
    try:
        config = configparser.RawConfigParser()
        config.read(PWD + MAKEFILE)
        return dict(config.items(section))
    except:
        print("[red bold]\[ERROR]: Section " + section + " not exist in " + MAKEFILE)
        sys.exit(1)


def readBuild():
    file_path = SOFTWARE + "/BUILD"

    if os.path.isfile(file_path):
        text_file = open(file_path, "r")
        data = text_file.read()
        text_file.close()
        return data

    return "Could not read the build"


def show_head(info, color):
    print("[*] ------------------------------------------------------------------------")
    if color == "white":
        console.print("[*][white bold] " + info)
    elif color == "red":
        console.print("[*][red bold] " + info)
    elif color == "green":
        console.print("[*][green bold] " + info)
    print("[*] ------------------------------------------------------------------------")


def show_info(info, color):
    print("[*] ------------------------------------------------------------------------")
    if color == "white":
        console.print("[*][white bold] " + info)
    elif color == "red":
        console.print("[*][red bold] " + info)
    elif color == "green":
        console.print("[*][green bold] " + info)
    print("[*] ------------------------------------------------------------------------")


def show_foot(info, color):
    print("[*] ------------------------------------------------------------------------")
    if color == "white":
        console.print("[*][white bold] " + info)
    elif color == "red":
        console.print("[*][red bold] " + info)
    elif color == "green":
        console.print("[*][green bold] " + info)
    print("[*] ------------------------------------------------------------------------")


def developer_info():
    print(f"sdkcpc v" + str(__version__))
    print(sys.platform + " - Build: " + str(readBuild()))
    print(f"© Destroyer 2022\n")
