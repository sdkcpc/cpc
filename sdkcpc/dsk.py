import os.path
import os.path
from os import path
import csv
from zipfile import ZipFile
import subprocess
import requests
from tqdm.auto import tqdm

from .about import *
from .validator import *
from .init import *

commands_8bp = ['8BP.BIN', '|3D', '|ANIMA', '|ANIMALL', '|AUTO', '|AUTOALL', '|COLAY', '|COLSP', '|COLSPALL', '|LAYOUT',
                '|LOCATESP', '|MAP2SP', '|MOVER', '|MOVERALL', 'MUSIC', '|MUSIC', '|PEEK', '|POKE', '|PRINTAT',
                '|PRINTSP', '|PRINTSPALL', '|RINK', '|ROUTESP', '|ROUTEALL', '|SETLIMITS', '|SETUPSP', '|UMAP', ]

SOFTWARE_PATH = os.environ['HOME'] + "/sdkcpc/resources"

if sys.platform == "darwin":
    iDSK = SOFTWARE_PATH + "/iDSK"
    URL_IDSK = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-OSX.zip"
    CDT = SOFTWARE_PATH + "/2cdt"
    URL_CDT = "https://github.com/sdkcpc/2cdt/raw/main/binary/darwin/2cdt"
elif sys.platform == "win32" or sys.platform == "win64":
    iDSK = SOFTWARE_PATH + "/iDSK.exe"
    URL_IDSK = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-windows.zip"
    CDT = SOFTWARE_PATH + "/2cdt.exe"
    URL_CDT = "https://github.com/sdkcpc/2cdt/raw/main/binary/win/2cdt.exe"
elif sys.platform == "linux":
    iDSK = SOFTWARE_PATH + "/iDSK"
    URL_IDSK = "https://github.com/destroyer-dcf/idsk/releases/download/v0.20/iDSK-0.20-linux.zip"
    CDT = SOFTWARE_PATH + "/2cdt"
    URL_CDT = "https://github.com/sdkcpc/2cdt/raw/main/binary/linux/2cdt"


