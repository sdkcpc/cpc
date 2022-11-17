import click
from .cat import *
from .save import *
from .run import *
from .about import *
from .concat import *
from .cls import *
from .machine import *
from .load import *
from .validator import *
from .console import *
from .cdt import *


@click.group()
def main():
    pass


@main.command()
def about():
    aboutCommand()


@main.command()
def console():
    consoleCommand()


@main.command()
def cdt():
    cdtCommand(True)


@main.command()
@click.argument('file', required=False)
def dsk(file):
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid sdkcpc project.</red>'), style=style)
        sys.exit(1)
    if not file:
        file = os.path.basename(os.path.normpath(os.getcwd())) + ".dsk"
    file_split = os.path.splitext(file)
    if file_split[1].upper() != ".DSK":
        file = file + ".dsk"
    updateConfigKey("files", "dsk", file.replace(" ", "_"))
    dskCommand(True)


@main.command()
@click.argument('file', required=False)
def load(file):
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid sdkcpc project.</red>'), style=style)
        sys.exit(1)
    if not file:
        file = ""
    loadCommand(file, True)


@main.command()
@click.argument('file', required=True)
@click.option('--template', '-t', type=click.Choice(['BASIC', '8BP'], case_sensitive=False))
def save(file, template):
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid sdkcpc project.</red>'), style=style)
        sys.exit(1)
    if not template:
        template = "BASIC"
    saveCommand(file, True)


@main.command()
def cat():
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid sdkcpc project.</red>'), style=style)
        sys.exit(1)
    catCommand(True)


@main.command()
def cls():
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid sdkcpc project.</red>'), style=style)
        sys.exit(1)
    clsCommand()


@main.command()
@click.argument('file', required=True)
def concat(file):
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid sdkcpc project.</red>'), style=style)
        sys.exit(1)
    concatCommand(file, True)


@main.command()
@click.argument('model', required=True)
def machine(model):
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid sdkcpc project.</red>'), style=style)
        sys.exit(1)
    modelCommand(model, True)


@main.command()
@click.argument('file', required=False)
@click.option('--model', '-m', type=click.Choice(['464', '664', '6128'], case_sensitive=False))
def run(file, model):
    if not isSdkProject():
        print_formatted_text(HTML('<red>[X] The path is not a valid sdkcpc project.</red>'), style=style)
        sys.exit(1)
    if not file:
        file = getRun()
    if not model:
        model = getModel()
    runCommand(file, model, True)


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
