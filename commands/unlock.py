from nextcord.ext import commands
import nextcord


class UnLock(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command()
    async def unlock(self, ctx):
        perm = ctx.channel.permissions_for(ctx.guild.default_role)
        if not perm.send_messages:
            await ctx.message.channel.set_permissions(ctx.guild.default_role,
                                                      overwrite=None)
            embed = nextcord.Embed(
                title="",
                description=f"The chat locked successfully.",
                color=0x00ff00)
        else:

            embed = nextcord.Embed(title="",
                                   description=f"The chat already unlocked.",
                                   color=0x00ff00)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(UnLock(client))
