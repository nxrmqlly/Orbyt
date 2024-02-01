#
# This file is part of Orbyt. (https://github.com/nxmrqlly/orbyt)
# Copyright (c) 2023-present Ritam Das
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Global error handler
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot import Orbyt
from .util.constants import EMOJIS


class GlobalError(commands.Cog):
    def __init__(self, bot: Orbyt) -> None:
        self.bot = bot

    def cog_load(self) -> None:
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    def cog_unload(self):
        tree = self.bot.tree
        tree.on_error = self._old_tree_error

    @commands.Cog.listener("on_command_error")
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
        elif isinstance(error, commands.BadArgument):
            await ctx.send_help(ctx.command)
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"{EMOJIS['no']} - Only developers can use this command.")
        else:
            await ctx.send(
                f"⚠️ - Unexpected error, report to developers: ```py\n{str(error)}\n```"
            )
            raise error

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"⏰ - Command is on cooldown!\n```py\n{str(error)}\n```",
                ephemeral=True,
            )
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                f"{EMOJIS['no']} - You are missing permissions!\n```py\n{str(error)}\n```",
                ephemeral=True,
            )

        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                f"{EMOJIS['no']} - I am missing permissions!\n```py\n{str(error)}\n```",
                ephemeral=True,
            )

        elif isinstance(error, app_commands.NoPrivateMessage):
            await interaction.response.send_message(
                f"{EMOJIS['no']} - This command cannot be used in direct messages!",
                ephemeral=True,
            )

        elif isinstance(error, app_commands.MissingAnyRole):
            await interaction.response.send_message(
                f"{EMOJIS['no']} - You are missing required roles!\n```py\n{str(error)}\n```",
            )

        elif isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(
                f"{EMOJIS['no']} - Check failed! (Suggested to report to developers)\n```py\n{str(error)}\n```",
                ephemeral=True,
            )

        else:
            await interaction.response.send_message(
                f"⚠️ - Unknown Error, please report to developers:\n```py\n{str(error)}\n```",
                ephemeral=True,
            )
            raise error


async def setup(bot: Orbyt):
    await bot.add_cog(GlobalError(bot))
