#!/usr/bin/python

import sys
import os
import re
import inquirer
from inquirer import errors
import shutil
from datetime import datetime
import subprocess
import os.path
from os import path
from rich.console import Console
from rich import print
from jinja2 import Environment, FileSystemLoader
from .common import *
from .validations import *
from rich.console import Console

console = Console(width=80, color_system="windows", force_terminal=True)


# Crea nuevo proyecto en la ruta actua.
#   @Param Nombre del Proyecto
def createNewProject(nameProject, template):
    questions = [
        inquirer.Confirm("validate83", message="Validate 8:3 name format in files")]
    answers_1 = inquirer.prompt(questions)

    if answers_1.get("validate83"):
        questions = [
            inquirer.Text("name_project",
                          message="Project's name",
                          validate=project_name_validation_yes)]
    else:
        questions = [
            inquirer.Text("name_project",
                          message="Project's names",
                          validate=project_name_validation_no)]

    answers_2 = inquirer.prompt(questions)

    questions = [
        inquirer.Text("description",
                      message="Project description",
                      default=""),
        inquirer.List("template",
                      message="Select the example Bas template to create",
                      choices=["BASIC", "8BP"], default="BASIC"),
        inquirer.Text("author",
                      message="Author's name",
                      default="Alan Sugar"),
        inquirer.Confirm("concatenate", message="Concatenate Bas files",
                         default=False)]
    answers_3 = inquirer.prompt(questions)

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

    answers_4 = inquirer.prompt(questions)

    questions = [
        inquirer.List("model.cpc",
                      message="Select CPC Model",
                      choices=["464", "664", "6128"], default="6128"),
        inquirer.Text("m4_ip",
                      message="IP M4 Board",
                      default="0.0.0.0",
                      validate=validate_ip),
        inquirer.List("creategit",
                      message="Do you want to create version control in the project (git software needed)?",
                      choices=["Yes", "No"], default="Yes"),
        inquirer.List("creategit",
                      message="Do you want to create version control in the project (git software needed)?",
                      choices=["Yes", "No"], default="Yes"),
        inquirer.List("vscodeopen", message="Do you want to open the new Project with Visual Studio Code?",
                      choices=["Yes", "No"], default="Yes"),
    ]

    answers_5 = inquirer.prompt(questions)

    # check nomenclature (spaces, 8:3 file)
    check_project_nomenclature(nameProject)

    # Creamos estructura del proyectod

    show_info("Create New Project " + nameProject, "white")

    data = {"project_name": nameProject, "compilation": str(datetime.now()), "template": template}

    if not path.exists(PWD + "/" + nameProject):

        # Create project folder
        os.makedirs(PWD + "/" + nameProject)

        # Create estructure project for template
        create_structure_project(nameProject, template)

        # create template makefile
        data = {"project_name": nameProject, "compilation": str(datetime.now()), "template": template}
        create_template(data, "project.j2", PWD + nameProject + "/" + MAKEFILE)

        # create template bas file
        if template == "8BP":
            copy_resources(PWD + nameProject + "/resources/8bp.dsk")
            create_template(data, "8bp.j2", PWD + nameProject + "/src/" + nameProject + ".bas")
        elif template == "BASIC":
            create_template(data, "basic.j2", PWD + nameProject + "/src/" + nameProject + ".bas")

        # Create a Git Versions and Vscode files

        if answers["creategit"] == "Yes":
            console.print("[+] Create Git Repository")
            gitInit(nameProject)
        if answers["vscodeopen"] == "Yes":
            createVscode(nameProject)
            openVscode(nameProject)

        show_info(nameProject + " project successfully created", "green")
    else:
        print("[red bold]\[ERROR] " + nameProject + " project exists on this path.")
        sys.exit(1)


# Cheque si el nombre de proyecto contiene espacios.
#   @Param Nombre del Proyecto
def check_project_nomenclature(nameProject):
    if nameProject.find(' ') != -1:
        print("[red bold]The project name cannot contain spaces")
        sys.exit(1)

    if len(nameProject) > 8:
        print("[red bold] The project name can only have a maximum of 8 characters.")
        sys.exit(1)


# Create template file
def create_template(data, template_name, file):
    j2_env = Environment(loader=FileSystemLoader(TEMPLATES), trim_blocks=True)
    with open(file, mode="w", encoding="utf-8") as message:
        message.write(j2_env.get_template(template_name).render(data))
    print("[+] Create Template " + file)


# Crea estructura del proyecto
def create_structure_project(project, template):
    if template == "BASIC":
        estructura = FOLDERS_PROJECT_NEW
    elif template == "8BP":
        estructura = FOLDERS_PROJECT_NEW

    for i in estructura:
        if not os.path.isdir(PWD + project + "/" + i):
            os.makedirs(PWD + project + "/" + i)
            print("[+] Create Folder " + project + "/" + i)


# Crea estructura vscode
def createVscode(project):
    try:
        shutil.copytree(APP_PATH + "/resources/vscode", PWD + project + "/.vscode")
        print("[+] Create Vscode files.")
    except OSError as err:
        print("[red bold]" + str(err))
        sys.exit(1)


# Copia 8bp defauld
def copy_resources(project):
    try:
        shutil.copy(APP_PATH + "/resources/software/8bp.dsk", project)
        print("[+] Copy example 8bp library.")
    except OSError as err:
        print("[red bold]" + str(err))
        sys.exit(1)


# Inicializacion repositorio GIT
def gitInit(project):
    FNULL = open(os.devnull, 'w')
    try:
        subprocess.call(['git', 'init', PWD + project], stdout=FNULL, stderr=subprocess.STDOUT)
    except:
        print('[red bold][ERROR] The git command does not exist.')

    try:
        shutil.copy(APP_PATH + "/resources/gitignore", PWD + project + "/.gitignore")
        print("[+] Create gitignore file.")
    except OSError as err:
        print("[bold red]" + err)
        sys.exit(1)


# Open Visual Studio Code
def openVscode(project):
    FNULL = open(os.devnull, 'w')
    try:
        subprocess.call(['code', PWD + project], stdout=FNULL, stderr=subprocess.STDOUT)
    except:
        print('[yellow bold][WARNING] The Visual Studio Code does not exist.')
