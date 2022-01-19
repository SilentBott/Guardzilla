from nextcord.ext import commands
import json


class AddBadWords(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="add-bad-words")
    async def addbadwords(self, ctx, *, words):
        with open("./blockedWords.json", ) as f:
            r = json.loads(f.read())
        words = [i for i in str(words).split(" ")]
        added_blocked = []
        for i in words:
            if i not in r[str(ctx.message.guild.id)][1]:
                r[str(ctx.message.guild.id)][1].append(i)
                added_blocked.append(i)
        with open("./blockedWords.json", "w") as f:
            json.dump(r, f)
        if bool(added_blocked):
            await ctx.send(f"New bad words: \n {' | '.join(added_blocked)}\nadded!!", delete_after=5)
        else:
            await ctx.send(f"There is bad words with the names: {' | '.join(words)}", delete_after=5)


def setup(client):
    client.add_cog(AddBadWords(client))
