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

"""Games."""

import json
from typing import Literal
from enum import Enum

import discord
import aiohttp
from discord.ui import Select
from discord import app_commands
from discord.ext import commands

from bot import Orbyt
from .util.constants import EMOJIS
from .util.views import BaseView


class Trivia:
    def __init__(self, question, options, correct_option):
        self.question: str = question
        self.options: list[str] = options
        self.correct_option: str = correct_option


class TriviaCategorySelect(Select):
    def __init__(self, categories: dict[int, str]):
        self.categories = categories

        options = []
        for k, v in categories.items():
            options.append(discord.SelectOption(label=v, value=k))

        super().__init__(
            placeholder="Select a category", min_values=1, max_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"{EMOJIS['yes']} - Selected **{self.categories[self.values[0]]}** category",
            ephemeral=True,
        )


class TriviaDifficultySelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Any", value=""),
            discord.SelectOption(label="Easy", value="easy"),
            discord.SelectOption(label="Medium", value="medium"),
            discord.SelectOption(label="Hard", value="hard"),
        ]
        super().__init__(
            placeholder="Select a difficulty",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        v = self.values[0] if self.values[0] else "Any"
        await interaction.response.send_message(
            f"{EMOJIS['yes']} - Selected **{v}** difficulty", ephemeral=True
        )


class TriviaView(BaseView):
    def __init__(self, trivia: Trivia):
        self.original_message = self.target.message
        self.options = trivia.options
        self.correct_option = trivia.correct_option
        self.question = trivia.question

    async def common_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.correct_option == button.custom_id:
            await interaction.response.send_message(
                f"{EMOJIS['yes']} - Correct!", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"{EMOJIS['no']} - Wrong!", ephemeral=True
            )
        await interaction.followup.send()

        await self.stop(interaction)


class TriviaInit(BaseView):
    def __init__(self, categories, questions):
        self.categories = categories

        c_s = TriviaCategorySelect(categories)
        d_s = TriviaDifficultySelect()

    async def resolve_trivia_questions(
        self,
        category: int,
        difficulty: Literal["easy", "medium", "hard", ""],
        amount: int,
    ):
        async with aiohttp.ClientSession() as session:
            data = await session.get(
                f"https://opentdb.com/api.php",
                params={
                    "amount": amount,
                    "category": category,
                    "difficulty": difficulty,
                },
            )
            if data["response_code"] != 0:
                return None

        resolved = []
        for que in data["results"]:
            resolved.append(
                Trivia(
                    que["question"],
                    que["incorrect_answers"] + [que["correct_answer"]],
                    que["correct_answer"],
                )
            )

        return resolved

    @discord.ui.button(emoji=EMOJIS["white_tick"], style=discord.ButtonStyle.green)
    async def confirm_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(content="Trivia!", view=TriviaView())


class Games(commands.GroupCog, name="games"):
    """Games."""

    def __init__(self, bot: Orbyt):
        self.bot = bot

    async def resolve_trivia_categories(self):
        async with aiohttp.ClientSession() as session:
            data = await session.get("https://opentdb.com/api_category.php")

        categories = data["trivia_categories"]

        resolved = {category["id"]: category["name"] for category in categories}
        # add 'Any Category' = 0
        resolved[0] = "Any Category"

        return resolved

    @app_commands.command(name="trivia")
    async def trivia_game(
        self,
        interaction: discord.Interaction,
        questions: int = 5,
    ):
        """Play trivia game."""

        view = TriviaInit(
            await self.resolve_trivia_categories(),
        )

        await interaction.response.send_message(
            f"{EMOJIS['no']} - This command is not yet implemented!\n"
            f"{questions=}\n",
            view=view,
        )


async def setup(bot: Orbyt):
    await bot.add_cog(Games(bot))
