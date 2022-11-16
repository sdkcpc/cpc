
import os.path
from .dsk import *
from .project import *
from .validator import *

console = Console()

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
def runCommand(bas_file):
    """
    Execute bas in retrovirtualmachine

    Args:
        bas_file(string): Bas file to execute in RVM

    """
    download_retro_virtual_machine()
    dsk = os.getcwd() + "/OUT/" + isDSK()
    if not path.exists(dsk):
        print("An error occurred not exist ./OUT/" + isDSK())
        sys.exit(1)

    print("[✔] Version : " + isVersion())
    print("[✔] Build   : " + isBuild())
    print("[✔] Bas File: " + bas_file)
    print("[✔] Dsk File: " + isDSK())

    FNULL = open(os.devnull, 'w')
    try:
        # Variables for platform
        if sys.platform == "darwin":
            subprocess.Popen([RVM, "-i", dsk, "-b=cpc" + isModel(), "-c=RUN\"" + bas_file + "\n"], stdout=FNULL,
                             stderr=subprocess.STDOUT)
        elif sys.platform == "win32" or sys.platform == "win64":
            subprocess.run([RVM, "-i", dsk, "-b=cpc" + isModel(), "-c=RUN\"" + bas_file + "\n"], stdout=FNULL,
                           stderr=subprocess.STDOUT)
        elif sys.platform == "linux":
            subprocess.Popen([RVM, "-i", dsk, "-b=cpc" + isModel(), "-c=RUN\"" + bas_file + "\n"], stdout=FNULL,
                             stderr=subprocess.STDOUT)
        print("[✔] Execution Successfully")
    except OSError as err:
        print("[✔] An error occurred while running Retro Virtual Machine: \n" + str(err))


def download_retro_virtual_machine():
    """
    download RetroVirtualMachine file

    """

    if not os.path.exists(SOFTWARE_PATH):
        os.makedirs(SOFTWARE_PATH)
    if not os.path.exists(RVM):
        validateOK("Download Retro Virtual Machine.... please wait..")
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
