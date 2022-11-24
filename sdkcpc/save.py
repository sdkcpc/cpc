import os.path
import os.path
import sys
import getpass as gt
from datetime import datetime

from rich import print
from rich.table import Table
from sdkcpc.init import createTemplate, copyFile, add2File
from sdkcpc.cat import *
from .about import headerAmstrad
from .common import *


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
    if isExist(get_configuration()["PROJECT_PATH"] + file):
        errMessage("File exists in this path.")
        sys.exit(1)

    # Check that it does not have blank spaces
    if ' ' in file:
        errMessage("Bad command")
        sys.exit(1)

    if int(getAllKBytes()) < 180:
        # We check that the name of the file without extension does not have more than 8 characters
        if len(file) > 8:
            file = file_split[0][0:8] + file_split[1]

        data = {"project": os.path.basename(os.path.normpath(get_configuration()["PROJECT_PATH"])),
                "build": str(datetime.now()),
                "version": "1.0.0"}
        createTemplate(data, "8bp.j2", file)

        if not os.path.exists(get_configuration()["LIBRARY_8BP"]):
            copyFile(get_configuration()["LOCAL_RESOURCES_SOFTWARE"] + "8bp.dsk", get_configuration()["LIBRARY_8BP"])

        if isExist(get_configuration()["FILE_CDT"]):
            add2File(get_configuration()["FILE_CDT"], file_split[0] + ",,," + file)
    else:
        MessageRed("Drive A: disc full\n")


def getAllKBytes():
    K = 0
    files = next(os.walk(get_configuration()["PROJECT_PATH"]))[2]
    for file in files:
        K = K + int(GetKbytes(get_configuration()["PROJECT_PATH"] + file))

    return K
