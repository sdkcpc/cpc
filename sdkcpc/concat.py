from .about import headerAmstrad
from .common import *


def concatCommand(file, activate):
    """Update config with file to concat"""

    # Show header is activated in config
    # if activate:
    #     headerAmstrad()
    # update concat field
    updateConfigKey("files", "concat", file)
    if not file:
        okMessage("Concatenate file is now disabled.")
    else:
        okMessage("The file to concatenate is now " + file)
