"""
A Quality-of-Life multipurpose Discord Bot.
Copyright (c) 2023-present Ritam Das

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Repository:
    https://github.com/nxrmqlly/Orbyt
"""

__copyright__ = "Copyright (C) 2023-present Ritam Das"
__title__ = "Orbyt"
__author__ = "Nxrmqlly (Ritam Das)"
__license__ = "AGPL v3"
__version__ = "1.3.0"

import os
from asyncio import run

from termcolor import colored

from bot import Orbyt
from exts.util.constants import ASCII_TITLE


async def _start():
    async with Orbyt() as bot:
        await bot.start()


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print(
        colored(
            ASCII_TITLE,
            color="light_magenta",
        )
    )

    run(_start())
