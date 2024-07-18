import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whois(self, ctx, *, member: discord.Member):
        """Method for revealing information on the given member.
        """
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

