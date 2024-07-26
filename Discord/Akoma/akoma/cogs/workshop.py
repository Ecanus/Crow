import discord

from discord.ext import commands
from PyDictionary import PyDictionary

from typing import Literal

class Counter(discord.ui.View):
    pass

# class Workshop(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.command()
#     async def shop(
#         self, ctx, buy_sell: Literal['buy', 'sell'], amount: Literal[1, 2],
#         *, item: str):
#         await ctx.send(f'{buy_sell.capitalize()}ing {amount} {item}(s)!')

dictionary = PyDictionary()

print(dictionary.meaning("adf"))