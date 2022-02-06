from nextcord.ext import commands
import json


class ShowBadWords(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="show-bad-words")
    async def showbadwords(self, ctx):
        with open("./blockedWords.json", ) as f:
            r = json.loads(f.read())
        words = [i for i in r[str(ctx.message.guild.id)][1]]
        await ctx.send(f"Current bad words: \n{' | '.join(words)}")


def setup(client):
    client.add_cog(ShowBadWords(client))
