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
A Extension to help with tags
"""

from typing import List
from datetime import datetime

import discord
from sqlite3 import Row
from discord import app_commands
from discord.ext import commands
from discord.ui import TextInput, Modal


from bot import Orbyt
from .util.text_format import truncate
from .util.constants import EMOJIS, SECONDARY_COLOR, CONTRAST_COLOR
from .util.paginator import CustomPaginator


class TagPages(CustomPaginator[int, Orbyt]):
    def __init__(
        self,
        *,
        entries: List[int],
        per_page: int = 10,
        clamp_pages: bool = True,
        target,
        timeout=180,
        title: str = "Tags",
    ) -> None:
        self.title = title

        super().__init__(
            entries=entries,
            per_page=per_page,
            clamp_pages=clamp_pages,
            target=target,
            timeout=timeout,
        )

    async def format_page(self, entries: List[Row]) -> discord.Embed:
        embed = discord.Embed(
            title=self.title,
            color=SECONDARY_COLOR,
            description="\n".join(
                [
                    f"**{i+1}.** {discord.utils.escape_markdown(entry[0])} (ID: {entry[1]})"
                    for i, entry in enumerate(entries)
                ]
            ),
        )

        embed.set_footer(text=f"Page {self.current_page}/{self.total_pages}")

        return embed


class AddTag(Modal):
    """Add a tag"""

    def __init__(self, bot: Orbyt) -> None:
        self.bot = bot

        super().__init__(title="Add Tag")

    name = TextInput(
        label="Tag Name",
        placeholder="Enter the name of the tag",
        required=True,
        max_length=50,
    )
    content = TextInput(
        label="Tag Content",
        placeholder="Enter the content of the tag",
        required=True,
        style=discord.TextStyle.long,
        max_length=2000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as c:
            data = await c.fetchone(
                "SELECT content FROM tags WHERE name = LOWER($1) AND guild = $2",
                self.name.value,
                interaction.guild.id,
            )

            if data:
                return await interaction.response.send_message(
                    f"{EMOJIS['no']} - Tag `{self.name.value}` already exists",
                    ephemeral=True,
                )

            now_timestamp = round(discord.utils.utcnow().timestamp())

            await c.execute(
                "INSERT INTO tags (name, content, guild, author, created_at) VALUES (LOWER($1), $2, $3, $4, $5)",
                self.name.value,
                self.content.value,
                interaction.guild.id,
                interaction.user.id,
                now_timestamp,
            )

            em = discord.Embed(
                description=f"{discord.utils.escape_markdown(self.content.value)}",
                color=SECONDARY_COLOR,
            )
            em.add_field(
                name="Tag created at:",
                value=f"<t:{now_timestamp}:F> (<t:{now_timestamp}:R>)",
            )

            await interaction.response.send_message(
                f"{EMOJIS['yes']} - Tag `{self.name.value}` added", embed=em
            )


class EditTag(Modal):
    """Edit a tag"""

    def __init__(
        self,
        bot: Orbyt,
        query: str,
        _name: str,
        author_bypass: bool,
    ) -> None:
        self.bot = bot
        self.query = query

        self._name = _name
        self.author_bypass = author_bypass

        super().__init__(title="Edit Tag")

    new_content = TextInput(
        label="Tag Content",
        placeholder="Enter the content of the tag",
        required=True,
        style=discord.TextStyle.long,
        max_length=2000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as c:
            if self.author_bypass:  # True
                await c.execute(
                    self.query,
                    self.new_content.value,
                    self._name,
                    interaction.guild.id,
                )
            else:
                await c.execute(
                    self.query,
                    self.new_content.value,
                    self._name,
                    interaction.guild.id,
                    interaction.user.id,
                )

            embed = discord.Embed(
                description=discord.utils.escape_markdown(self.new_content.value),
                color=CONTRAST_COLOR,
            )

            await interaction.response.send_message(
                content=f"{EMOJIS['yes']} - Tag `{self._name}` edited {'[ Moderator Permissions ]' if self.author_bypass else ''}",
                embed=embed,
            )


class Tags(commands.GroupCog, name="tag"):
    def __init__(self, bot: Orbyt):
        self.bot = bot

    def bypass_query(self, interaction: discord.Interaction):
        author_bypass = (
            interaction.user.guild_permissions.manage_guild
            or interaction.user.guild_permissions.manage_messages
            or interaction.user.id == self.bot.owner_id
        )

        finished_query = "AND author = $3" if not author_bypass else ""

        return [author_bypass, finished_query]

    @app_commands.command(name="add")
    async def tag_add(self, interaction: discord.Interaction):
        """Add a tag to the server (Run in Modal)"""
        modal = AddTag(self.bot)
        await interaction.response.send_modal(modal)

    @app_commands.command(name="view")
    async def tag_view(
        self, interaction: discord.Interaction, name: str, raw: bool = False
    ):
        """View a tag

        Parameters
        -----------

        name: str
            The name of the tag to view
        raw: Optional[bool]
            Whether to display the content of the tag without markdown
        """

        async with self.bot.pool.acquire() as c:
            data = await c.fetchone(
                "SELECT content FROM tags WHERE name = LOWER($1) AND guild = $2",
                name,
                interaction.guild.id,
            )

            # tag exists?
            if not data:
                return await interaction.response.send_message(
                    f"{EMOJIS['no']} - Tag `{name}` not found", ephemeral=True
                )

        if raw:
            content = discord.utils.escape_markdown(data[0])
        else:
            content = data[0]

        await interaction.response.send_message(
            content=discord.utils.escape_mentions(content)
        )

    @app_commands.command(name="remove")
    async def tag_remove(self, interaction: discord.Interaction, name: str):
        """Remove a tag from the server

        Parameters
        -----------
        name: str
            The name of the tag to delete
        """

        # check if user has manage_guild or manage_messages permssion or is bot owner
        bypass = self.bypass_query(interaction)
        author_bypass = bypass[0]

        async with self.bot.pool.acquire() as c:
            data = await c.fetchone(
                "SELECT content, author FROM tags WHERE name = LOWER($1) AND guild = $2",
                name,
                interaction.guild.id,
            )

            # if tag exists
            if not data:
                return await interaction.response.send_message(
                    f"{EMOJIS['no']} - Tag `{name}` not found", ephemeral=True
                )

            # check if user can delete tag + return
            if not author_bypass and (data[1] != interaction.user.id):
                return await interaction.response.send_message(
                    f"{EMOJIS['no']} - You can only remove your own tags",
                    ephemeral=True,
                )

        query = f"DELETE FROM tags WHERE name = LOWER($1) AND guild = $2 {bypass[1]}"

        if author_bypass:  # if not author but mod
            await c.execute(query, name, interaction.guild.id)
        else:  # if author
            await c.execute(query, name, interaction.guild.id, interaction.user.id)

        await interaction.response.send_message(
            f"{EMOJIS['yes']} - Tag `{name}` removed {'[ Moderator Permission ]' if author_bypass else ''}",
        )

    @app_commands.command(name="list")
    async def tag_list(self, interaction: discord.Interaction):
        """View all tags of the server"""

        async with self.bot.pool.acquire() as c:
            data = await c.fetchall(
                "SELECT name, id FROM tags WHERE guild = $1",
                interaction.guild.id,
            )

            if not data:
                return await interaction.response.send_message(
                    f"{EMOJIS['no']} - No tags found", ephemeral=True
                )

            view = TagPages(
                clamp_pages=True,
                timeout=60,
                entries=data,
                target=interaction,
                title=f"Tags in {interaction.guild.name}",
            )

            embed = await view.embed()
            await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="edit")
    async def tag_edit(self, interaction: discord.Interaction, name: str):
        """Edit a Tag

        Parameters
        -----------
        name : str
            The name of the tag to edit
        """

        bypass = self.bypass_query(interaction)
        author_bypass = bypass[0]

        async with self.bot.pool.acquire() as c:
            data = await c.fetchone(
                "SELECT content, author FROM tags WHERE name = LOWER($1) AND guild = $2",
                name,
                interaction.guild.id,
            )

            # tag exists?
            if not data:
                return await interaction.response.send_message(
                    f"{EMOJIS['no']} - Tag `{name}` not found", ephemeral=True
                )

            # check for tag owner or mod perms
            if not author_bypass and (data[1] != interaction.user.id):
                return await interaction.response.send_message(
                    f"{EMOJIS['no']} - You don't have permission to edit this tag",
                    ephemeral=True,
                )

        query = f"UPDATE tags SET content = $1 WHERE name = LOWER($2) AND guild = $3 {bypass[1]}"

        modal = EditTag(self.bot, query, name, author_bypass)

        await interaction.response.send_modal(modal)

    @app_commands.command(name="search")
    async def tag_search(self, interaction: discord.Interaction, query: str):
        """Search for a tag in the server

        Parameters
        -----------
        query : str
            The query by which to search for
        """

        async with self.bot.pool.acquire() as c:
            data = await c.fetchall(
                "SELECT name, id FROM tags WHERE name LIKE $1 AND guild = $2 ORDER BY name ASC LIMIT 25",
                f"%{query}%",
                interaction.guild.id,
            )

            if not data:
                return await interaction.response.send_message(
                    f"{EMOJIS['no']} - No tags found matching `{query}`",
                    ephemeral=True,
                )

            view = TagPages(
                clamp_pages=True,
                timeout=60,
                entries=data,
                target=interaction,
                title=f"Tags matching {query}",
            )
            emb = await view.embed()

            await interaction.response.send_message(embed=emb, view=view)

    @app_commands.command(name="info")
    async def tag_info(self, interaction: discord.Interaction, name: str):
        """View the info of a tag

        Parameters
        -----------
        name : str
            The name of the tag to view information about
        """

        async with self.bot.pool.acquire() as c:
            data = await c.fetchone(
                "SELECT author, created_at FROM tags WHERE name = LOWER($1) AND guild = $2",
                name,
                interaction.guild.id,
            )

            if not data:
                return await interaction.response.send_message(
                    f"{EMOJIS['no']} - Tag `{name}` not found", ephemeral=True
                )

            _created_at = datetime.fromtimestamp(data[1])

            embed = (
                discord.Embed(title=f"Tag: `{name}` Information", color=SECONDARY_COLOR)
                .add_field(
                    name="Author",
                    value=f"<@{data[0]}>",
                )
                .add_field(
                    name="Created At",
                    value=f"{discord.utils.format_dt(_created_at, 'F')} ({discord.utils.format_dt(_created_at, 'R')})",
                )
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="random")
    async def tag_random(self, interaction: discord.Interaction):
        """View a random tag from the server"""

        async with self.bot.pool.acquire() as c:
            data = await c.fetchone(
                "SELECT name, content FROM tags WHERE guild = $1 ORDER BY RANDOM() LIMIT 1",
                interaction.guild.id,
            )

            if not data:
                return await interaction.response.send_message(
                    f"{EMOJIS['no']} - No tags found", ephemeral=True
                )

            _content = f"{EMOJIS['dictionary']} - `{discord.utils.escape_mentions(data[0])}`\n\n{data[1]}"

            await interaction.response.send_message(content=truncate(_content, 2000))

    @app_commands.command(name="by-user")
    async def tag_user(self, interaction: discord.Interaction, user: discord.User):
        """View all tags of a user

        Parameters
        -----------
        user : discord.User
            The user to view the tags of
        """

        async with self.bot.pool.acquire() as c:
            data = await c.fetchall(
                "SELECT name, id FROM tags WHERE guild = $1 AND author = $2",
                interaction.guild.id,
                user.id,
            )

            if not data:
                return await interaction.response.send_message(
                    f"{EMOJIS['no']} - No tags found from @{str(user)}",
                    ephemeral=True,
                )

            view = TagPages(
                clamp_pages=True,
                timeout=60,
                entries=data,
                target=interaction,
                title=f"Tags from @{str(user)}",
            )
            emb = await view.embed()
            await interaction.response.send_message(embed=emb, view=view)


async def setup(bot: Orbyt):
    await bot.add_cog(Tags(bot))
