from nextcord.ext import commands
import nextcord
from nextcord.utils import get
import pymongo


class Lock(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command()
    async def lock(self, ctx):
        perm = ctx.channel.permissions_for(ctx.guild.default_role)
        if perm.send_messages:
            await ctx.message.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            embed = nextcord.Embed(title="", description=f"The chat locked successfully.",
                                   color=0x00ff00)
        else:

            embed = nextcord.Embed(title="", description=f"The chat already locked.",
                                   color=0x00ff00)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Lock(client))
