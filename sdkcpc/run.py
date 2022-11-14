import os
import os.path
from zipfile import ZipFile
from tqdm.auto import tqdm

from .project import *
from rich.console import Console

from .project import *

console = Console()

# GET PLATFORM
if sys.platform == "darwin":
    RETROVIRTUALMACHINE = MY_HOME + "/RetroVirtualMachine"
    URL = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "win32" or sys.platform == "win64":
    RETROVIRTUALMACHINE = MY_HOME + "/RetroVirtualMachine.exe"
    URL = "https://static.retrovm.org/release/beta1/windows/x86/RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "linux":
    RETROVIRTUALMACHINE = MY_HOME + "/RetroVirtualMachine"
    URL = "https://static.retrovm.org/release/beta1/linux/x64/RetroVirtualMachine.2.0.beta-1.r7.linux.x64.zip"


def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(path, mode)


def download_retro_virtual_machine():
    if not os.path.exists(MY_HOME):
        os.makedirs(MY_HOME)
    if not os.path.exists(RETROVIRTUALMACHINE):
        validateOK("Download Retro Virtual Machine.... please wait..")
        with requests.get(URL, stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="") as raw:
                with open(MY_HOME + "/rvm.zip", 'wb') as output:
                    shutil.copyfileobj(raw, output)
                    with ZipFile(MY_HOME + "/rvm.zip", "r") as zipObj:
                        zipObj.extractall(MY_HOME)
        os.remove(MY_HOME + "/rvm.zip")
        if sys.platform == "darwin" or sys.platform == "linux":
            make_executable(RETROVIRTUALMACHINE)


# Ejecuta retro virtual machine con el dsk asociado
def rvm():

    project_data = Get_data_project_dict()

    show_head("Run " + project_data.get("name_project").replace(" ", "_") + ".dsk in the Emulator", "white")
    validateAll()
    download_retro_virtual_machine()
    if not path.exists(PWD + project_data.get("name_project").replace(" ", "_") + ".dsk"):
        show_info("An error occurred not exist " + project_data.get("name_project").replace(" ", "_") + ".dsk", "red")
        sys.exit(1)
    DSK = PWD + project_data.get("name_project").replace(" ", "_") + ".dsk"
    validateOK("Version : " + project_data.get("version"))
    validateOK("Build   : " + project_data.get("build"))
    validateOK("Bas File: " + project_data.get("bas_file"))
    validateOK("Dsk File: " + project_data.get("name_project").replace(" ", "_") + ".dsk")

    FNULL = open(os.devnull, 'w')
    try:
        # Variables for platform
        if sys.platform == "darwin":
            retcode = subprocess.Popen([RETROVIRTUALMACHINE, "-i", DSK, "-b=cpc" + project_data.get("model.cpc"),
                                        "-c=RUN\"" + project_data.get("bas_file") + "\n"], stdout=FNULL,
                                       stderr=subprocess.STDOUT)
        elif sys.platform == "win32" or sys.platform == "win64":
            retcode = subprocess.run([RETROVIRTUALMACHINE, "-i", DSK, "-b=cpc" + project_data.get("model.cpc"),
                                      "-c=RUN\"" + project_data.get("bas_file") + "\n"])
        elif sys.platform == "linux":
            retcode = subprocess.Popen([RETROVIRTUALMACHINE, "-i", DSK, "-b=cpc" + project_data.get("model.cpc"),
                                        "-c=RUN\"" + project_data.get("bas_file") + "\n"], stdout=FNULL,
                                       stderr=subprocess.STDOUT)
        show_foot("Execution Successfully", "green")
        print()
    except:
        show_info("An error occurred while running Retro Virtual Machine.'", "red")
