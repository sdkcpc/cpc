import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from .save import *
from .cls import *
from .about import headerAmstrad
from .cat import *
from .about import *

session = PromptSession(history=FileHistory('~/.history'))

commandActivate = True

command_list = ["ABOUT", "CDT", "DSK", "MACHINE", "CAT", "RUN", "LOAD", "SAVE", "CLS", "CONCAT", "CLS"]

sql_completer = WordCompleter(command_list, ignore_case=True)


def consoleCommand():
    # Erase Screen
    clsCommand()

    sessions = PromptSession(completer=sql_completer, history=FileHistory(os.getcwd() + '/.sdkcpc/.history'),
                             cursor=CursorShape.BLOCK)
    # Show header is activated in config
    headerAmstrad()

    while True:
        try:
            command = sessions.prompt('', auto_suggest=AutoSuggestFromHistory())
        except KeyboardInterrupt:
            print("GoodBye!!")
            sys.exit(1)
        except EOFError:
            break
        else:
            if command:
                command.split()
                if command.split()[0].upper() in command_list:
                    if command.split()[0].upper() == "CLS":
                        clsCommand()
                    elif command.split()[0].upper() == "CAT":
                        catCommand(False)
                    elif command.split()[0].upper() == "ABOUT":
                        aboutCommand()
                    elif command.split()[0].upper() == "SAVE":
                        if countCommand(command.split(), 2):
                            saveCommand(command.split()[1], False)
                    print_formatted_text(HTML('<yellow>Ready</yellow>'), style=style)
                else:
                    print_formatted_text(HTML('<yellow>Syntax error\nReady</yellow>'), style=style)
    print('GoodBye!')


if __name__ == '__main__':
    console()


def countCommand(command, number):
    if len(command) == number:
        return True
    else:
        print_formatted_text(HTML('<yellow>Operand missing</yellow>'), style=style)
