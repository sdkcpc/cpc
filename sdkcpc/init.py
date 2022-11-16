import os.path
import shutil
import sys
from datetime import datetime
from .validator import *
from .ini import *
from jinja2 import Environment, FileSystemLoader


def initCommand(folder, model):
    """
    initialize project

    Args:
        file (string): Path of file
        folder (string): Template bas to create.

    """

    # Check exist proyect folder
    if os.path.exists(os.getcwd() + "/.sdkcpc"):
        print("A project already exists in this path.")
        sys.exit(1)
    else:
        os.mkdir(folder + "/.sdkcpc")
        print("[✔] Create config files.")

    # If the project does not exist, we create a folder
    if not os.path.exists(folder):
        os.mkdir(folder)

    # copy files (vscode and config)
    createVscode(folder)
    copyFile(os.path.dirname(os.path.abspath(__file__)) + "/resources/templates/config", folder + "/.sdkcpc/config")

    # Create model file
    build = str(datetime.now())
    updateConfigKey("rvm", "model", model)
    updateConfigKey("compilation", "build", build)

    # Create bas template
    data = {"project": os.path.basename(os.path.normpath(folder)), "build": build, "version": "1.0.0"}
    createTemplate(data, "basic.j2", folder + "/MAIN.BAS")
    print("[✔] Initialized SDKCPC folder in " + folder + ".sdkcpc")


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
        print("[✔] Create Template Bas file.")


def createVscode(folder):
    """
    create files vscode

    Args:
        folder (string): project folder

    """
    try:
        shutil.copytree(os.path.dirname(os.path.abspath(__file__)) + "/resources/vscode", folder + "/.vscode")
        print("[✔] Create Vscode files.")
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
        # print("[✔] Copy config files.")
    except OSError as err:
        print("[red]" + str(err))
        sys.exit(1)
