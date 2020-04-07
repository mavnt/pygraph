import shutil

from .logging_utils import logging
from .pygraph import Graph

if shutil.which("dot") is None:
    logging.critical("dot binary not found !!!")
