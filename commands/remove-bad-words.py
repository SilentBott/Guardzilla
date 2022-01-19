from nextcord.ext import commands
import json


class RemoveBadWords(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="remove-bad-words")
    async def removebadwords(self, ctx, *, words):
        bad_word = False
        with open("./blockedWords.json", ) as f:
            r = json.loads(f.read())
        words = [i for i in str(words).split(" ")]
        blocked_words = []
        for i in words:
            if i in r[str(ctx.message.guild.id)][1]:
                r[str(ctx.message.guild.id)][1].remove(i)
                bad_word = True
                blocked_words.append(i)
        if bad_word:
            l = f"The bad words:\n{' | '.join(blocked_words)}\nRemoved!!"
        else:
            l = f"There isn't bad words with the names: \n{' | '.join(blocked_words)}\n"
        with open("./blockedWords.json", "w") as f:
            json.dump(r, f)
        await ctx.send(l, delete_after=5)


def setup(client):
    client.add_cog(RemoveBadWords(client))
