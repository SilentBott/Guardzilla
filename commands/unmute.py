from nextcord.ext import commands
import nextcord


class UnMute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command()
    async def unmute(self, ctx, member):
        try:
            member = str(int(member))
        except ValueError:
            member = member.split("<@!")[1].split(">")[0]
        member = await ctx.guild.fetch_member(member)
        ch = []
        for channel in ctx.guild.text_channels:
            # f = await channel.set_permissions(member, send_messages=False)
            l = channel.permissions_for(member)
            if not l.send_messages:
                await channel.set_permissions(member, overwrite=None)
                ch.append(l)
        if len(ch) > 1:
            embed = nextcord.Embed(title="", description=f"The member {member.mention} Muted successfully.",
                               color=0x00ff00)
        else:
            embed = nextcord.Embed(title="", description=f"The member {member.mention} already UnMuted.",
                               color=0x00ff00)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(UnMute(client))
