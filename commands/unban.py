from nextcord.ext import commands


class Unban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        banned_users = await ctx.guild.bans()
        try:
            banned_id = int(member)
        except ValueError:
            banned_id = int(member.split("<@!")[1].split(">")[0])
        user = [user for user in banned_users if banned_id == user.user.id]
        if bool(user):
            await ctx.guild.unban(user[0].user)
            await ctx.reply(f"The member: {user[0].user.mention} unbanned Successfully.")
        else:
            await ctx.reply(f"There isn't any banned user with the user: <@{banned_id}>")


def setup(client):
    client.add_cog(Unban(client))
