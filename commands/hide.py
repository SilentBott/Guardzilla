#import required modules
from nextcord.ext import commands
import nextcord


class Hide(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command()
    async def hide(self, ctx, channel=None):
        #if admin didn't mention the channel
        if not channel:
            # select the current channel
            channel = ctx.channel
        else:
            #get the selected channel
            try:
                channel = str(int(channel))
            except ValueError:
                channel = channel.split("<#")[1].split(">")[0]
            channel = await ctx.guild.fetch_channel(channel)
        #get the channel perms
        l = channel.permissions_for(ctx.guild.default_role)
        #check if its visible
        if l.view_channel:
            #change perms
            await channel.set_permissions(ctx.guild.default_role,
                                          view_channel=False)
            embed = nextcord.Embed(
                description=f"The channel {channel.mention} hided sucessfully.",
                color=0x00ff00)
        #check if hidden
        else:
            embed = nextcord.Embed(description="The channel already hidden",
                                   color=0x00ff00)
        #send the msg
        await ctx.send(embed=embed)


# add the command as cog
def setup(client):
    client.add_cog(Hide(client))
