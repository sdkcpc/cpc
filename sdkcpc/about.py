from rich.console import Console


from .project import *

from . import __version__
from .common import *
from rich import print
from rich.console import Console

console = Console(width=100, color_system="windows", force_terminal=True)


# Show Banner in console
#   @Param text to show in banner
def about():
    ver = __version__
    build = readBuild()
    banner = """\n[bold white] ╔═╗╔╦╗╦╔═╔═╗╔═╗╔═╗ [bold white]┌─────────────┐[/]    [bold white]Created by: [bold green]© Destroyer - 2022[/]
[bold white] ╚═╗ ║║╠╩╗║  ╠═╝║   [bold white]│ [red bold]■■■[green] ■■■[blue] ■■■ [white]│[/]    [bold white]Github    : [bold green]https://github.com/sdkcpc/cpc.git[/]
[bold white] ╚═╝═╩╝╩ ╩╚═╝╩  ╚═╝ [bold white]│ [red bold]■■■[green] ■■■[blue] ■■■ [white]│[/]    [bold white]Version   : [bold green]{ver}[/]
[white] For Amstrad Basic[bold white]  └─────────────┘[/]    [bold white]Build     : [bold green]{build}[/]""".format(
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
