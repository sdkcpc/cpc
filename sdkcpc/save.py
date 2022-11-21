import os.path
import os.path
import sys
import getpass as gt
from datetime import datetime

from rich import print
from rich.table import Table
from sdkcpc.init import createTemplate, copyFile, add2File

from .about import headerAmstrad
from .validator import *


def saveCommand(file, activate):
    """
    create file bas in project

    Args:
        file (string): Path of file

    """
    file_split = os.path.splitext(file)

    # Show header is activated in config
    # if activate:
    #     headerAmstrad()

    # Check if the file exists
    if isExist(os.getcwd() + "/" + file):
        errMessage("File exists in this path.")
        sys.exit(1)

    # Check that it does not have blank spaces
    if ' ' in file:
        errMessage("Bad command")
        sys.exit(1)

    # We check that the name of the file without extension does not have more than 8 characters
    if len(file) > 8:
        file = file_split[0][0:8] + file_split[1]

    data = {"project": os.path.basename(os.path.normpath(os.getcwd())), "build": str(datetime.now()),
            "version": "1.0.0"}
    createTemplate(data, "8bp.j2", file)

    if not os.path.exists(os.getcwd() + "/.sdkcpc/8bp.dsk"):
        copyFile(os.path.dirname(os.path.abspath(__file__)) + "/resources/software/8bp.dsk",
                 os.getcwd() + "/.sdkcpc/8bp.dsk")

    if isExist(os.getcwd() + "/.sdkcpc/CDT"):
        add2File(os.getcwd() + "/.sdkcpc/CDT", file_split[0] + ",,," + file)
