import sys
from .cls import *
from .about import *
from os import system, name

from sdkcpc.validator import updateConfigKey


def modelCommand(model):
    """
    change model cpc

    """
    if model == "6128" or model == "664" or model == "464":
        # update model field
        updateConfigKey("rvm", "model", model)
        clsCommand()
        headerAmstrad()
        print("[✔] The CPC model is now " + model)
    else:
        print("[X] The model is not supported. Wouldn't it be that you want a Spectrum?")
        sys.exit(1)

