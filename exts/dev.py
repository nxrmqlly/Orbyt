"""
Commands for developers only
"""


from typing import Optional, Literal

import discord
from discord.ext import commands

from bot import Orbyt
from .util.views import ConfirmView


class Developer(commands.Cog, command_attrs=dict(hidden=True)):
    """Hidden from users that are not owners"""

    def __init__(self, bot: Orbyt):
        self.bot: Orbyt = bot

    async def cog_before_invoke(self, ctx: commands.Context) -> bool:
        return ctx.author.id in self.bot.owner_ids

    @commands.group(name="dev", invoke_without_command=True)
    @commands.is_owner()
    async def dev(self, ctx: commands.Context):
        """Hidden developer only commands"""

        cmds = ", ".join([f"`{x.name}`" for x in self.dev.commands])
        await ctx.send(f"Available: {cmds}")

    @dev.command("load", aliases=["l"])
    async def load(self, ctx: commands.Context, *exts):
        """dev load <ext+>: Load ext

        Args:
            exts: Extensions to load
        """
        for ext in exts:
            try:
                await self.bot.load_extension(f"exts.{ext}")
                await ctx.send(f"📥 `exts.{ext}`")
            except commands.ExtensionError as e:
                await ctx.send(
                    f"Error loading {e.name}" + "\n" + f"```py\n{str(e)}\n```"
                )
                continue

    @dev.command("unload", aliases=["u"])
    async def unload(self, ctx: commands.Context, *exts):
        """dev unload <ext+>: Unload ext

        Args:
            exts: Extensions to unload"""
        for ext in exts:
            try:
                if ext == "developer":
                    continue
                await self.bot.unload_extension(f"exts.{ext}")
                await ctx.send(f"📤 `exts.{ext}`")
            except commands.ExtensionError as e:
                await ctx.send(
                    f"Error unloading {e.name}" + "\n" + f"```py\n{str(e)}\n```"
                )
                continue

    @dev.command("reload", aliases=["r"])
    async def reload(self, ctx: commands.Context, *exts):
        """dev reload <ext+>: Reload ext

        Args:
            exts: Extensions to reload"""
        for ext in exts:
            try:
                await self.bot.reload_extension(f"exts.{ext}")
                await ctx.send(f"🔄 `exts.{ext}`")
            except commands.ExtensionError as e:
                await ctx.send(
                    f"Error reloading {e.name}" + "\n" + f"```py\n{str(e)}\n```"
                )
                continue

    @commands.command()
    @commands.is_owner()
    async def sync(
        self,
        ctx,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        """Syncs App Commands

        sync -> global sync;
        sync ~ -> sync current guild;
        sync * -> copies all global app commands to guild;
        sync ^ -> clear commands from current guild + sync;
        sync id_1 id_2 -> syncs guilds with id 1 and 2;

        """
        await ctx.send("Syncing")
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            where = "globally" if spec is None else "to the current guild."

            await ctx.send(f"Synced {len(synced)} commands {where}")
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @commands.command(name="shutdown", aliases=["close"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shuts down the bot"""
        view = ConfirmView(
            timeout=20, confirm_msg="Shutting Down", deny_msg="Cancelled", target=ctx
        )
        await ctx.send("Are you sure you want to shutdown the bot?", view=view)
        await view.wait()

        if view.value:
            await ctx.send(":wave: - Goodbye.")
            await self.bot.close()


async def setup(bot: Orbyt):
    await bot.add_cog(Developer(bot))
