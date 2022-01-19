from nextcord.ext import commands
import nextcord
from nextcord.utils import get


class Hide(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command()
    async def hide(self, ctx, channel=None):
        if not channel:
            channel = ctx.channel
        else:
            try:
                channel = str(int(channel))
            except ValueError:
                channel = channel.split("<#")[1].split(">")[0]
            channel = await ctx.guild.fetch_channel(channel)
        l = channel.permissions_for(ctx.guild.default_role)
        if l.view_channel:
            await channel.set_permissions(ctx.guild.default_role, view_channel=False)
            embed = nextcord.Embed(
                description=f"The channel {channel.mention} hided sucessfully.", color=0x00ff00)
        else:
            embed = nextcord.Embed(
                description="The channel already hidden", color=0x00ff00)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Hide(client))
