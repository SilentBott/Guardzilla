from nextcord.ext import commands
import json


class RemoveBadWords(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="remove-bad-words")
    async def removebadwords(self, ctx, *, bad_words):
        bad_word = False
        with open("./blockedWords.json", ) as f:
            data = json.loads(f.read())
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
        with open("./blockedWords.json", "w") as f:
            json.dump(data, f)
        await ctx.send(l, delete_after=5)


def setup(client):
    client.add_cog(RemoveBadWords(client))
