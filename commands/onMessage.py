from nextcord.ext import commands
import json
import pymongo
from os import environ as getenv


def blocked(msg, words: list):
    for word in words:
        if word in str(msg.content).lower():
            return True
    else:
        return False


class OnMessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_message(self, message):
        with open("bot_admin.json", "r") as f:
            admins = json.loads(f.read())["Admins"]
        if message.guild is None or message.author.bot:
            return
        db = pymongo.MongoClient(getenv["mongoDBclient"])[str(
            message.guild.id)]

        # suggestion chat-----------------------------------------------------------
        if message.content[0] != "r":
            suggestions = db["suggestionsRoom"]
            channel = suggestions.find_one({"_id": 0})
            if not channel:
                suggestions.insert_one({"_id": 0})
                channel = suggestions.find_one({"_id": 0})
            if "id" in channel:
                if str(channel["id"]) == str(message.channel.id):
                    await message.add_reaction(emoji="✅")
                    await message.add_reaction(emoji="❎")

        # shorts respond ------------------------------------------------------------
        with open("shorts.json", ) as f:
            data = json.load(f)
        for i in data:
            if i in message.content:
                await message.channel.send(data[i])
                break

        #bad words --------------------------------------------------------------
        if str(message.author.id) in admins:
            return
        blockedWords = db["blockedwords"]
        log = blockedWords.find_one({"_id": 0})
        if not log:
            blockedWords.insert_one({"_id": 0, str(message.guild.id): [0, []]})
            log = blockedWords.find_one({"_id": 0})
        try:
            blocked_true, words = log[str(message.guild.id)]
        except:
            log.update({str(message.guild.id): [0, []]})
            blockedWords.delete_one({"_id": 0})
            blockedWords.insert_one(log)
            blocked_true, words = log[str(message.guild.id)]
        if blocked_true:
            if blocked(message, words):
                await message.delete()
                ""
                await message.channel.send(
                    f"The message deleted cuz its bad word ok? {message.author.mention}.",
                    delete_after=5)
                return


def setup(client):
    client.add_cog(OnMessage(client))
