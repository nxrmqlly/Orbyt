"""
    Information Related Commands
"""
import time

import discord
from discord import app_commands
from discord.ext import commands

from bot import Orbyt


class Info(commands.Cog):
    """Commands that give out information (WOW)"""

    def __init__(self, bot: Orbyt):
        self.bot: Orbyt = bot

    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction):
        """Returns the latency of the bot"""

        before = time.perf_counter()
        embed = discord.Embed(
            title="Pong!",
            description=f"""<:network:1080529982520037446> **API Latency:** {round(self.bot.latency * 1000)}ms""",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed)

        after = time.perf_counter()
        embed.description = (
            embed.description
            + f"\n<:network:1080529982520037446> **Round Trip Latency:** {round((after - before) * 1000)}ms"
        )

        await interaction.edit_original_response(embed=embed)


async def setup(bot: Orbyt):
    await bot.add_cog(Info(bot))
