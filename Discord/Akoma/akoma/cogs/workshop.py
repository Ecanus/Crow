import discord

from discord.ext import commands

from typing import Literal

import requests
from bs4 import BeautifulSoup

# class Workshop(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.command()
#     async def shop(
#         self, ctx, buy_sell: Literal['buy', 'sell'], amount: Literal[1, 2],
#         *, item: str):
#         await ctx.send(f'{buy_sell.capitalize()}ing {amount} {item}(s)!')

# url = "https://www.merriam-webster.com/dictionary/endeavour"
# response = requests.get(url)

# soup = BeautifulSoup(response.content, "html.parser")
# entry_word_section = soup.find_all(class_="entry-word-section-container")

# # Check if misspelled word (class_="mispelled-word")

# # If definition exists.
# # Check if British v. American spelling (class_="cxl-ref") text contains "chiefly British spelling of"
# if entry_word_section:
#     for entry in entry_word_section:
#         parts_of_speech = entry.find(class_="parts-of-speech")
#         print(parts_of_speech.get_text())

#         definitions = entry.find_all("span", class_="dtText")
#         for d in definitions:
#             print(d.get_text())

from akoma.utils import get_definitions_from_website

definitions = get_definitions_from_website("pickle")
print(definitions)


