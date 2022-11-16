import os.path
import os.path
from os import path
from zipfile import ZipFile
import subprocess
import requests
from tqdm.auto import tqdm
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


def dskCommand():
    """
    create dsk image

    Args:
        file (string): Path of file

    """
    # Check that it is and sdkcpc project
    if not isConfig():
        print("This folder is not a valid sdkcpc project")
        sys.exit(1)

    # if exist remove temporal folder
    removeTemporalFolder()

    # If the project does not exist, we create a folder
    if not os.path.exists(os.getcwd() + "/OUT"):
        os.mkdir(os.getcwd() + "/OUT")

    if not os.path.exists(os.getcwd() + "/TMP"):
        os.mkdir(os.getcwd() + "/TMP")

    # Download iDSK software if not exist
    downloadiDsk()

    # create new buil/version
    new_version = patchVersion(readConfigKey("compilation", "version"))
    new_compilation = str(datetime.now())

    # Deleting comment lines ('1) bas files
    files = next(os.walk(os.getcwd()))[2]
    for file in files:
        if file.endswith(".BAS") or file.endswith(".bas"):
            remove_comments_lines_in_bas_files(file, new_version, new_compilation)
    print("[✔] Remove Comment lines BAS files.")

    # concatenate files
    if isConcat():
        files_in_path = next(os.walk(os.getcwd() + "/TMP/"))[2]
        with open(os.getcwd() + "/TMP/" + isConcat() + ".concat", "a") as file_object:
            for basfile in files_in_path:
                with open(os.getcwd() + "/TMP/" + basfile) as file:
                    print("Concatenate file -> " + str(basfile))
                    while line := file.readline().rstrip():
                        file_object.write(line + "\r\n")
                os.remove(os.getcwd() + "/TMP/" + '/' + basfile)
        os.rename(os.getcwd() + "/TMP/" + isConcat() + ".concat", os.getcwd() + "/TMP/" + isConcat())

    # If it exists, we extract the 8BP library binary from the dsk image
    extract8BPLibrary(os.getcwd() + "/.sdkcpc/8bp.dsk", os.getcwd() + "/8BP.BIN")

    dsk = os.getcwd() + "/OUT/" + isDSK()

    # We create DSK file with name last folder of the path
    createDskFile(dsk)

    # Add files to DSK
    AddFilesFolder2Dsk(dsk, os.getcwd() + "/TMP", "BAS")
    AddFilesFolder2Dsk(dsk, os.getcwd(), "None")

    # if exist remove temporal folder
    removeTemporalFolder()

    # Update compilation data in config file
    updateConfigKey("compilation", "version", new_version)
    updateConfigKey("compilation", "build", new_compilation)

    # Show Message
    print("[✔] Build Successfully - Version: " + new_version + " - Build: " + new_compilation)


def downloadiDsk():
    """
    download idsk file

    Args:
        file (string): Path of file
    """

    if not os.path.exists(os.environ['HOME'] + "/sdkcpc/resources"):
        os.makedirs(os.environ['HOME'] + "/sdkcpc/resources")
    if not os.path.exists(iDSK):
        print("[✔] Download iDSK Software Version 0.20.... please wait..")
        with requests.get(URL, stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="") as raw:
                with open(os.environ['HOME'] + "/sdkcpc/resources/idsk.zip", 'wb') as output:
                    shutil.copyfileobj(raw, output)
                    with ZipFile(os.environ['HOME'] + "/sdkcpc/resources/idsk.zip", "r") as zipObj:
                        zipObj.extractall(os.environ['HOME'] + "/sdkcpc/resources")
        os.remove(os.environ['HOME'] + "/sdkcpc/resources/idsk.zip")
        if sys.platform == "darwin" or sys.platform == "linux":
            chmod(iDSK)


def removeTemporalFolder():
    """
    Remove temporal Folder.

    """
    if os.path.exists(os.getcwd() + "/TMP"):
        shutil.rmtree(os.getcwd() + "/TMP")


