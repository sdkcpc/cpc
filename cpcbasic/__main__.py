import sys

import click
from cpcbasic.run import *
from cpcbasic.about import *
from cpcbasic.concat import *
from cpcbasic.common import *
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
def concat(file):
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid CPCBasic project.</red>'), style=style)
        sys.exit(1)
    concatCommand(file, True)

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
@click.option('--project', '-p', required=True)
def init(project):
    initCommand(project)


if __name__ == '__main__':
    main()
