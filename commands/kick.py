from nextcord.ext import commands


class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member, *, reason=None):
        member = member.split("<@!")[1].split(">")[0]
        member = await ctx.guild.fetch_member(member)
        if ctx.author.id == member.id:
            await ctx.reply(f"You Cannot kick yourself")
        elif member.id == ctx.guild.owner.id:
            await ctx.reply(f"You Cannot kick The owner")
        elif ctx.author is ctx.guild.owner or ctx.author.top_role > member.top_role:
            if member.id == self.client.user.id:
                await ctx.reply(f"You Cannot kick the bot by its command")
            else:
                await ctx.guild.kick(member, reason=reason)
                await ctx.reply(f"The member: {member.mention} kicked Successfully.")
        elif ctx.author.top_role <= member.top_role:
            await ctx.reply(f"You cannot kick: {member.mention}, because he/she have higher role as you")
        elif ctx.author.top_role == member.top_role:
            await ctx.reply(f"You cannot kick: {member.mention}, because he/she have the same role as you")


def setup(client):
    client.add_cog(Kick(client))
