import os.path
import os.path
from os import path
from zipfile import ZipFile
import subprocess
import requests
from tqdm.auto import tqdm

from .about import *
from .common import *
from .init import *


def loadCommand(file, activate):
    """
    create dsk image

    Args:
        file (string): Path of file

    """

    # Show header is activated in config
    # if activate:
    #     headerAmstrad()

    # if not exist file exit
    if commandFileExist(file):
        file = os.getcwd() + "/" + file

        # Open Visual Studio Code
        openVscode(file)

        # Show Message
        okMessage("Open Visual Studio Code")


# Open Visual Studio Code
def openVscode(project):
    FNULL = open(os.devnull, 'w')
    try:
        subprocess.call(['code', project], stdout=FNULL, stderr=subprocess.STDOUT)
    except OSError as err:
        print('[X] The Visual Studio Code does not exist. ' + str(err))
