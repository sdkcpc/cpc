import os.path
import os.path
from os import path
from zipfile import ZipFile
import subprocess
import requests
from tqdm.auto import tqdm

from .about import *
from .validator import *
from .init import *

SOFTWARE_PATH = os.environ['HOME'] + "/sdkcpc/resources"

if sys.platform == "darwin":
    iDSK = SOFTWARE_PATH + "/iDSK"
    URL = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-OSX.zip"
elif sys.platform == "win32" or sys.platform == "win64":
    iDSK = SOFTWARE_PATH + "/iDSK.exe"
    URL = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-windows.zip"
elif sys.platform == "linux":
    iDSK = SOFTWARE_PATH + "/iDSK"
    URL = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-linux.zip"


def loadCommand(file):
    """
    create dsk image

    Args:
        file (string): Path of file

    """

    # Show header is activated in config
    headerAmstrad()

    # if not exist file exit
    commandFileExist(file)
    file = os.getcwd() + "/" + file

    # Open Visual Studio Code
    openVscode(file)

    # Show Message
    print("[✔] Open Visual Studio Code")


# Open Visual Studio Code
def openVscode(project):
    FNULL = open(os.devnull, 'w')
    try:
        subprocess.call(['code', project], stdout=FNULL, stderr=subprocess.STDOUT)
    except OSError as err:
        print('[X] The Visual Studio Code does not exist. ' + err)
