from sys import version_info

from pyrogram import __version__ as __pyro_version__

__version_major__ = 0
__version_minor__ = 1
__version_micro__ = 5
__version_beta__ = 11

__version__ = "{}.{}.{}".format(__version_major__,
                                __version_minor__,
                                f"{__version_micro__}-beta.{__version_beta__}"
                                if __version_beta__ else __version_micro__)

__license__ = ("[GNU General Public License v3.0]"
               "(https://github.com/StarkGang/Fridays/blob/master/LICENSE)")

__copyright__ = "Copyright (C) 2020 by [StarkGang@Github](https://github.com/StarkGang)"

__python_version__ = "{}.{}.{}".format(version_info[0], version_info[1], version_info[2])
