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
Limited-Time Commands (updated regularly)
"""

import random
from io import BytesIO
from functools import partial
from typing import Literal

import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont

from .util.constants import EMOJIS
from .util.views import BaseView
from .util.text_format import truncate


def image_cooldown(interaction: discord.Interaction):
    if interaction.user.id == interaction.client.owner_id:
        return None

    return app_commands.Cooldown(1, 120)


def christmas_card(author: str, to_user: str, color: str):
    messages = [
        "Merry Christmas and Happy New Year!",
        "Season's Greetings! And best wishes for the New Year.",
        "I hope your holiday is full of love, peace, and joy!",
        "Merry Christmas! And best wishes for 2024.",
        "Merry Christmas! Wishing you all the happiness in the world.",
        "Wishing you peace and joy all season long. Happy Holidays!",
    ]

    img = Image.open(f"./exts/assets/xmas_{color.lower()}.png")
    width, height = img.size

    to_user_font = ImageFont.truetype("./exts/assets/fonts/Kids Year.ttf", 40)
    author_font = ImageFont.truetype("./exts/assets/fonts/coolvetica-rg.otf", 30)
    greet_font = ImageFont.truetype("./exts/assets/fonts/coolvetica-rg.otf", 35)
    canvas = ImageDraw.Draw(img)

    author = truncate(f"@{author}", 32)

    to_user = truncate(f"@{to_user}", 26)
    to_user_width = canvas.textlength(to_user, font=to_user_font)

    greet = "“" + random.choice(messages) + "”"
    greet_width = canvas.textlength(greet, font=greet_font)

    canvas.text(  # to user
        (
            (width - to_user_width) / 2,
            (height / 2) - 22,
        ),
        to_user,
        (255, 255, 255),
        font=to_user_font,
    )

    canvas.text(  # Sent by author
        (
            115,
            798,
        ),
        author,
        (255, 255, 255),
        font=author_font,
        align="center",
    )

    canvas.text(  # Greet
        (
            (width - greet_width) / 2,
            (height / 2) + 70,
        ),
        greet,
        (255, 255, 255),
        font=greet_font,
    )

    _as_bytes = BytesIO()
    img.save(_as_bytes, format="PNG")
    _as_bytes.seek(0)

    img.close()

    return _as_bytes


class SendCardConfirm(BaseView):
    def __init__(
        self,
        *,
        card_img,
        author: discord.User,
        to_user: discord.User,
        timeout=180,
        target,
    ):
        self.card_img = card_img
        self.to_user = to_user
        self.author = author

        super().__init__(timeout=timeout, target=target)

    @discord.ui.button(
        label="Send to User",
        style=discord.ButtonStyle.green,
        emoji=EMOJIS["white_tick"],
    )
    async def send_to_user(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        try:
            festive_emojis = ["💖", "🎁", "🎅", "⛄", "🎄", "💝", "❄️"]
            emj = random.choice(festive_emojis)

            jump_view = discord.ui.View().add_item(
                discord.ui.Button(
                    label=f"Sent from {self.target.guild.name}",
                    style=discord.ButtonStyle.url,
                    url=self.target.channel.jump_url,
                    emoji=emj,
                )
            )

            self.card_img.seek(0)

            await self.to_user.send(
                f"{emj} - **@{self.author.name}** has sent you a card!\n"
                "||**Tip:** Use `/card christmas` in a mutual server to send a christmas card!||",
                file=discord.File(self.card_img, filename="card.png"),
                view=jump_view,
            )

        except discord.HTTPException as exc:
            if not exc.code == 50007:
                return

            self.card_img.seek(0)
            return await interaction.response.send_message(
                f"{EMOJIS['no']} - I cannot send the card to the user because they have DMs disabled.\nIf you are their friend, download this card and send it manually.",
                file=discord.File(self.card_img, filename="card.png"),
                ephemeral=True,
            )

        await interaction.response.send_message(
            content=f"{EMOJIS['yes']} - The card was send successfully to {self.to_user.mention}!",
            ephemeral=True,
        )

        await self.stop(self.target)


class Festive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    card = app_commands.Group(
        name="card", description="Send festive cards to users in the server!"
    )

    @card.command(name="christmas")
    @app_commands.checks.dynamic_cooldown(image_cooldown)
    async def christmas(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        color: Literal["Blue", "Green", "Purple", "Red"] = None,
    ):
        """Send a Christmas Card!

        Parameters
        -----------
        user : discord.Member
            The user to send the card to
        color : Literal['Blue', 'Green', 'Purple', 'Red']
            The color of the card. (default: Blue)
        """
        if user.bot:
            return await interaction.response.send_message(
                f"{EMOJIS['no']} - You cannot send a card to a bot.",
                ephemeral=True,
            )
        if user == interaction.user:
            return await interaction.response.send_message(
                "😔 - Well thats sad, but you cannot send cards to yourself.\n**Merry Christmas & Happy Holidays from Team Orbyt**",
                ephemeral=True,
            )

        author = str(interaction.user)
        to_user = str(user)

        gen_card = partial(
            christmas_card,
            author,
            to_user,
            color or "Blue",
        )

        card = await self.bot.loop.run_in_executor(None, gen_card)

        view = SendCardConfirm(
            card_img=card,
            author=interaction.user,
            to_user=user,
            timeout=60,
            target=interaction,
        )
        view.bot = self.bot

        await interaction.response.send_message(
            content="🎁 - Here is your card! Is this OK? (Preview)",
            file=discord.File(card, filename="card.png"),
            ephemeral=True,
            view=view,
        )

    @christmas.error
    async def on_xmas_err(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message("⏰ - " + str(error), ephemeral=True)


async def setup(bot):
    await bot.add_cog(Festive(bot))
