import shutil
from datetime import datetime

from cpcbasic.run import *
from cpcbasic.common import *


def initCommand(folder):
    """
    initialize project

    Args:
        folder (string): Template bas to create.

    """

    # if "/" in folder or "\\" in folder:
    if not validate_path(folder):
        folder = os.getcwd() + "/" + folder

    PROJECT_PATH = folder
    PROJECT_NAME = folder.rsplit('/', 1)[-1]
    PROJECT_CONFIG = PROJECT_PATH + "/config"

    # Check exist proyect folder
    if os.path.exists(PROJECT_PATH):
        print("A project already exists in this path.")
        sys.exit(1)

    # If the project does not exist, we create a folders
    for create in get_configuration()["PROJECT_FOLDERS"]:
        os.makedirs(PROJECT_PATH + "/" + create)

    # copy files (vscode and config)
    create_vscode_data(folder)
    copy_file(get_configuration()["LOCAL_RESOURCES_TEMPLATES"] + "config", PROJECT_CONFIG)

    # Create model file
    build = str(datetime.now())

    # update data in makefile
    updateConfigKey("compilation", "build", build, PROJECT_PATH)
    updateConfigKey("data", "project", PROJECT_NAME, PROJECT_PATH)
    updateConfigKey("data", "dsk", PROJECT_NAME + ".dsk", PROJECT_PATH)
    updateConfigKey("rvm", "run.file", "main.bas", PROJECT_PATH)

    # Create bas template
    data = {"project": PROJECT_NAME, "build": build, "version": "1.0.0"}
    create_template(data, "8bp.j2", PROJECT_PATH + "/src/main.bas")

    # Add library 8bp
    if not os.path.exists(PROJECT_PATH + "/assets/8bp/8bp.dsk"):
        copy_file(get_configuration()["LOCAL_RESOURCES_SOFTWARE"] + "8bp.dsk", PROJECT_PATH + "/assets/8bp/8bp.dsk")

    okMessage('Project CPCBasic create in ' + PROJECT_PATH)


def validate_path(filepath):
    """
    Validate path folder

    Args:
        filepath (string): Path of folder

    """
    pattern = ""
    if sys.platform == "darwin" or sys.platform == "linux":
        pattern = r"^\/([A-z0-9-_+]+\/)*([A-z0-9])"
    elif sys.platform == "win32" or sys.platform == "win64":
        pattern = r"/^(?:[\w]\:|\/)(\/[a-z_\-\s0-9\.]+)/i"

    if re.match(pattern, filepath):
        return True
    else:
        return False


def add_lines_file(file, text):
    """
    add lines to file

    Args:
        file (string): Path of file
        text (string): file text

    """
    fp = open(file, 'a')
    fp.write(text + "\n")
    fp.close()


def create_template(data, template, file):
    """
    create template bas

    Args:
        data (dict): data to template
        template (string): template name
        file (string): Name of the file to create

    """
    j2_env = Environment(loader=FileSystemLoader(get_configuration()["LOCAL_RESOURCES_TEMPLATES"]),
                         trim_blocks=True)
    with open(file, mode="w", encoding="utf-8") as message:
        message.write(j2_env.get_template(template).render(data))
        okMessage("Create Template Bas file.")


def create_vscode_data(folder):
    """
    create files vscode

    Args:
        folder (string): project folder

    """
    try:
        shutil.copytree(get_configuration()["LOCAL_RESOURCES_VSCODE"], folder + "/.vscode")
        okMessage("Create Vscode files.")
    except OSError as err:
        print("[red]" + str(err))
        sys.exit(1)


def copy_file(origen, destino):
    """
    create files vscode

    Args:
        origen (string): file source
        destino (string): file destination
        @param origen:
        @param destino:

    """
    try:
        shutil.copy(origen, destino)
        # okMessage("Copy config files.")
    except OSError as err:
        print("[red]" + str(err))
        sys.exit(1)
