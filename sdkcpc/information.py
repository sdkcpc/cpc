import glob

from .project import *

import os

from rich import print

console = Console()
contador_files = 0


def info():
    project_data = Get_data_project_dict()
    show_head("Project validation", "white")
    validateAll()
    show_head("Project information", "white")
    # print("[*] ------------------------------------------------------------------------")
    print("[*] [blue bold]COMPILATION [/]------------------------------------------------------------")
    print("[*]   compilation: " + project_data.get("build"))
    print("[*]   version: " + project_data.get("version"))
    print("[*] [blue bold]GENERAL [/]----------------------------------------------------------------")
    print("[*]   name: " + project_data.get("name_project"))
    print("[*]   description: " + project_data.get("description"))
    print("[*]   template: " + project_data.get("template"))
    print("[*]   author: " + project_data.get("author"))
    print("[*] [blue bold]CONFIG [/]-----------------------------------------------------------------")
    if project_data.get("concatenate"):
        print("[*]   concatenate.bas.files: Yes")
    else:
        print("[*]   concatenate.bas.files: No")
    print("[*]   name.bas.file: " + project_data.get("bas_file"))
    print("[*] [blue bold]RETRO VIRTUAL MACHINE [/]--------------------------------------------------")
    print("[*]   model.cpc: " + project_data.get("model.cpc"))
    print("[*] [blue bold]M4 BOARD [/]---------------------------------------------------------------")
    print("[*]   ip: " + project_data.get("m4_ip"))
    print(" ")

    if project_data.get("template") == "8BP":
        info_files(FOLDERS_PROJECT_NEW)
    elif project_data.get("template") == "BASIC":
        info_files(FOLDERS_PROJECT_NEW)


def info_files(estructura):
    show_head("Project Files", "white")
    TOTAL_FILES = 0
    TOTAL_SIZE = 0
    for i in estructura:
        if not i == "resources":
            TOTAL_FILES = TOTAL_FILES + CountFilesFolderProject(i)
            print("[✔] [blue bold]" + i + " [/] (" + str(CountFilesFolderProject(i)) + " Files)")
            arr = next(os.walk(PWD + i))[2]
            if len(arr) == 0:
                TOTAL_SIZE = TOTAL_SIZE + 0
                print('{message: <18}'.format(message="[✔]  ....") + "[0 KB]")
            for x in range(0, len(arr)):
                TOTAL_SIZE = TOTAL_SIZE + int(GetKbytes(PWD + i + "/" + arr[x]))
                print('{message: <18}'.format(message="[✔]   " + arr[x]) + "[" + GetKbytes(
                    PWD + i + "/" + arr[x]) + " KB]")
    show_foot("Total " + str(TOTAL_FILES) + " files with a size of " + str(TOTAL_SIZE) + " KB", "green")


def GetKbytes(file):
    if int(f"{os.path.getsize(file) / float(1 << 10):,.0f}") == 0:
        return "1"
    else:
        return str(f"{os.path.getsize(file) / float(1 << 10):,.0f}")


# Get number of kbytes of folder
#   @Param folder project
def GetTotalKbytesFolder(folder):
    print("\n[yellow] files in " + folder + " (" + str(CountFilesFolderProject(folder)) + "): ")
    total_size = 0
    files = glob.glob(PWD + folder + "/*")
    contador = 0
    for f in files:
        if int(f"{os.path.getsize(f) / float(1 << 10):,.0f}") == 0:
            total_size = total_size + 1
            print("[yellow]  -" + os.path.basename(f) + " (1 KB)")
        else:
            total_size = total_size + int(f"{os.path.getsize(f) / float(1 << 10):,.0f}")
            print("[yellow]   -" + os.path.basename(f) + str(f"{os.path.getsize(f) / float(1 << 10):,.0f} KB"))
        contador += 1
    if contador == 0:
        print("[yellow]  -No files in folder")
        print("")

    # return total_size


# Count files in folder project
#   @Param folder project
def CountFilesFolderProject(folder):
    try:
        dir_path = r'' + PWD + "/" + folder
        count_files: int = 0
        # Iterate directory
        for path_files in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path_files)):
                count_files += 1
        return count_files
    except IOError:
        return 0
