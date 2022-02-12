from nextcord.ext import commands
import json
import pymongo


class AddBadWords(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="add-bad-words", aliases=["add-bad-word", "addbadwords", "addbadword", 'add_bad_words', "add_bad_word"])
    async def addbadwords(self, ctx, *, new_words):
        if '"' not in new_words:
            await ctx.send(f"Error", delete_after=8)
            return

        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        blockedwords = cluster["blockedwords"]
        data = blockedwords.find_one({"_id": 0})
        if not data:
            blockedwords.insert_one({"_id": 0, str(ctx.guild.id): [0, []]})
            data = blockedwords.find_one({"_id": 0})
        if str(ctx.guild.id) not in data:
            blockedwords.insert_one({"_id": 0, str(ctx.guild.id): [0, []]})
            data = blockedwords.find_one({"_id": 0})

        words, added_blocked = [], []
        for i in range(len(str(new_words).split('"'))//2):
            words.append(str(new_words).split('"')[i*2+1])

        for bad_word in words:
            if bad_word not in data[str(ctx.message.guild.id)][1]:
                if bad_word:
                    data[str(ctx.message.guild.id)][1].append(bad_word)
                    added_blocked.append(bad_word)
        # delete data from data base
        blockedwords.delete_one({"_id": 0})
        # add the new data to the data base
        blockedwords.insert_one(data)

        if bool(added_blocked):
            await ctx.send(f"New bad words:\n" + ' | '.join([f"`{x}`" for x in added_blocked]) + "\nadded!!", delete_after=8)
        else:
            await ctx.send(f"no bad words added.", delete_after=8)


def setup(client):
    client.add_cog(AddBadWords(client))
