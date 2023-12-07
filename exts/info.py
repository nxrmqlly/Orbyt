"""
Information Related Commands
"""
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from bot import Orbyt
from .util.constants import EMOJIS


class Info(commands.Cog):
    """Commands that give out information about a object"""

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

    info = app_commands.Group(name="info", description="Information of Discord Objects")

    @info.command(name="server")
    async def info_server(self, interaction: discord.Interaction):
        """Returns information about the server"""

        guild = interaction.guild

        gen_info = {
            "ID": guild.id,
            "Created": f"{discord.utils.format_dt(guild.created_at, 'f')} ({discord.utils.format_dt(guild.created_at, 'R')})",
            "Verification": f"{str(guild.verification_level).replace('_', ' ').replace('none', 'no').title()} Verification Level",
        }
        counts = {
            "Roles": len(guild.roles),
            "Channels": len(guild.channels),
            "Emojis": len(guild.emojis),
            "Stickers": len(guild.stickers),
        }
        membertypes = {
            "Humans": len([m for m in guild.members if not m.bot]),
            "Bots": len([m for m in guild.members if m.bot]),
            "Total": len(guild.members),
        }

        embed = (
            discord.Embed(title="ℹ️ Server Information", color=discord.Color.blurple())
            .add_field(
                name="🌐 General Info",
                value="\n".join([f"**{k}:** {v}" for k, v in gen_info.items()]),
            )
            .add_field(
                name="🔢 Counts",
                value="\n".join([f"**{k}:** {v}" for k, v in counts.items()]),
            )
            .add_field(
                name="<:booster_shine:995611491778711552> Boosts",
                value=f"**Boosters:** {guild.premium_subscription_count}"
                + "\n"
                + f"**Boost Level:** {guild.premium_tier or 'None'}",
            )
            .add_field(
                name="👥 Members",
                value="\n".join([f"**{k}:** {v}" for k, v in membertypes.items()]),
            )
            .add_field(
                name="<:owner_icon:995606433527779370> Owner",
                value=guild.owner.mention + "\n" + f"**ID:** {guild.owner_id}",
            )
        )
        if guild.icon:
            embed.set_author(name=guild.name, icon_url=guild.icon.url)
            embed.set_thumbnail(url=guild.icon.url)
        else:
            embed.set_author(name=guild.name)

        guild_icon_view = discord.ui.View().add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.url, label="Server Icon", url=guild.icon.url
            )
        )
        await interaction.response.send_message(embed=embed, view=guild_icon_view)

    @info.command(name="user")
    async def info_user(
        self, interaction: discord.Interaction, user: Optional[discord.Member]
    ):
        """Returns information about the user

        Parameters
        -----------

            user: discord.Member:
                The user to get information about
        """

        # TODO: Make more features LOL

        if not user:
            user = interaction.user

        basic_info = {
            "ID": user.id,
            "Username": user.name,
            "Display Name": user.display_name
            if not user.display_name == user.name
            else EMOJIS["no"],
            "Discriminator": user.discriminator or "None",
            "Created": f"{discord.utils.format_dt(user.created_at, 'f')} ({discord.utils.format_dt(user.created_at, 'R')})",
            "Joined": f"{discord.utils.format_dt(user.joined_at, 'f')} ({discord.utils.format_dt(user.joined_at, 'R')})",
            "Is Owner?": EMOJIS["yes" if interaction.guild.owner == user else "no"],
            "Is Bot?": EMOJIS["yes" if user.bot else "no"],
        }

        embed = discord.Embed(
            title="ℹ️ User Information",
            color=user.accent_color or discord.Color.blurple(),
        ).add_field(
            name="👤 Basic Info",
            value="\n".join(
                [f"**{k}:** {v}" for k, v in basic_info.items()],
            ),
        )

        if user.avatar:
            embed.set_author(name=user.name, icon_url=user.avatar.url)
            embed.set_thumbnail(url=user.avatar.url)
        else:
            embed.set_author(name=user.name)

        await interaction.response.send_message(embed=embed)


async def setup(bot: Orbyt):
    await bot.add_cog(Info(bot))
