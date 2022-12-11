import sys
from amstradbasic.cls import *
from amstradbasic.about import *
from os import system, name

from amstradbasic.common import updateConfigKey, okMessage, errMessage


def modelCommand(model, activate):
    """
    change model cpc

    """

    # Show header is activated in config
    # if activate:
    #     headerAmstrad()

    if model == "6128" or model == "664" or model == "464":
        # update model field
        updateConfigKey("rvm", "model", model)
        clsCommand()
        # headerAmstrad()
        okMessage("The CPC model is now " + model)
    else:
        errMessage(" The model is not supported. Wouldn't it be that you want a Spectrum?")