def dskCommand(activate):
    """
    create dsk image

    Args:
        activate (boolean): activate header

    """
    # Show header is activated in config
    if activate:
        headerAmstrad()

    # Check that it is and sdkcpc project
    if not isSdkProject():
        print("This folder is not a valid sdkcpc project")
        sys.exit(1)

    # if exist remove temporal folder
    removeTemporalFolder()

    # If the project does not exist, we create a folder
    if not os.path.exists(os.getcwd() + "/OUT"):
        os.mkdir(os.getcwd() + "/OUT")

    if not os.path.exists(os.getcwd() + "/OUT/M4"):
        os.mkdir(os.getcwd() + "/OUT/M4")

    if not os.path.exists(os.getcwd() + "/TMP"):
        os.mkdir(os.getcwd() + "/TMP")

    # Download iDSK software if not exist
    downloadiDsk()

    # Initialize M4 file
    createFile(os.getcwd() + "/.sdkcpc/.M4", "")

    # create new buil/version
    new_version = patchVersion(readConfigKey("compilation", "version"))
    new_compilation = str(datetime.now())

    # Deleting comment lines ('1) bas files
    files = next(os.walk(os.getcwd()))[2]
    for file in files:
        if file.endswith(".BAS") or file.endswith(".bas"):
            remove_comments_lines_in_bas_files(file, new_version, new_compilation)
    okMessage("Remove Comment lines BAS files.")

    # concatenate files
    if getConcat():
        files_in_path = next(os.walk(os.getcwd() + "/TMP/"))[2]
        with open(os.getcwd() + "/TMP/" + getConcat() + ".concat", "a") as file_object:
            for basfile in files_in_path:
                with open(os.getcwd() + "/TMP/" + basfile) as file:
                    while line := file.readline().rstrip():
                        file_object.write(line + "\r\n")
                os.remove(os.getcwd() + "/TMP/" + '/' + basfile)
        os.rename(os.getcwd() + "/TMP/" + getConcat() + ".concat", os.getcwd() + "/TMP/" + getConcat())

    # If it exists, we extract the 8BP library binary from the dsk image
    if findCommand8BP():
        extractFileDSK(os.getcwd() + "/.sdkcpc/8bp.dsk", os.getcwd() + "/8BP.BIN")

    dsk = os.getcwd() + "/OUT/" + getDSK()

    # We create DSK file with name last folder of the path
    okMessage("------- Create DSK Image -------")
    createDskFile(dsk)

    # Add files to DSK
    AddFilesFolder2Dsk(dsk, os.getcwd() + "/TMP", "BAS")
    AddFilesFolder2Dsk(dsk, os.getcwd(), "None")

    # Create CDT Imagen
    if isExist(os.getcwd() + "/.sdkcpc/CDT"):
        cdt = os.getcwd() + "/OUT/" + getCDT()
        okMessage("------- Create CDT Image -------")
        download2cdt()
        createCdtFile(cdt)

        rows = []
        addArchive = [CDT, "-b", "2000", "-r"]
        with open(os.getcwd() + "/.sdkcpc/CDT", 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                if not row[0]:
                    row[0] = "ARCHIVE"
                addArchive.append(row[0])
                if row[1]:
                    addArchive.append("-L")
                    addArchive.append(row[1])
                if row[2]:
                    addArchive.append("-X")
                    addArchive.append(row[2])
                if row[3]:
                    file_split = os.path.splitext(row[3])
                    if file_split[1].upper() == ".BAS":
                        addArchive.append(os.getcwd() + "/TMP/" + row[3])
                    else:
                        addArchive.append(os.getcwd() + "/" + row[3])
                else:
                    errMessage("No exist file in CDT file")
                addArchive.append(cdt)
                addFileToCdt(addArchive)
                okMessage("Add " + row[3] + " to CDT")
                addArchive = [CDT, "-b", "2000", "-r"]

    if getM4() != "0.0.0.0":
        okMessage("------- Create M4 Folder -------")
        with open(os.getcwd() + "/.sdkcpc/.M4") as M4File:
            for line in M4File:
                if line:
                    extractFileDSK(dsk, os.getcwd() + "/OUT/M4/" + line)

    # if exist remove temporal folder
    removeTemporalFolder()

    # Update compilation data in config file
    updateConfigKey("compilation", "version", new_version)
    updateConfigKey("compilation", "build", new_compilation)

    # Show Message
    okMessage("Build Successfully - Version: " + new_version + " - Build: " + new_compilation)


def createCdtFile(file):
    """
   create dsk file

    Args:
        file (string): name image dsk create

    """
    FNULL = open(os.devnull, 'w')

    try:
        subprocess.Popen([CDT, "-n", ".", file], stdout=FNULL, stderr=subprocess.STDOUT)
        okMessage("Create image cdt " + os.path.basename(file))
    except OSError as err:
        print("BUILD ERROR - " + "CDT does not exist. " + str(err))
        sys.exit(1)


def addFileToCdt(data):
    """
    add files to dsk image

    Args:
        file (string): path file to added
        dsk (string): path name of dsk file
        type_file (string): values 0 ascii, 1 binary

    """
    FNULL = open(os.devnull, 'w')

    try:
        subprocess.run(data, stdout=FNULL, stderr=subprocess.STDOUT)
    except OSError as err:
        errMessage(" Error Added file " + file + " to DSK: " + str(err))
        sys.exit(1)


def download2cdt():
    """
    download CDT file

    Args:
        file (string): Path of file
    """

    if not os.path.exists(os.environ['HOME'] + "/sdkcpc/resources"):
        os.makedirs(os.environ['HOME'] + "/sdkcpc/resources")
    if not os.path.exists(CDT):
        okMessage("Download 2cdt Software.... please wait..")
        with requests.get(URL_CDT, stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="") as raw:
                with open(os.environ['HOME'] + "/sdkcpc/resources/2cdt", 'wb') as output:
                    shutil.copyfileobj(raw, output)
        if sys.platform == "darwin" or sys.platform == "linux":
            chmod(CDT)


def downloadiDsk():
    """
    download idsk file

    Args:
        file (string): Path of file
    """

    if not os.path.exists(os.environ['HOME'] + "/sdkcpc/resources"):
        os.makedirs(os.environ['HOME'] + "/sdkcpc/resources")
    if not os.path.exists(iDSK):
        okMessage("Download iDSK Software Version 0.20.... please wait..")
        with requests.get(URL_IDSK, stream=True) as r:
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


def extractFileDSK(library, destiny):
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
            okMessage("extract image file: " + os.path.basename(destiny).strip())
        except OSError as err:
            print("Error to Copy the 8BP library to the sdkcpc project: " + str(err))
            sys.exit(1)
    else:
        okMessage("No exist 8BP library in sdkcpc project.")


def findWord(word_list, line):
    """
    Search a string for a list of words

    Args:
        line (string): path file image sdk library
        word_list (string): word list
    """
    for word in word_list:
        if word in line:
            return True


def findCommand8BP():
    """
    add files to dsk image

    Args:
        file (string): path file image sdk library

    """
    files = next(os.walk(os.getcwd()))[2]
    for file in files:
        file_split = os.path.splitext(file)
        file = file_split[0] + file_split[1]
        if file_split[1].upper() == ".BAS":
            with open(os.getcwd() + "/" + file) as f:
                result = [findWord(commands_8bp, line.upper()) for line in f.readlines()]
            if True in result:
                return True


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
        okMessage("Create image disk " + os.path.basename(file))
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
        subprocess.run([os.environ['HOME'] + "/sdkcpc/resources/iDSK", dsk, "-i", file, "-f", "-t", type_file],
                       stdout=FNULL, stderr=subprocess.STDOUT)
        add2File(os.getcwd() + "/.sdkcpc/.M4", os.path.basename(file))
    except OSError as err:
        errMessage(" Error Added file " + file + " to DSK: " + str(err))
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
                    okMessage("Add binary " + file + " to DSK")
                else:
                    addFileToDsk(file_add, dsk, "0")
                    okMessage("Add ascii " + file + " to DSK")
        else:
            if file_split[1].upper() != ".BAS":
                if is_binary(file_add):
                    addFileToDsk(file_add, dsk, "1")
                    okMessage("Add binary " + file + " to DSK")
                else:
                    addFileToDsk(file_add, dsk, "0")
                    okMessage("Add ascii " + file + " to DSK")


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
