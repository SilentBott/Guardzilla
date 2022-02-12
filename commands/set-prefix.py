from nextcord.ext import commands
import json
import pymongo


class SetPrefix(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="set-prefix", aliases=["setprefix"])
    async def setprefix(self, ctx, prefixx):
        cluster = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")["Guardzilla"]
        prefix = cluster["prefix"]
        prefix_x = prefix.find_one({"_id": 0})
        if str(ctx.guild.id) not in prefix_x:
            prefix_x.update({str(ctx.guild.id): prefix})
        prefix_x[str(ctx.guild.id)] = prefixx

        prefix.delete_one({"_id": 0})
        prefix.insert_one(prefix_x)
        await ctx.send(f"Done!\nNew prefix set to {prefix_x[str(ctx.guild.id)]}")


def setup(client):
    client.add_cog(SetPrefix(client))
