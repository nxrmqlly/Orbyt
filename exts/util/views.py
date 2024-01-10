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

"""Boilerplate discord.ui.Views."""

from typing import TypeVar, Optional, Union
import re

import discord
from discord.ext import commands

from exts.util.constants import EMOJIS, HTTP_URL_REGEX

BotT = TypeVar("BotT", bound="commands.Bot")


def re_url_match(url: str):
    return re.fullmatch(HTTP_URL_REGEX, url)


def message_jump_button(url: str, to_where: str = "to Message"):
    if not re_url_match(url):
        raise ValueError("Invalid URL. Check `is_http` param.")

    return discord.ui.Button(
        label=f"Jump {to_where}", style=discord.ButtonStyle.link, url=url
    )


class BaseView(discord.ui.View):
    """
    Base View for other views.

    Parameters
    -----------
    timeout: :class:`int`
        Timeout in seconds
    target
        The target to use
    """

    def __init__(
        self,
        *,
        timeout=180,
        target: Optional[BotT] = None,
    ):
        self.target = target

        self.author: Optional[Union[discord.User, discord.Member]] = target and (
            target.user if isinstance(target, discord.Interaction) else target.author
        )

        self.ctx_msg = None

        super().__init__(timeout=timeout)

    async def stop(self, interaction: discord.Interaction):
        for child in self.children:
            child.disabled = True

        await interaction.edit_original_response(view=self)

        super().stop()

    async def interaction_check(
        self, interaction: discord.Interaction[discord.Client]
    ) -> bool:
        if self.target is None:
            return True

        assert self.author

        if self.author.id != interaction.user.id:
            return await interaction.response.send_message(
                f"{EMOJIS['no']} - Only the author can respond to this",
                ephemeral=True,
            )

        # chnl
        if (
            self.target.channel
            and interaction.channel
            and self.target.channel.id != interaction.channel.id
        ):
            return await interaction.response.send_message(
                f"{EMOJIS['no']} - This isn't in the right channel",
                ephemeral=True,
            )

        return True

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True

        if not self.target:
            return

        if isinstance(self.target, discord.Interaction):
            await self.target.edit_original_response(view=self)
        else:
            await self.ctx_msg.edit(view=self)


class ConfirmView(BaseView):
    """
    View for confirming or denying a request.

    Parameters
    -----------
    timeout: :class:`int`
        Timeout in seconds
    confirm_msg: :class:`str`
        The message to edit to when confirming
    deny_msg: :class:`str`
        The message to edit to when denying
    target
        The target to use
    """

    def __init__(
        self,
        timeout=180,
        confirm_msg: str = None,
        deny_msg: str = None,
        target: Optional[BotT] = None,
    ):
        super().__init__(timeout=timeout, target=target)

        self.value = None

        self.target = target
        self.confirm_msg = confirm_msg
        self.deny_msg = deny_msg

    @discord.ui.button(emoji=EMOJIS["white_tick"], style=discord.ButtonStyle.green)
    async def confirm_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.confirm_msg:
            await interaction.response.edit_message(content=self.confirm_msg, view=self)
        else:
            await interaction.response.defer()

        self.value = True
        await self.stop(interaction)

    @discord.ui.button(emoji=EMOJIS["white_x"], style=discord.ButtonStyle.red)
    async def deny_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.deny_msg:
            await interaction.response.edit_message(content=self.deny_msg, view=self)
        else:
            await interaction.response.defer()

        self.value = False
        await self.stop(interaction)
