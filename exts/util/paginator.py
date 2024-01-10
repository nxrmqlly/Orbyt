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
Pagination based on given list
"""

from typing import List, TypeVar, Optional, Union, Generic
import abc

import discord

from .constants import EMOJIS
from .views import BaseView
from bot import Orbyt

T = TypeVar("T")
BotT = TypeVar("BotT", bound="Orbyt")


class SendToPage(discord.ui.Modal):
    def __init__(self, paginator):
        super().__init__(title="Send to page", timeout=None)
        self.paginator: CustomPaginator = paginator

    to_page: str = discord.ui.TextInput(
        label="Page",
        style=discord.TextStyle.short,
        required=True,
        max_length=4,
    )

    async def on_submit(self, interaction: discord.Interaction):
        if not self.to_page.value.isdigit() or self.to_page.value == "0":
            return await interaction.response.send_message(
                content=f"{EMOJIS['no']} - Please Input a valid whole number as a page number!",
                ephemeral=True,
            )

        elif (
            int(self.to_page.value) > self.paginator.max_page
            or int(self.to_page.value) < 1
        ):
            return await interaction.response.send_message(
                content=f"{EMOJIS['no']} - Please Input a valid page number!",
                ephemeral=True,
            )

        self.paginator._skip_to_page(int(self.to_page.value) - 1)

        embed = await self.paginator.embed()
        return await interaction.response.edit_message(embed=embed, view=self.paginator)


class CustomPaginator(Generic[T, BotT], BaseView, abc.ABC):
    """
    Pagination based on given list

    Parameters
    -----------
    entries: :class:`List`
        The list of entries
    per_page: :class:`int`
        The number of entries per page
    clamp_pages: :class:`bool`
        Whether to clamp the pages
    target
        The target
    timeout: :class:`int`
        The timeout
    """

    def __init__(
        self,
        *,
        entries: List[T],
        per_page: int = 10,
        clamp_pages: bool = True,
        target,
        timeout=180,
    ) -> None:
        super().__init__(timeout=timeout, target=target)

        self.entries: List[T] = entries
        self.per_page: int = per_page
        self.clamp_pages: bool = clamp_pages

        self.target: Optional[BotT] = target
        self.author: Optional[Union[discord.User, discord.Member]] = target and (
            target.user if isinstance(target, discord.Interaction) else target.author
        )
        self.bot: Optional[BotT] = target and (
            target.client if isinstance(target, discord.Interaction) else target.bot
        )

        self._current_page_index = 0
        self.pages = [
            entries[i : i + per_page] for i in range(0, len(entries), per_page)
        ]
        self.page_counter.label = f"{self.current_page}/{self.total_pages}"

    @property
    def max_page(self) -> int:
        """The max page count."""
        return len(self.pages)

    @property
    def min_page(self) -> int:
        """The minimum page count."""
        return 1

    @property
    def current_page(self) -> int:
        """The current page index."""
        return self._current_page_index + 1

    @property
    def total_pages(self) -> int:
        """Returns the total number of pages."""
        return len(self.pages)

    def _update_counter(self):
        self.page_counter.label = f"{self.current_page}/{self.total_pages}"

    @abc.abstractmethod
    def format_page(self, entries: List[T], /) -> discord.Embed:
        """Formatting provided for embed for current page"""
        raise NotImplementedError("Must be implemented")

    async def embed(self) -> discord.Embed:
        """Get embed for current page"""
        return await discord.utils.maybe_coroutine(
            self.format_page, self.pages[self._current_page_index]
        )

    def _switch_page(self, count: int, /) -> None:
        self._current_page_index += count

        if self.clamp_pages:
            if count < 0:  # Going down
                if self._current_page_index < 0:
                    self._current_page_index = self.max_page - 1
            elif count > 0:  # Going up
                if self._current_page_index > self.max_page - 1:  # - 1 for indexing
                    self._current_page_index = 0
        self._update_counter()

        return

    def _skip_to_page(self, _index: int, /) -> None:
        self._current_page_index = _index
        self._update_counter()

    @discord.ui.button(
        emoji=EMOJIS["double_arrow_left"], style=discord.ButtonStyle.blurple
    )
    async def first_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Go to the first page"""

        self._skip_to_page(0)

        embed = await self.embed()
        return await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(emoji=EMOJIS["arrow_left"], style=discord.ButtonStyle.gray)
    async def previous_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Go to the previous page"""

        self._switch_page(-1)

        embed = await self.embed()
        return await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        label="Page/Pages", style=discord.ButtonStyle.gray, disabled=True
    )
    async def page_counter(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Show the current page and total pages"""
        await interaction.response.defer()

    @discord.ui.button(emoji=EMOJIS["arrow_right"], style=discord.ButtonStyle.gray)
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Go to the next page"""

        self._switch_page(1)

        embed = await self.embed()
        return await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        emoji=EMOJIS["double_arrow_right"], style=discord.ButtonStyle.blurple
    )
    async def last_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Go to the last page"""

        self._skip_to_page(self.max_page - 1)

        embed = await self.embed()
        return await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(emoji=EMOJIS["white_x"], style=discord.ButtonStyle.red, row=1)
    async def _stop(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> discord.InteractionMessage:
        """Stop the paginator"""

        await interaction.response.defer()
        await self.stop(interaction)

    @discord.ui.button(label="Skip to page", style=discord.ButtonStyle.blurple, row=1)
    async def skip_to_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Skip to a specific page"""

        modal = SendToPage(self)
        await interaction.response.send_modal(modal)
