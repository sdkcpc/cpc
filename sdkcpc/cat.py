import os.path
import os.path
import sys
import getpass as gt
import pathlib

from rich import print
from rich.columns import Columns
from rich.table import Table
from .validator import *


def catCommand():
    """Show files in folder (Format Amstrad)"""
    # initialitate variables
    col = ""
    count = 1
    column = 1
    totalKbytes = 0

    # Check that it is an amstrad repository
    if not isConfig():
        print("no es un ")
        sys.exit(1)

    # show files in folders
    grid = Table.grid(expand=False)
    grid.add_column()
    grid.add_column(justify="right")

    files = next(os.walk(os.getcwd()))[2]

    for file in files:
        # if it is not a folder we show it
        file_split = os.path.splitext(file)
        if column == 1:
            file_extension = pathlib.Path(os.getcwd() + "/" + file).suffix
            totalKbytes = totalKbytes + int(GetKbytes(file))
            col = '{:<8s}{:>3s}{:>8s}'.format(file_split[0].ljust(8, " "), file_split[1], GetKbytes(file) + "K")
            column = column + 1
        else:
            totalKbytes = totalKbytes + int(GetKbytes(file))
            file_extension = pathlib.Path(os.getcwd() + "/" + file).suffix
            col = col + '   {:<8s}{:>3s}{:>8s}'.format(file_split[0].ljust(8, " "), file_split[1], GetKbytes(file) + "K")
            grid.add_row(col)
            column = 1
            col = ""

        if count == len(files):
            grid.add_row(col)
        count = count + 1

    # Show files
    print("Drive A: user " + str(gt.getuser()) + "\n")
    print(grid)
    bytesFree = 180 - int(totalKbytes)
    print("\n" + str(bytesFree) + "K free")


def GetKbytes(file):
    """
    Get Kbites of files

    Args:
        file (string): Path of file

    """
    if int(f"{os.path.getsize(file) / float(1 << 10):,.0f}") == 0:
        return "1"
    else:
        return str(f"{os.path.getsize(file) / float(1 << 10):,.0f}")
