import os
import sys

from prompt_toolkit import PromptSession, print_formatted_text, HTML
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory

from sdkcpc.load import loadCommand


from sdkcpc.concat import concatCommand
from sdkcpc.dsk import dskCommand

from sdkcpc.machine import modelCommand
from sdkcpc.run import runCommand

from sdkcpc.save import saveCommand

from sdkcpc.cat import catCommand
from sdkcpc.validator import *
from sdkcpc.about import headerAmstrad, aboutCommand
from sdkcpc.cls import clsCommand

session = PromptSession(history=FileHistory('~/.history_sdkcpc'))

commandActivate = True

command_list = ["ABOUT", "DSK", "MACHINE", "CAT", "RUN", "LOAD", "SAVE", "CLS", "CONCAT"]

sql_completer = WordCompleter(command_list, ignore_case=True)

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
                             history=FileHistory(os.getcwd() + '/.sdkcpc/.history'),
                             cursor=CursorShape.BLOCK)

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
                if command.split()[0].upper() in command_list:
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
                    elif command.split()[0].upper() == "DSK":
                        if len(command.split()) == 2:
                            file = command.split()[1]
                            file_split = os.path.splitext(file)
                            if file_split[1].upper() != ".DSK":
                                file = file + ".dsk"
                            updateConfigKey("files", "dsk", file.replace(" ", "_"))
                        dskCommand(False)
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
