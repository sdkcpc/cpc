import os.path
import os.path
import getpass as gt
from rich import print
from rich.table import Table
from .validator import *
from .about import *


def concatCommand(file):
    """Update config with file to concat"""

    # update concat field
    updateConfigKey("files", "concat", file)
    print("[✔] The file to concatenate is now " + file)
