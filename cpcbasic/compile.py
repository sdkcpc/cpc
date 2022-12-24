import os
import re
import subprocess
import sys

from cpcbasic.common import *
from prompt_toolkit.styles import Style

style = Style.from_dict({
    'red': '#ff0066',
    'green': '#44ff00',
    'yellow': '#ffff00',
    'blue': '#0000FF'
})
def compile():
    ejemplo_dir = os.getcwd() + "/src"
    regexbas = r'[A-Za-z0-9]*.(BAS|bas)'
    regexccz = r'[A-Za-z0-9]*.(ccz80|CCZ80)'
    for path_dir, dirs, ficheros in os.walk(ejemplo_dir):
        print(path_dir)
        for file in ficheros:
            print(file)
            if re.search(regexbas, file):
                makefile(os.getcwd() + "/src/"+file)
            elif re.search(regexccz, file):
                makeccz80(os.getcwd() + "/src/"+file)
            else:
                print("file desconocido, no hacemos nada")

def makefile(file):
    new_version = "dfasdf"
    new_compilation = "dsfasdf"
    file_name = os.path.basename(file)
    with open(file, "r") as inputs:
        with open(os.getcwd() + "/obj/" + file_name, "w", newline='\r\n') as output:
            output.write("1 ' Version: " + new_version + " -- Build: " + new_compilation + "\r")
            for line in inputs:
                if not line.strip("\n").startswith("1 '"):
                    output.write(line)
            output.write("\n")
        if find8BPCommand(file):
            if not validate_path(dataProject()["8bp"]["dsk"]):
                library8bp = os.getcwd() + "/" + dataProject()["8bp"]["dsk"]
            else:
                library8bp = dataProject()["8bp"]["dsk"]
            if os.path.exists(library8bp):
                print("extrac file")
            else:
                print("error")
                sys.exit(1)
        print("[+] convert to CPC file: " + file_name)

def makeccz80(file):
    print(file)

def makeimages():
    print("DFSAf")


def makedsk():
    print("makle")


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

def find8BPCommand(file):
    """
    find command 8bp in bas file

    Args:
        file (string): path file
    """
    COMMANDS_8BP = ['|3D', '|ANIMA', '|ANIMALL', '|AUTO', '|AUTOALL', '|COLAY', '|COLSP', '|COLSPALL',
                    '|LAYOUT',
                    '|LOCATESP', '|MAP2SP', '|MOVER', '|MOVERALL', 'MUSIC', '|MUSIC', '|PEEK', '|POKE', '|PRINTAT',
                    '|PRINTSP', '|PRINTSPALL', '|RINK', '|ROUTESP', '|ROUTEALL', '|SETLIMITS', '|SETUPSP',
                    '|UMAP']
    with open(file) as f:
        result = [findWord(COMMANDS_8BP, line.upper()) for line in f.readlines()]
    if True in result:
        return True


def extractFileDSK(library, destiny):
    """
    add files to dsk image

    Args:
        file (string): path file image sdk library

    """

    if os.path.exists(library):
        FNULL = open(os.devnull, 'w')

        try:
            subprocess.Popen([iDSK, library, "-g", destiny], stdout=FNULL, stderr=subprocess.STDOUT)
            okMessage("Extract image file: " + os.path.basename(destiny).strip())
        except OSError as err:
            print("Error to Copy the 8BP library to the cpcbasic project: " + str(err))
            sys.exit(1)
    else:
        okMessage("No exist 8BP library in cpcbasic project.")