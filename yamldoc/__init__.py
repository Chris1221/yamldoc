from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("yamldoc")
except PackageNotFoundError:
    __version__ = "unknown"

from .parser import parse_yaml, main
from .cli import cli
from .entries import *
