import os.path
import sys

from .make import *
from .validator import *

SOFTWARE_PATH = os.environ['HOME'] + "/sdkcpc/resources"
if sys.platform == "darwin":
    RVM = os.environ['HOME'] + "/sdkcpc/resources/RetroVirtualMachine"
    URL_RVM = "https://static.retrovm.org/release/beta1/windows/x86/" \
              "RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "win32" or sys.platform == "win64":
    RVM = SOFTWARE_PATH + "/RetroVirtualMachine.exe"
    URL_RVM = "https://static.retrovm.org/release/beta1/windows/x86/" \
              "RetroVirtualMachine.2.0.beta-1.r7.windows.x86.zip"
elif sys.platform == "linux":
    RVM = SOFTWARE_PATH + "/RetroVirtualMachine"
    URL_RVM = "https://static.retrovm.org/release/beta1/linux/x64/" \
              "RetroVirtualMachine.2.0.beta-1.r7.linux.x64.zip"


# Ejecuta retro virtual machine con el dsk asociado
def runCommand(bas_file, model, activate):
    """
    Execute bas in retrovirtualmachine

    Args:
        bas_file(string): Bas file to execute in RVM

    """

    # Show header is activated in config
    # if activate:
    #     headerAmstrad()

    # if not exist file exit
    if commandFileExist(bas_file):

        # update configfile
        updateConfigKey("files", "run", bas_file)

    download_retro_virtual_machine()
    dsk = os.getcwd() + "/OUT/" + getDSK()
    if path.exists(dsk):
        okMessage("Version : " + getVersion())
        okMessage("Build   : " + getBuild())
        okMessage("Bas File: " + bas_file)
        okMessage("Dsk File: " + getDSK())

        FNULL = open(os.devnull, 'w')
        try:
            # Variables for platform
            if sys.platform == "darwin":
                subprocess.Popen([RVM, "-i", dsk, "-b=cpc" + model, "-c=RUN\"" + bas_file + "\n"], stdout=FNULL,
                                 stderr=subprocess.STDOUT)
            elif sys.platform == "win32" or sys.platform == "win64":
                subprocess.run([RVM, "-i", dsk, "-b=cpc" + model, "-c=RUN\"" + bas_file + "\n"], stdout=FNULL,
                               stderr=subprocess.STDOUT)
            elif sys.platform == "linux":
                subprocess.Popen([RVM, "-i", dsk, "-b=cpc" + model, "-c=RUN\"" + bas_file + "\n"], stdout=FNULL,
                                 stderr=subprocess.STDOUT)
            okMessage("Execution Successfully")
        except OSError as err:
            errMessage("An error occurred while running Retro Virtual Machine: \n" + str(err))
    else:
        errMessage("An error occurred not exist ./OUT/" + getDSK())


def download_retro_virtual_machine():
    """
    download RetroVirtualMachine file

    """

    if not os.path.exists(SOFTWARE_PATH):
        os.makedirs(SOFTWARE_PATH)
    if not os.path.exists(RVM):
        print("[*] Download Retro Virtual Machine.... please wait..")
        with requests.get(URL_RVM, stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="") as raw:
                with open(SOFTWARE_PATH + "/rvm.zip", 'wb') as output:
                    shutil.copyfileobj(raw, output)
                    with ZipFile(SOFTWARE_PATH + "/rvm.zip", "r") as zipObj:
                        zipObj.extractall(SOFTWARE_PATH)
        os.remove(SOFTWARE_PATH + "/rvm.zip")
        if sys.platform == "darwin" or sys.platform == "linux":
            chmod(RVM)
