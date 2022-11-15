import click
import os
from .validator import *
from .cat import *


@click.group()
def main():
    pass


@main.command()
def about():
    print('about')
    # TODO: show files in folder.


@main.command()
@click.argument('load', required=False)
def load(file):
    print(file)
    # TODO: open vscode, .


@main.command()
@click.argument('file', required=False)
def dsk(file):
    print(file)
    # TODO: generate dsk of cdt file in OUT folder.


@main.command()
@click.argument('file', required=False)
@click.option(',template', ',t', type=click.Choice(['BASIC', '8BP'], case_sensitive=False))
def save(file):
    print(file)
    # TODO: create file bas.


@main.command()
def cat():
    catCommand()


@main.command()
@click.argument('file', required=True)
def run(file):
    print(file)
    # TODO: FILE --> Run rvm con fichero file, si no hay fichero hacer cat.


@main.command()
@click.option('--model', '-m', type=click.Choice(['464', '664', '6128'], case_sensitive=False))
@click.option('--folder', '-f', required=False)
def init(model, folder):
    if not model:
        model = "6128"
    if not folder:
        folder = os.getcwd() + "/"

    print(folder, model)
    # TODO: FOLDER -> crear ruta si no existe
    # TODO: MODEL --> crear fichero .model y si es 464 archivo .cdt y .dsk con el modelo en carpeta .config


if __name__ == '__main__':
    main()
