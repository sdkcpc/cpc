import os

from . import __version__
from .common import *


def headerAmstrad():
    """
    show header Amstrad is activated in config

    """

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

    print_formatted_text(HTML('<yellow>' + info + '</yellow>'), style=style)


# print_formatted_text(HTML('<white>' + info + '</white>'), style=style)


def aboutCommand():
    """
    show header about amstradbasic

    """
    ver = __version__
    build = readBuild()

    print_formatted_text(HTML('<yellow>╔═╗╔╦╗╦╔═╔═╗╔═╗╔═╗ ┌─────────────┐  Created by: © Destroyer - 2022</yellow>'),
                         style=style)
    print_formatted_text(HTML(
        '<yellow>╚═╗ ║║╠╩╗║  ╠═╝║   │</yellow><red> ■■■ </red><green>■■■ </green><blue>■■■</blue><yellow> '
        '│  Github    : https://github.com/amstradbasic/cpc.git</yellow>'),
        style=style)
    print_formatted_text(HTML(
        '<yellow>╚═╝═╩╝╩ ╩╚═╝╩  ╚═╝ │</yellow><red> ■■■ </red><green>■■■ </green><blue>■■■</blue><yellow> '
        '│  Version   : ' + ver + '</yellow>'),
        style=style)
    print_formatted_text(HTML('<yellow>For Amstrad Basic  └─────────────┘  Build     : ' + build + '</yellow>'),
                         style=style)


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
    Read number build amstradbasic

    """
    file_path = get_configuration()["LOCAL_RESOURCES_SOFTWARE"] + "BUILD"
    if os.path.isfile(file_path):
        text_file = open(file_path, "r")
        data = text_file.read()
        text_file.close()
        return data
    return "Could not read the build"
