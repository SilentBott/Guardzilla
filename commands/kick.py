#import required module
from nextcord.ext import commands


class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member, *, reason=None):
        # get the selected member
        member = member.split("<@!")[1].split(">")[0]
        member = await ctx.guild.fetch_member(member)
        # if selected member is the member who called the function
        if ctx.author.id == member.id:
            await ctx.reply(f"You Cannot kick yourself")
        # if selected member is the owner of the server
        elif member.id == ctx.guild.owner.id:
            await ctx.reply(f"You Cannot kick The owner")
        # if its the owner or someone who have higher perms wants to kick someone
        elif ctx.author is ctx.guild.owner or ctx.author.top_role > member.top_role:
            if member.id == self.client.user.id:
                await ctx.reply(f"You Cannot kick the bot by its command")
            else:
                await ctx.guild.kick(member, reason=reason)
                await ctx.reply(
                    f"The member: {member.mention} kicked Successfully.")
        # if selected member have higher role
        elif ctx.author.top_role <= member.top_role:
            await ctx.reply(
                f"You cannot kick: {member.mention}, because he/she have higher role as you"
            )
        # if selected member have the same higher author perms
        elif ctx.author.top_role == member.top_role:
            await ctx.reply(
                f"You cannot kick: {member.mention}, because he/she have the same role as you"
            )

# add the command as cog
def setup(client):
    client.add_cog(Kick(client))
