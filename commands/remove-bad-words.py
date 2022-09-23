from nextcord.ext import commands
import json
import pymongo
from os import environ as getenv

class RemoveBadWords(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="remove-bad-words")
    async def removebadwords(self, ctx, *, bad_words):
        bad_word = False
        db = pymongo.MongoClient(getenv["mongoDBclient"])[ctx.message.guild.id]
        blockedWords = db["blockedwords"]
        data = blockedWords.find_one({"_id": 0})
        words, blocked_words = [], []
        for i in range(len(str(bad_words).split('"'))//2):
            words.append(str(bad_words).split('"')[i*2+1])

        for i in words:
            if i in data[str(ctx.message.guild.id)][1]:
                data[str(ctx.message.guild.id)][1].remove(i)
                blocked_words.append(i)
        if blocked_words:
            l = f"Bad words:\n" + \
                ' | '.join([f"`{x}`" for x in blocked_words]) + "\nremoved!!"
        else:
            l = f"There isn't bad words to remove"
        blockedWords.delete_one({"_id": 0})
        blockedWords.insert_one(data)
        await ctx.send(l, delete_after=5)


def setup(client):
    client.add_cog(RemoveBadWords(client))
