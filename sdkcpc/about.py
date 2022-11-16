from . import __version__
from .common import *
from rich.console import Console

console = Console()


# Show Banner in console
#   @Param text to show in banner
def aboutCommand():
    ver = __version__
    build = readBuild()
    banner = """\n[bold white] ╔═╗╔╦╗╦╔═╔═╗╔═╗╔═╗ [bold white]┌─────────────┐[/][white]    Created by: © Destroyer - 2022[/]
[bold white] ╚═╗ ║║╠╩╗║  ╠═╝║   [bold white]│ [red bold]■■■[green] ■■■[blue] ■■■ [white]│[/]    Github    : https://github.com/sdkcpc/cpc.git[/]
[bold white] ╚═╝═╩╝╩ ╩╚═╝╩  ╚═╝ [bold white]│ [red bold]■■■[green] ■■■[blue] ■■■ [white]│[/]    Version   : {ver}[/]
[white] For Amstrad Basic[bold white]  └─────────────┘[/]    [bold]Build     : [bold]{build}[/]""".format(
        ver=ver, build=build)

    console.print(banner)
    console.print("")


def head():
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
    file_path = os.path.dirname(os.path.abspath(__file__)) + "/resources/software/BUILD"
    if os.path.isfile(file_path):
        text_file = open(file_path, "r")
        data = text_file.read()
        text_file.close()
        return data
    return "Could not read the build"
