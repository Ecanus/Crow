import settings
import discord
from discord.ext import commands

from cogs.utility import Utility
from cogs.listeners import Listeners

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="|", intents=intents)

@bot.event
async def on_ready():
    # Add Cogs
    await bot.add_cog(Utility(bot))
    await bot.add_cog(Listeners(bot))


    print("We have logged in as {0} as {1}".format(
        bot.user,
        bot.user.id))
    print('------')

# Run bot
bot.run(settings.DISCORD_API_SECRET)