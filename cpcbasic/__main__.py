import sys

import click
from cpcbasic.cat import *
from cpcbasic.save import *
from cpcbasic.run import *
from cpcbasic.about import *
from cpcbasic.concat import *
from cpcbasic.cls import *
from cpcbasic.machine import *
from cpcbasic.load import *
from cpcbasic.common import *
from cpcbasic.console import *
from cpcbasic.init import validatePath
from cpcbasic.__init__ import __version__ as version

@click.group()
@click.version_option(version, '-v', '--version', is_flag=True, help="Show version Amstrad Basic")
def main():
    pass

@main.command()
def about():
    aboutCommand()


@main.command()
def console():
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid CPCBasic project.</red>'), style=style)
        sys.exit(1)
    consoleCommand()


@main.command()
@click.argument('file', required=False)
def make(file):
    cdtFile = ""
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid CPCBasic project.</red>'), style=style)
        sys.exit(1)
    if not file:
        if not getDSK():
            file = os.path.basename(os.path.normpath(os.getcwd())) + ".dsk"
            cdtFile = os.path.basename(os.path.normpath(os.getcwd())) + ".cdt"
        else:
            file = getDSK()
            cdtFile = getCDT()
    file_split = os.path.splitext(file)
    if file_split[1].upper() != ".DSK":
        cdtFile = file + ".cdt"
        file = file + ".dsk"
    else:
        cdtFile = file_split[0] + ".cdt"

    updateConfigKey("files", "dsk", file.replace(" ", "_"))
    updateConfigKey("files", "cdt", cdtFile.replace(" ", "_"))
    makeCommand()


@main.command()
@click.argument('file', required=False)
def load(file):
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid CPCBasic project.</red>'), style=style)
        sys.exit(1)
    if not file:
        file = ""
    loadCommand(file, True)


@main.command()
@click.argument('source', required=True)
@click.option('--template', '-t', type=click.Choice(['BASIC', '8BP'], case_sensitive=False))
def save(file, template):
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid CPCBasic project.</red>'), style=style)
        sys.exit(1)
    if not template:
        template = "BASIC"
    saveCommand(file, True)


@main.command()
def cat():
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid CPCBasic project.</red>'), style=style)
        sys.exit(1)
    catCommand(True)


@main.command()
def cls():
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid CPCBasic project.</red>'), style=style)
        sys.exit(1)
    clsCommand()


@main.command()
@click.argument('file', required=False)
def concat(file):
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid CPCBasic project.</red>'), style=style)
        sys.exit(1)
    concatCommand(file, True)


@main.command()
@click.argument('model', required=True)
def machine(model):
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid CPCBasic project.</red>'), style=style)
        sys.exit(1)
    modelCommand(model, True)


@main.command()
@click.argument('file', required=False)
@click.option('--model', '-m', type=click.Choice(['464', '664', '6128'], case_sensitive=False))
def run(file, model):
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid CPCBasic project.</red>'), style=style)
        sys.exit(1)
    if not model:
        model = getModel()
    if not file:
        if not getRun():
            errMessage("Bad command")
            sys.exit(0)
        else:
            file = getRun()
    runCommand(file.replace('"', ''), model, False)


@main.command()
@click.option('--model', '-m', type=click.Choice(['464', '664', '6128'], case_sensitive=False))
@click.option('--folder', '-f', required=False)
def init(model, folder):
    if not model:
        model = "6128"
    if not folder:
        folder = os.getcwd() + "/"

    initCommand(folder, model)


if __name__ == '__main__':
    main()
