import random
import cogs.constants as constants

import discord
from discord.ext import commands

from typing import Text

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self._reply_methods = [
            self._reply_flameo,
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore message content if a command
        if message.content.startswith(self.bot.command_prefix):
            return

        # Process commands first
        await self.bot.process_commands(message)

        # Ignore messages from the bot itself
        if message.author.id == self.bot.user.id:
            return

        # Check if message can be replied to
        reply = self._reply(message.content.lower())
        if reply:
            await message.reply(reply, mention_author=False)

    def _reply(self, message) -> Text:
        """Checks if the given message can be replied to by the bot.
        Returns an empty string if not.
        """
        return next(
            (reply_method(message)
            for reply_method in self._reply_methods
            if reply_method(message)), "")

    def _reply_flameo(self, message) -> Text:
        """Checks if the given message contains flameo-adjacent content.
        Returns an empty string if not.
        """
        reply = ""

        for word in constants.FLAMEO_KEYWORDS:
            if word in message:
                reply = random.choice(constants.FLAMEO_RESPONSES)
                break

        return reply

