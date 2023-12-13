"""A Quality-of-Life multipurpose Discord Bot.

Copyright (C) 2023 Ritam Das

Orbyt is a versatile, quality-of-life Discord Bot for Discord enthusiasts.

Author:
    Ritam Das

Repository:
    https://github.com/nxrmqlly/Orbyt
"""

__copyright__ = "Copyright (C) 2023 Ritam Das"
__title__ = "Orbyt"
__author__ = "Nxrmqlly (Ritam Das)"
__license__ = "AGPL v3"

import os
from asyncio import run

from termcolor import colored

from bot import Orbyt


async def _start():
    """
    Runs the function asynchronously to start the bot.

    Async function that starts the Bot.
    The bot is started by calling the `start` method of the bot instance.
    """
    async with Orbyt() as bot:
        await bot.start()


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    TITLE = """
  .oooooo.             .o8                       .   
 d8P'  `Y8b           "888                     .o8   
888      888 oooo d8b  888oooo.  oooo    ooo .o888oo      By Nxrmqlly
888      888 `888""8P  d88' `88b  `88.  .8'    888        https://github.com/nxrmqlly/Orbyt
888      888  888      888   888   `88..8'     888
`88b    d88'  888      888   888    `888'      888 .      Copyright (C) 2023 Ritam Das | AGPL v3
 `Y8bood8P'  d888b     `Y8bod8P'     .8'       "888" 
                                 .o..P'              
                                 `Y8P'               
"""
    print(
        colored(
            TITLE,
            color="light_magenta",
        )
    )

    run(_start())
