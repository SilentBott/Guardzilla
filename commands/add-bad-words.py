from nextcord.ext import commands
import json


class AddBadWords(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="add-bad-words")
    async def addbadwords(self, ctx, *, new_words):
        if not new_words:
            await ctx.send(f"Error", delete_after=8)
            return
        if '"' not in new_words:
            await ctx.send(f"Error", delete_after=8)
            return
        with open("./blockedWords.json", "r") as f:
            data = json.loads(f.read())
        words, added_blocked = [], []
        for i in range(len(str(new_words).split('"'))//2):
            words.append(str(new_words).split('"')[i*2+1])

        for bad_word in words:
            if bad_word not in data[str(ctx.message.guild.id)][1]:
                if bad_word:
                    data[str(ctx.message.guild.id)][1].append(bad_word)
                    added_blocked.append(bad_word)
        with open("./blockedWords.json", "w") as f:
            json.dump(data, f)
        if bool(added_blocked):
            await ctx.send(f"New bad words:\n" + ' | '.join([f"`{x}`" for x in added_blocked]) + "\nadded!!", delete_after=8)
        else:
            await ctx.send(f"no bad words added.", delete_after=8)


def setup(client):
    client.add_cog(AddBadWords(client))
