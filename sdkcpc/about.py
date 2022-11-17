import os

from . import __version__
from rich.console import Console

from .validator import getBuild, getHeader, getModel

console = Console()


def headerAmstrad():
    """
    show header Amstrad is activated in config

    """
    if getHeader().upper() == "ON":
        if getModel() == "6128":
            kbytes = "128"
            s = "s3"
            basic = "1.1"
            year = "1985"
        elif getModel() == "664":
            kbytes = "64"
            s = "v2"
            basic = "1.1"
            year = "1984"
        elif getModel() == "464":
            kbytes = "64"
            s = "s1"
            basic = "1.0"
            year = "1984"
        else:
            print("No model")

        info = """
 Amstrad {kbytes}K Microcomputer  ({s})
 ©1985 Amstrad Consumer Electronic plc
          and Locomotive Software Ltd.
      
 BASIC {basic}
    
 Ready
        """.format(kbytes=kbytes, basic=basic, s=s, year=year)
        print(info)


def aboutCommand():
    """
    show header about sdkcpc

    """
    ver = __version__
    build = readBuild()
    banner = """\n[bold white] ╔═╗╔╦╗╦╔═╔═╗╔═╗╔═╗ [bold white]┌─────────────┐[/][white]    Created by: © Destroyer - 2022[/]
[bold white] ╚═╗ ║║╠╩╗║  ╠═╝║   [bold white]│ [red bold]■■■[green] ■■■[blue] ■■■ [white]│[/]    Github    : https://github.com/sdkcpc/cpc.git[/]
[bold white] ╚═╝═╩╝╩ ╩╚═╝╩  ╚═╝ [bold white]│ [red bold]■■■[green] ■■■[blue] ■■■ [white]│[/]    Version   : {ver}[/]
[white] For Amstrad Basic[bold white]  └─────────────┘[/]    [bold]Build     : [bold]{build}[/]""".format(
        ver=ver, build=build)

    console.print(banner)
    console.print("")


def header():
    """
    Shows the application header

    """
    ver = __version__
    build = readBuild()
    banner = """
[bold white]╔═╗╔╦╗╦╔═╔═╗╔═╗╔═╗ [bold white]┌─────────────┐[/]
[bold white]╚═╗ ║║╠╩╗║  ╠═╝║   [bold white]│ [red bold]■■■[green] ■■■[blue] ■■■ [white]│[/]
[bold white]╚═╝═╩╝╩ ╩╚═╝╩  ╚═╝ [bold white]│ [red bold]■■■[green] ■■■[blue] ■■■ [white]│[/]
[white]For Amstrad Basic[bold white]  └─────────────┘[/]""".format(ver=ver, build=build)

    console.print(banner)
    console.print("")


def readBuild():
    """
    Read number build sdkcpc

    """
    file_path = os.path.dirname(os.path.abspath(__file__)) + "/resources/software/BUILD"
    if os.path.isfile(file_path):
        text_file = open(file_path, "r")
        data = text_file.read()
        text_file.close()
        return data
    return "Could not read the build"
