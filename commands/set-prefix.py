from nextcord.ext import commands
import json


class SetPrefix(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True, manage_messages=True)
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="set-prefix")
    async def setprefix(self, ctx, prefix):
        with open("./prefix.json", ) as f:
            prefix_x = json.loads(f.read())
        prefix_x[str(ctx.message.guild.id)] = prefix
        with open("./prefix.json", "w") as f:
            json.dump(prefix_x, f)
        await ctx.send(f"Done!\nNew prefix set to {prefix}")


def setup(client):
    client.add_cog(SetPrefix(client))
