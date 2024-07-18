
from discord.ext import commands

from typing import Literal

class Workshop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(
        self, ctx, buy_sell: Literal['buy', 'sell'], amount: Literal[1, 2],
        *, item: str):
        await ctx.send(f'{buy_sell.capitalize()}ing {amount} {item}(s)!')