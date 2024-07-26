import discord
from discord.ext import commands

from typing import Text

import utils

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whois(self, ctx, *, member: discord.Member):
        """Method for revealing information on the given member.
        """
        whois_str = (
            ":speech_left: **{0}**\n\n"
            "> **Display Name:** {1}\n"
            "> **Join Date:** {2}\n"
            "> **Top Role:** {3}").format(
            ctx.message.content.replace("|whois", "").strip(),
            member.display_name,
            utils.format_date(member.joined_at),
            str(member.top_role).replace("@", "@/")
        )

        await ctx.reply(utils.sign(whois_str))

    @commands.command()
    async def whatis(self, ctx, word: Text):
        """Method for defining the given word.
        """
        whatis_str = utils.get_definition_str(word)
        await ctx.reply(utils.sign(whatis_str))

