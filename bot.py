#
# This file is part of Orbyt. (https://github.com/nxmrqlly/orbyt)
# Copyright (c) 2023-present Ritam Das
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""Boilerplate code for Bot's root functionalities"""

import logging
import sys

import discord
import jishaku
import asqlite
from discord.ext import commands
from termcolor import colored

from logging.handlers import RotatingFileHandler
from exts.util.text_format import spaced_padding, CustomFormatter
from config import DEBUG, PROD_TOKEN, DEBUG_BOT_TOKEN


INITIAL_EXTENSIONS = [
    "exts.info",
    "exts.dev",
    "exts.tags",
    "exts.festive",
    "exts.embed",
    "exts.error",
]


class Orbyt(commands.AutoShardedBot):
    """Base Class for the bot"""

    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned,
            case_insensitive=True,
            strip_after_prefix=True,
            intents=discord.Intents.all() if DEBUG else intents,
            owner_id=767115163127906334,
            activity=discord.Activity(
                type=discord.ActivityType.custom,
                name="Orbyt",
                state="💫 Exploring new dimensions. /ping",
            ),
            status="idle",
            *args,
            **kwargs,
        )
        self._codeblock = "```"

    @property
    def db(self):
        return self.pool

    async def setup_hook(self):
        """Set up logger and load extensions"""

        ## ----- Logging ----- ##

        logger = logging.getLogger("discord")
        logger.setLevel(logging.INFO)
        fmt = "[{asctime}] [{levelname}] - {name}: {message}"
        date_fmt = "%H:%M:%S"
        # Log to file
        f_formatter = logging.Formatter(fmt, date_fmt, "{")

        file_handler = RotatingFileHandler(
            "./logs/discord.log",
            mode="w",
            encoding="utf-8",
            maxBytes=5 * 1024 * 1024,
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(f_formatter)

        # Log to console
        c_formatter = CustomFormatter(fmt, date_fmt, "{")

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(c_formatter)

        # Add & Finish up
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        ## ----- Database Setup ----- ##

        self.pool = await asqlite.create_pool("./db/orbyt.db")
        async with self.pool.acquire() as c:
            with open("./db/schema.sql") as f:
                await c.executescript(f.read())

        ## ----- Load Extensions ----- ##

        await self.load_extension("jishaku")

        loaded_exts = []
        for ext in INITIAL_EXTENSIONS:
            try:
                await self.load_extension(ext)
            except commands.ExtensionError as exc:
                print(colored(f"Failed to load extension {ext}: {exc}", "red"))
            else:
                loaded_exts.append(ext)

        print(
            colored(
                spaced_padding("Extensions", 52)
                + "\n| > "
                + "\n| > ".join(loaded_exts)
                + "\n",
                "light_blue",
            )
        )

    async def close(self):
        await self.pool.close()
        await super().close()

    async def on_ready(self):
        """Called when the bot is ready"""

        basic_info = [
            f"{tag:<12}: {value}"
            for tag, value in [
                ("User", self.user),
                ("ID", self.user.id),
                ("Python", sys.version),
                ("Discord.py", discord.__version__),
                ("Jishaku", jishaku.__version__),
                ("Guilds", len(self.guilds)),
                ("Shards", self.shard_count),
                ("Debug Mode", DEBUG),
            ]
        ]
        print(
            colored(
                "\n"
                + spaced_padding("Logged In", 52)
                + "\n| > "
                + "\n| > ".join(basic_info)
                + "\n",
                "cyan",
            )
        )

    async def start(self) -> None:
        """Asyncrously start the bot"""

        await super().start(
            token=DEBUG_BOT_TOKEN if DEBUG else PROD_TOKEN,
            reconnect=True,
        )
