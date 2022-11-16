import sys
import os
import re
import inquirer
import json
from inquirer import errors
import shutil
from datetime import datetime
import subprocess
import os.path
from os import path
from pathlib import Path
from rich.console import Console
from rich import print
from jinja2 import Environment, FileSystemLoader

from .about import *
from .validations import *
from rich.console import Console

console = Console()

PWD = os.getcwd() + "/"
MAKEFILE = "Project.cfg"


# Crea nuevo proyecto en la ruta actua.
#   @Param Nombre del Proyecto
def createNewProject():
    questions = [
        inquirer.Confirm("validate83", message="Validate 8:3 name format in files"),
        inquirer.Text("name_project", message="Project's name", validate=project_name_validation),
        inquirer.Text("description", message="Project description", default=""),
        inquirer.List("template", message="Select the example Bas template to create", choices=["BASIC", "8BP"],
                      default="BASIC"),
        inquirer.Text("author", message="Author's name", default="Alan Sugar"),
        inquirer.Confirm("concatenate", message="Concatenate Bas files", default=False)]

    answers_1 = inquirer.prompt(questions)

    if answers_1.get("validate83"):
        questions = [
            inquirer.Text("bas_file",
                          message="Bas file name (with extension)",
                          validate=bas_name_validation_yes)]
    else:
        questions = [
            inquirer.Text("bas_file",
                          message="Bas file name (with extension)",
                          validate=bas_name_validation_no)]

    answers_2 = inquirer.prompt(questions)

    questions = [
        inquirer.List("model.cpc",
                      message="Select CPC Model",
                      choices=["464", "664", "6128"], default="6128"),
        inquirer.Text("m4_ip",
                      message="IP M4 Board",
                      default="0.0.0.0",
                      validate=validate_ip)]

    answers_3 = inquirer.prompt(questions)

    questions = [
        inquirer.Confirm("creategit",
                         message="Do you want to create version control in the project (git software needed)"),
        inquirer.Confirm("vscodeopen",
                         message="Do you want to open the new Project with Visual Studio Code")]

    answers_4 = inquirer.prompt(questions)

    answers_1.update(answers_2)
    answers_1.update(answers_3)

    project = answers_1.get("name_project")
    project_path = PWD + answers_1.get("name_project")

    show_info("Create New Project " + project, "white")

    data = {"build": str(datetime.now()), "version": "1.0.0"}
    data.update(answers_1)

    # Create project folder
    os.makedirs(project_path)
    create_structure_project(project_path)
    json_string = json.dumps(data, indent=4)
    create_project_cfg(project_path + "/" + MAKEFILE, json_string)

    # create template bas file
    if answers_1.get("template") == "8BP":
        copy_resources(project_path + "/resources/8bp.dsk")
        create_template(data, "8bp.j2", project_path + "/src/" + answers_1.get("bas_file"))
    elif answers_1.get("template") == "BASIC":
        create_template(data, "basic.j2", project_path + "/src/" + answers_1.get("bas_file"))

    if answers_4.get("creategit"):
        console.print("[✔] Create Git Repository")
        gitInit(project_path)
    if answers_4.get("vscodeopen"):
        createVscode(project_path)
        openVscode(project_path)

    show_info(project + " project successfully created", "green")

    return True


# Cheque si el nombre de proyecto contiene espacios.
#   @Param Nombre del Proyecto
# def check_project_nomenclature(nameProject):
#     if nameProject.find(' ') != -1:
#         print("[red bold]The project name cannot contain spaces")
#         sys.exit(1)
#
#     if len(nameProject) > 8:
#         print("[red bold] The project name can only have a maximum of 8 characters.")
#         sys.exit(1)

def create_project_cfg(path, data):
    f = open(path, "w")
    f.write(data)
    f.close()


# Create template file
def create_template(data, template_name, file):
    j2_env = Environment(loader=FileSystemLoader(TEMPLATES), trim_blocks=True)
    with open(file, mode="w", encoding="utf-8") as message:
        message.write(j2_env.get_template(template_name).render(data))
    print("[✔] Create Template " + Path(file).stem + ".bas")


# Crea estructura del proyecto
def create_structure_project(project):
    for i in FOLDERS_PROJECT_NEW:
        if not os.path.isdir(project + "/" + i):
            os.makedirs(project + "/" + i)
            print("[✔] Create Folder ../" + i)


# Crea estructura vscode
def createVscode(project):
    try:
        shutil.copytree(APP_PATH + "/resources/vscode", project + "/.vscode")
        print("[✔] Create Vscode files.")
    except OSError as err:
        print("[red bold]" + str(err))
        sys.exit(1)


# Copia 8bp defauld
def copy_resources(project):
    try:
        shutil.copy(APP_PATH + "/resources/software/8bp.dsk", project)
        print("[✔] Copy example 8bp library.")
    except OSError as err:
        print("[red bold]" + str(err))
        sys.exit(1)


# Inicializacion repositorio GIT
def gitInit(project):
    FNULL = open(os.devnull, 'w')
    try:
        subprocess.call(['git', 'init', project], stdout=FNULL, stderr=subprocess.STDOUT)
    except OSError as err:
        print('[red bold][ERROR] The git command does not exist. ' + err)

    try:
        shutil.copy(APP_PATH + "/resources/gitignore", project + "/.gitignore")
        print("[✔] Create gitignore file.")
    except OSError as err:
        print("[bold red]" + err)
        sys.exit(1)


# Open Visual Studio Code
def openVscode(project):
    FNULL = open(os.devnull, 'w')
    try:
        subprocess.call(['code', project], stdout=FNULL, stderr=subprocess.STDOUT)
    except OSError as err:
        print('[yellow bold][WARNING] The Visual Studio Code does not exist. ' + err)
