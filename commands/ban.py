from nextcord.ext import commands
import os


class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member, *, reason=None):
        member = member.split("<@!")[1].split(">")[0]
        member = await ctx.guild.fetch_member(member)
        if ctx.author.id is member.id:
            await ctx.reply(f"You Cannot ban yourself")
        elif member.id is ctx.guild.owner.id:
            await ctx.reply(f"You Cannot ban The owner")
        elif ctx.author is ctx.guild.owner or ctx.author.top_role > member.top_role:
            if member.id == self.client.user.id:
                await ctx.reply(f"You Cannot ban the bot by its command")
            else:
                await ctx.guild.ban(member, reason=reason)
                await ctx.reply(f"The member: {member.mention} banned Successfully.")
        elif ctx.author.top_role <= member.top_role:
            await ctx.reply(f"You cannot ban: {member.mention}, because he/she have higher role as you")
        elif ctx.author.top_role == member.top_role:
            await ctx.reply(f"You cannot ban: {member.mention}, because he/she have the same role as you")


def setup(client):
    client.add_cog(Ban(client))
