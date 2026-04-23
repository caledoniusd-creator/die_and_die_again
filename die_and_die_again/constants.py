
from functools import cache

from die_and_die_again.__version__ import __version__

__app_name__ = "Die & Die Again!"
__author__ = "Caledonius D."
__copyright__ = "©2026"

@cache
def app_info_string():
    return f"{__app_name__} v{__version__} {__copyright__} {__author__} "