def chmod(path_file):
    """
    chmod to file

    Args:
        file (string): Path of file

    """
    mode = os.stat(path_file).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(path_file, mode)


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
        file (string): file to comments eliminate
        new_version (string): Version name
        new_compilation (string): Build date

    """
    # Elimina comentarios de linea de Visual studio Code (1 ')
    with open(os.getcwd() + "/" + file, "r") as inputs:
        with open(os.getcwd() + "/TMP/" + file, "w", newline='\r\n') as output:
            output.write("1 ' Version: " + new_version + " -- Build: " + new_compilation)
            for line in inputs:
                if not line.strip("\n").startswith("1 '"):
                    output.write(line)
            output.write("\n")


def extract8BPLibrary(library, destiny):
    """
    add files to dsk image

    Args:
        file (string): path file image sdk library

    """

    if path.exists(library):
        FNULL = open(os.devnull, 'w')

        try:
            subprocess.Popen(
                [os.environ['HOME'] + "/sdkcpc/resources/iDSK", library, "-g", destiny],
                stdout=FNULL, stderr=subprocess.STDOUT)
            print("[✔] Copy the 8BP library to the sdkcpc project.")
        except OSError as err:
            print("Error to Copy the 8BP library to the sdkcpc project: " + str(err))
            sys.exit(1)
    else:
        print("[✔] No exist 8BP library in sdkcpc project.")


def createDskFile(file):
    """
   create dsk file

    Args:
        file (string): name image dsk create

    """
    FNULL = open(os.devnull, 'w')

    try:
        subprocess.Popen([os.environ['HOME'] + "/sdkcpc/resources/iDSK", file, "-n"],
                         stdout=FNULL,
                         stderr=subprocess.STDOUT)
        print("[✔] Create image disk " + os.path.basename(file))
    except OSError as err:
        print("BUILD ERROR - " + "iDSK does not exist. " + str(err))
        sys.exit(1)


def addFileToDsk(file, dsk, type_file):
    """
    add files to dsk image

    Args:
        file (string): path file to added
        dsk (string): path name of dsk file
        type_file (string): values 0 ascii, 1 binary

    """
    FNULL = open(os.devnull, 'w')

    try:
        subprocess.run(
            [os.environ['HOME'] + "/sdkcpc/resources/iDSK", dsk, "-i", file, "-f", "-t", type_file],
            stdout=FNULL, stderr=subprocess.STDOUT)

    except OSError as err:
        print("[X] Error Added file " + file + " to DSK: " + str(err))
        sys.exit(1)


def AddFilesFolder2Dsk(dsk, folder, option):
    """
    add files to dsk image

    Args:
        file (string): path file to added
        folder (string): path files
        option (string): if files BAS or not

    """
    files = next(os.walk(folder))[2]
    for file in files:
        file_add = folder + "/" + file
        file_split = os.path.splitext(file)
        file = file_split[0] + file_split[1]
        if option == "BAS":
            if file_split[1].upper() == ".BAS":
                if is_binary(file_add):
                    addFileToDsk(file_add, dsk, "1")
                    print("[✔] Add binary " + file + " to DSK")
                else:
                    addFileToDsk(file_add, dsk, "0")
                    print("[✔] Add ascii " + file + " to DSK")
        else:
            if file_split[1].upper() != ".BAS":
                if is_binary(file_add):
                    addFileToDsk(file_add, dsk, "1")
                    print("[✔] Add binary " + file + " to DSK")
                else:
                    addFileToDsk(file_add, dsk, "0")
                    print("[✔] Add ascii " + file + " to DSK")


def is_binary(file):
    """
    get file is binary

    Args:
        file (string): file to analizate

    """
    try:
        with open(file, 'tr') as check_file:
            check_file.read()
            return False
    except:
        return True
