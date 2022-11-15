import os.path
import os.path
import sys
import getpass as gt

from rich import print
from rich.table import Table
from .validator import *


def catCommand():
    """Show files in folder (Format Amstrad)"""
    # initialitate variables
    col = ""
    count = 1
    column = 1
    totalKbytes = 0

    # Check that it is an sdkcpc project
    if not isConfig():
        print("This folder is not a valid sdkcpc project")
        sys.exit(1)

    # show files in folders
    grid = Table.grid(expand=False)
    grid.add_column()
    grid.add_column(justify="right")

    files = next(os.walk(os.getcwd()))[2]

    for file in files:
        # if it is not a folder we show it
        file_split = os.path.splitext(file)
        if len(file_split[0]) > 8:
            file83 = file_split[0][0:7] + "~"
        else:
            file83 = file_split[0]
        if column == 1:
            totalKbytes = totalKbytes + int(GetKbytes(file))
            col = '{:<8s}{:>3s}{:>8s}'.format(file83.ljust(8, " "), file_split[1], GetKbytes(file) + "K")
            column = column + 1
        else:
            totalKbytes = totalKbytes + int(GetKbytes(file))
            col = col + '   {:<8s}{:>3s}{:>8s}'.format(file83.ljust(8, " "), file_split[1], GetKbytes(file) + "K")
            grid.add_row(col)
            column = 1
            col = ""

        if count == len(files):
            grid.add_row(col)
        count = count + 1

    # Show files
    print("\nDrive A: user " + str(gt.getuser()) + "\n")
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
