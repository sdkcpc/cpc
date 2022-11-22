import os.path
import shutil
import sys
from datetime import datetime
import re

from .about import headerAmstrad
from .validator import *
from jinja2 import Environment, FileSystemLoader


def initCommand(folder, model):
    """
    initialize project

    Args:
        file (string): Path of file
        folder (string): Template bas to create.

    """

    # if "/" in folder or "\\" in folder:
    if not validatePath(folder):
        folder = os.getcwd() + "/" + folder

    # Check exist proyect folder
    if os.path.exists(folder + "/.sdkcpc"):
        print("A project already exists in this path.")
        sys.exit(1)

    # If the project does not exist, we create a folder
    if not os.path.exists(folder + "/.sdkcpc"):
        os.makedirs(folder + "/.sdkcpc")

    # copy files (vscode and config)
    createVscode(folder)
    copyFile(os.path.dirname(os.path.abspath(__file__)) + "/resources/templates/config", folder + "/.sdkcpc/config")

    # Create model file
    build = str(datetime.now())
    updateConfigKey("rvm", "model", model, folder + "/.sdkcpc")
    updateConfigKey("compilation", "build", build, folder + "/.sdkcpc")

    # Create bas template
    data = {"project": os.path.basename(os.path.normpath(folder)), "build": build, "version": "1.0.0"}
    createTemplate(data, "8bp.j2", folder + "/MAIN.BAS")

    # Add library 8bp
    if not os.path.exists(folder + "/.sdkcpc/8bp.dsk"):
        copyFile(os.path.dirname(os.path.abspath(__file__)) + "/resources/software/8bp.dsk",
                 folder + "/.sdkcpc/8bp.dsk")

    # Create file
    createFile(folder + "/.sdkcpc/CDT.example", "nombre a mostrar,direccion de carga,direccion de ejecucion,"
                                                "archivo a cargar,nombre del cdt\nMAIN,,,MAIN.BAS\n")

    # Show header is activated in config
    # headerAmstrad()

    okMessage("Initialized SDKCPC folder in " + folder + "/.sdkcpc")


def validatePath(filePath):
    """
    Validate path folder

    Args:
        filePath (string): Path of folder

    """
    pattern = ""
    if sys.platform == "darwin" or sys.platform == "linux":
        pattern = r"^\/([A-z0-9-_+]+\/)*([A-z0-9])"
    elif sys.platform == "win32" or sys.platform == "win64":
        pattern = r"/^(?:[\w]\:|\/)(\/[a-z_\-\s0-9\.]+)/i"

    if re.match(pattern, filePath):
        return True
    else:
        return False


def createFile(file, text):
    """
    create file

    Args:
        file (string): Path of file
        text (string): file text

    """
    fp = open(file, 'w')
    fp.write(text)
    fp.close()


def add2File(file, text):
    """
    add lines to file

    Args:
        file (string): Path of file
        text (string): file text

    """
    fp = open(file, 'a')
    fp.write(text + "\n")
    fp.close()


def createTemplate(data, template, file):
    """
    create template bas

    Args:
        data (dict): data to template
        template (string): template name
        file (string): Name of the file to create

    """
    j2_env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__)) + "/resources/templates/"),
                         trim_blocks=True)
    with open(file, mode="w", encoding="utf-8") as message:
        message.write(j2_env.get_template(template).render(data))
        okMessage("Create Template Bas file.")


def createVscode(folder):
    """
    create files vscode

    Args:
        folder (string): project folder

    """
    try:
        shutil.copytree(os.path.dirname(os.path.abspath(__file__)) + "/resources/vscode", folder + "/.vscode")
        okMessage("Create Vscode files.")
    except OSError as err:
        print("[red]" + str(err))
        sys.exit(1)


def copyFile(origen, destino):
    """
    create files vscode

    Args:
        origen (string): file source
        destino (string): file destination

    """
    try:
        shutil.copy(origen, destino)
        # okMessage("Copy config files.")
    except OSError as err:
        print("[red]" + str(err))
        sys.exit(1)
