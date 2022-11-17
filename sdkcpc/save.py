import os.path
import os.path
import sys
import getpass as gt
from datetime import datetime

from rich import print
from rich.table import Table
from sdkcpc.init import createTemplate, copyFile

from .about import headerAmstrad
from .validator import *


def saveCommand(file, template):
    """
    create file bas in project

    Args:
        file (string): Path of file
        template (string):

    """

    # Show header is activated in config
    headerAmstrad()

    # Check if the file exists
    if isExist(os.getcwd() + "/" + file):
        print("File exists in this path.")
        sys.exit(1)

    # Check that it does not have blank spaces
    if ' ' in file:
        print("Bad command")
        sys.exit(1)

    # We check that the name of the file without extension does not have more than 8 characters
    if len(file) > 8:
        file_split = os.path.splitext(file)
        file = file_split[0][0:8] + file_split[1]

    data = {"project": os.path.basename(os.path.normpath(os.getcwd())), "build": str(datetime.now()),
            "version": "1.0.0"}
    createTemplate(data, template.lower() + ".j2", file)

    if template.upper() == "8BP":
        if not os.path.exists(os.getcwd() + "/.sdkcpc/8bp.dsk"):
            copyFile(os.path.dirname(os.path.abspath(__file__)) + "/resources/software/8bp.dsk",
                     os.getcwd() + "/.sdkcpc/8bp.dsk")
