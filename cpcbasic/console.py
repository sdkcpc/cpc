import os
import sys

from prompt_toolkit import PromptSession, print_formatted_text, HTML
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory

from cpcbasic.load import loadCommand


from cpcbasic.concat import concatCommand
from cpcbasic.make import makeCommand

from cpcbasic.machine import modelCommand
from cpcbasic.run import runCommand

from cpcbasic.save import saveCommand

from cpcbasic.cat import catCommand
from cpcbasic.common import *
from cpcbasic.about import headerAmstrad, aboutCommand
from cpcbasic.cls import clsCommand

session = PromptSession(history=FileHistory('~/.history_cpcbasic'))

sql_completer = WordCompleter(get_configuration()["COMMAND_LIST"], ignore_case=True)

style = Style.from_dict(
    {
        # Default style.
        "": "#ffff00"
    }
)


def consoleCommand():
    # Erase Screen
    clsCommand()
    print(os.getcwd())
    sessions = PromptSession(style=style, completer=sql_completer,
                             history=FileHistory(get_configuration()["FILE_HISTORY"]), cursor=CursorShape.BLOCK)

    # Show header is activated in config
    headerAmstrad()

    while True:
        try:
            command = sessions.prompt('', style=style, auto_suggest=AutoSuggestFromHistory())
        except KeyboardInterrupt:
            print_formatted_text(HTML('<yellow>GoodBye!!</yellow>'), style=style)
            sys.exit(1)
        except EOFError:
            break
        else:
            if command:
                command.split()
                if command.split()[0].upper() in get_configuration()["COMMAND_LIST"]:
                    if command.split()[0].upper() == "ABOUT":
                        aboutCommand()
                    elif command.split()[0].upper() == "CAT":
                        catCommand(False)
                    if command.split()[0].upper() == "CLS":
                        clsCommand()
                    elif command.split()[0].upper() == "CONCAT":
                        if countCommand(command.split(), 2):
                            file = command.split()[1]
                            concatCommand(file.replace('"', ''), False)
                    elif command.split()[0].upper() == "MAKE":
                        if len(command.split()) == 2:
                            file = command.split()[1]
                            file_split = os.path.splitext(file)
                            if file_split[1].upper() != ".DSK":
                                file = file + ".dsk"
                            updateConfigKey("files", "dsk", file.replace(" ", "_"))
                        makeCommand()
                    elif command.split()[0].upper() == "LOAD":
                        if len(command.split()) == 2:
                            file = command.split()[1].replace('"', '')
                        else:
                            file = ""
                        loadCommand(file, False)
                    elif command.split()[0].upper() == "MACHINE":
                        if countCommand(command.split(), 2):
                            file = command.split()[1]
                            modelCommand(file.replace('"', ''), False)
                    elif command.split()[0].upper() == "RUN":
                        if len(command.split()) == 3:
                            updateConfigKey("files", "dsk", command.split()[1].replace(" ", "_"))
                            runCommand(command.split()[1], command.split()[2], False)
                        elif len(command.split()) == 2:
                            updateConfigKey("files", "run", command.split()[1].replace(" ", "_"))
                            runCommand(command.split()[1], getModel(), False)
                        elif len(command.split()) == 1:
                            runCommand(getRun(), getModel(), False)
                    elif command.split()[0].upper() == "SAVE":
                        if countCommand(command.split(), 2):
                            file = command.split()[1]
                            if not isExist(file.replace('"', '')):
                                saveCommand(file.replace('"', ''), False)
                            else:
                                print_formatted_text(HTML('<red>File exists in this path</red>'), style=style)
                    elif command.split()[0].upper() == "CDT":
                        print_formatted_text(HTML('<white>Coming soon</white>'), style=style)
                    print_formatted_text(HTML('<yellow>Ready</yellow>'), style=style)
                else:
                    print_formatted_text(HTML('<yellow>Syntax error\nReady</yellow>'), style=style)


if __name__ == '__main__':
    consoleCommand()


def countCommand(command, number):
    if len(command) == number:
        return True
    else:
        print_formatted_text(HTML('<yellow>Operand missing</yellow>'), style=style)
