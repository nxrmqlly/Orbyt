"""Boilerplate code for Bot's root functionalities"""

import logging
from sys import version

import discord
import jishaku
from discord.ext import commands
from termcolor import colored

from util.text_format import spaced_padding, CustomFormatter
from config import DEBUG, DISCORD_TOKEN, DEBUG_BOT_TOKEN
from exts import EXTENSIONS


class Orbyt(commands.AutoShardedBot):
    """Base Class for the bot"""

    def __init__(self, *args, **kwargs):
        """Initialise the class from `super()`"""
        super().__init__(
            command_prefix=commands.when_mentioned_or("orbyt ", "Orbyt "),
            case_insensitive=True,
            strip_after_prefix=True,
            intents=discord.Intents.all(),
            owner_ids={767115163127906334},
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="pop music! v0.1.0 /ping",
            ),
            status="idle",
            *args,
            **kwargs,
        )

    async def setup_hook(self):
        """Set up logger and load extensions"""
        logger = logging.getLogger("discord")
        logger.setLevel(logging.DEBUG)
        fmt = "[{asctime}] [{levelname}] - {name}: {message}"
        date_fmt = "%d %b %Y %H:%M:%S"
        # Log to file
        f_formatter = logging.Formatter(fmt, date_fmt, "{")

        file_handler = logging.FileHandler(
            "./logs/discord.log", mode="w", encoding="utf-8"
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

        await self.load_extension("jishaku")

        loaded_exts = []
        for ext in EXTENSIONS:
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

    async def on_ready(self):
        """Called when the bot is ready"""

        basic_info = [
            f"{tag:<12}: {value}"
            for tag, value in [
                ("User", self.user),
                ("ID", self.user.id),
                ("Python", version),
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
            token=DEBUG_BOT_TOKEN if DEBUG else DISCORD_TOKEN,
            reconnect=True,
        )
