import settings
import discord
from discord.ext import commands

from typing import Literal

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="|", intents=intents)

@bot.event
async def on_ready():
    print("We have logged in as {0}".format(
        bot.user,
        bot.user.id))
    print('------')

# METHODS

@bot.command()
async def whois(ctx, *, member: discord.Member):
    whois_string = (
        "Here's what I found about {0}:\n\n"
        "> **Display Name:** {1}\n"
        "> **Join Date:** {2}\n"
        "> **Top Role:** {3}").format(
        ctx.message.content.replace("|whois", "").strip(),
        member.display_name,
        member.joined_at,
        str(member.top_role).replace("@", "@/")
    )

    await ctx.send(whois_string)

# ------

# TESTS

@bot.command()
async def shop(ctx, buy_sell: Literal['buy', 'sell'], amount: Literal[1, 2], *, item: str):
    await ctx.send(f'{buy_sell.capitalize()}ing {amount} {item}(s)!')

#------

# run bot
bot.run(settings.DISCORD_API_SECRET)