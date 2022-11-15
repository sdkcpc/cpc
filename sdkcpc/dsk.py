import os.path
import os.path
import sys
import getpass as gt
from zipfile import ZipFile

import requests
from tqdm.auto import tqdm
from rich import print
from rich.table import Table
from .validator import *


def dskCommand(file):
    """
    create dsk image

    Args:
        file (string): Path of file

    """
    # Check that it is an sdkcpc project
    if not isConfig():
        print("This folder is not a valid sdkcpc project")
        sys.exit(1)

    # If the project does not exist, we create a folder
    if not os.path.exists(os.getcwd() + "/OUT"):
        os.mkdir(os.getcwd() + "/OUT")

    # isConcat()
    # Download iDSK software if not exist
    downloadiDsk()

    # create new buil/version
    new_version = patchVersion(readConfigKey("compilation", "version"))
    new_compilation = str(datetime.now())

    # Deleting comment lines ('1) bas files
    files = next(os.walk(os.getcwd()))[2]
    for file in files:
        if file.endswith(".BAS").upper():
            remove_comments_lines_in_bas_files(file, new_version, new_compilation)


def downloadiDsk():
    """
    download idsk file

    Args:
        file (string): Path of file
    """
    if not os.path.exists(os.environ['HOME'] + "/sdkcpc/resources"):
        os.makedirs(os.environ['HOME'] + "/sdkcpc/resources")
    if not os.path.exists(os.environ['HOME'] + "/sdkcpc/resources/iDSK"):
        print("[+] Download iDSK Software Version 0.20.... please wait..")
        with requests.get("https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-OSX.zip",
                          stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="") as raw:
                with open(os.environ['HOME'] + "/sdkcpc/resources/idsk.zip", 'wb') as output:
                    shutil.copyfileobj(raw, output)
                    with ZipFile(os.environ['HOME'] + "/sdkcpc/resources/idsk.zip", "r") as zipObj:
                        zipObj.extractall(os.environ['HOME'] + "/sdkcpc/resources")
        os.remove(os.environ['HOME'] + "/sdkcpc/resources/idsk.zip")
        if sys.platform == "darwin" or sys.platform == "linux":
            chmod(os.environ['HOME'] + "/sdkcpc/resources/iDSK")


def chmod(path):
    """
    chmod to file

    Args:
        file (string): Path of file

    """
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(path, mode)


def patchVersion(version):
    """
    increment version

    Args:
        version (string): version format x.x.x

    """
    version = version.split('.')
    version[2] = str(int(version[2]) + 1)
    return '.'.join(version)


def remove_comments_lines_in_bas_files(file, new_version, new_compilation):
    """
    delete comment vscode lines in bas files

    Args:
        version (string): version format x.x.x

    """
    # Elimina comentarios de linea de Visual studio Code (1 ')
    with open(os.getcwd() + file, "r") as input:
        with open(OBJ_PATH + "/" + file, "w", newline='\r\n') as output:
            output.write("1 ' Version: " + new_version + " -- Build: " + new_compilation)
            for line in input:
                if not line.strip("\n").startswith("1 '"):
                    output.write(line)
            output.write("\n")
    validateOK("Remove Comment lines -> OBJ/" + file)
    validateOK("Unix to Dos -> OBJ/" + file)
