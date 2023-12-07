"""
Pagination based on given list
"""

from typing import List, TypeVar, Optional, Union, Generic
import abc

import discord
from discord.interactions import Interaction
from discord.ext import commands

from bot import Orbyt
from .constants import EMOJIS
from .views import BaseView

T = TypeVar("T")
BotT = TypeVar("BotT", bound="commands.Bot")


class CustomPaginator(Generic[T, BotT], BaseView, abc.ABC):
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

    @property
    def max_page(self) -> int:
        """The max page count."""
        return len(self.pages)

    @property
    def min_page(self) -> int:
        """The min page count."""
        return 1

    @property
    def current_page(self) -> int:
        """The current page index."""
        return self._current_page_index + 1

    @property
    def total_pages(self) -> int:
        """Returns the total number of pages."""
        return len(self.pages)

    @abc.abstractmethod
    def format_page(self, entries: List[T], /) -> discord.Embed:
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

        return

    @discord.ui.button(emoji=EMOJIS["arrow_left"], style=discord.ButtonStyle.gray)
    async def previous_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Go to the previous page"""
        await interaction.response.defer()

        self._switch_page(-1)

        embed = await self.embed()
        return await interaction.edit_original_response(embed=embed)

    @discord.ui.button(emoji=EMOJIS["white_x"], style=discord.ButtonStyle.red)
    async def on_stop(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> discord.InteractionMessage:
        """Stop the paginator"""

        await interaction.response.defer()
        await self.stop(interaction)

    @discord.ui.button(emoji=EMOJIS["arrow_right"], style=discord.ButtonStyle.gray)
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Go to the next page"""
        await interaction.response.defer()

        self._switch_page(1)

        embed = await self.embed()
        return await interaction.edit_original_response(embed=embed)
