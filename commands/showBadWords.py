from nextcord.ext import commands
import pymongo
from os import environ as getenv

class ShowBadWords(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="show-bad-words", aliases=["showbadwords", "show_bad_words"])
    async def showbadwords(self, ctx):
        db = pymongo.MongoClient(getenv["mongoDBclient"])[str(ctx.message.guild.id)]
        blockedWords = db["blockedwords"]
        r = blockedWords.find_one({"_id": 0})
        words = [i for i in r[str(ctx.message.guild.id)][1]]
        await ctx.send(f"Current bad words: \n{' | '.join([f'`{x}`' for x in words])}")


def setup(client):
    client.add_cog(ShowBadWords(client))
