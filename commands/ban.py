# modules i'll use
from nextcord.ext import commands


class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member, *, reason=None):
        #get the user
        member = member.split("<@!")[-1].split("<@")[-1].split(">")[0]
        member = await ctx.guild.fetch_member(member)
        # check if all states if O K
        if ctx.author.id == member.id:
            await ctx.reply(f"You Cannot ban yourself")
        elif member.id == ctx.guild.owner.id:
            await ctx.reply(f"You Cannot ban The owner")
        elif ctx.author.top_role < member.top_role:
            await ctx.reply(
                f"You cannot ban: {member.mention}, because {member.name} have higher role."
            )
        elif ctx.author.top_role == member.top_role:
            await ctx.reply(
                f"You cannot ban: {member.mention}, because {member.name} and you are having the same role."
            )
        elif ctx.author.top_role > member.top_role:
            if member.id == self.client.user.id:
                await ctx.reply(f"You Cannot ban the bot by its command")
            else:
                await ctx.guild.ban(member, reason=reason)
                await ctx.reply(
                    f"The member: {member.mention} banned Successfully.")

# add the command as cog
def setup(client):
    client.add_cog(Ban(client))
