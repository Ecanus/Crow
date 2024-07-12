import settings
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="|", intents=intents)

@bot.event
async def on_ready():
    print("We have logged in as {0}".format(
        bot.user,
        bot.user.id))
    print('------')

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

bot.run(settings.DISCORD_API_SECRET)

"""
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0}".format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$hello"):
        await message.channel.send("Hello! Katcherr")

client.run(settings.DISCORD_API_SECRET)"""