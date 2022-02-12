from nextcord.ext import commands
import json
import pymongo


class ShowBadWords(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="show-bad-words", aliases=["showbadwords", "show_bad_words"])
    async def showbadwords(self, ctx):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        blockedWords = cluster["blockedwords"]
        r = blockedWords.find_one({"_id": 0})
        words = [i for i in r[str(ctx.message.guild.id)][1]]
        await ctx.send(f"Current bad words: \n{' | '.join([f'`{x}`' for x in words])}")


def setup(client):
    client.add_cog(ShowBadWords(client))
