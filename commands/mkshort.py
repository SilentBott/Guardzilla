from nextcord.ext import commands
import json


class mkShort(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command()
    async def mkshort(self, ctx, q, *, ans=""):
        with open("shorts.json", ) as f:
            data = json.load(f)
        if not ans and q in data:
            data.pop(q)
            await ctx.send(f"DONE!\n \"{q}\" removed from the shorts")
        elif not ans and q not in data:
            await ctx.send(f"ERROR!\n\"{q}\"not in shorts to remove it")
        else:
            data[q] = ans
            await ctx.send("Done!")
        with open("shorts.json", "w") as f:
            json.dump(data, f)


def setup(client):
    client.add_cog(mkShort(client))
