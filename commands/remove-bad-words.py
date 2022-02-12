from nextcord.ext import commands
import json
import pymongo
import os


class RemoveBadWords(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="remove-bad-words")
    async def removebadwords(self, ctx, *, bad_words):
        bad_word = False
        cluster = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")["Guardzilla"]
        blockedWords = cluster["blockedwords"]
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
