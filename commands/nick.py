from nextcord.ext import commands
import nextcord
import pymongo


class Nick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    @commands.command()
    async def nick(self, ctx, member, *, nick=None):
        try:
            member = str(int(member))
        except ValueError:
            member = member.split("<@")[1].split(">")[0].replace("!", "")
        member = await ctx.guild.fetch_member(member)
        embed = nextcord.Embed(color=0x00ff00)
        if str(member.id) == str(ctx.message.guild.owner.id):
            embed.set_author(
                name=f"Sorry but i cannot change guild owner's nickname")
            await ctx.send(embed=embed)
            return
        if nick == None:
            if member.name == member.display_name:
                embed.set_author(
                    name=f"The member already don't have nickname",
                    url=member.avatar.url)
            elif member.name != member.display_name:
                dn = member.display_name
                n = member.namit(nick=member.name)
                if member.avatar:
                    embed.set_author(
                        name=
                        f"Member: {member.name}\nNickname reset: to '{member.name}'",
                        url=member.avatar.url)
                else:
                    embed.set_author(
                        name=
                        f"Member: {member.name}\nNickname reset: to '{member.name}'"
                    )
        else:
            if member.display_name == nick:
                embed.set_author(name=f"This is already the user nickname",
                                 url=member.avatar.url)

            elif nick == member.name:
                dn = member.display_name
                await member.edit(nick=nick)
                embed.set_author(
                    name=
                    "Member: {member.mention}\nReset its name: `{dn.name}`",
                    url=member.avatar.url)

            else:
                if member.avatar:
                    embed.set_author(name="This is the member nickname ",
                                     url=member.avatar.url)
                else:
                    embed.set_author(name="This is the member nickname ")
                dn = member.display_name
                await member.edit(nick=nick)
                if member.avatar:
                    embed.set_author(
                        name=f"Nick name changed\nFrom: {dn} to: `{nick}`",
                        url=member.avatar.url)
                else:
                    embed.set_author(
                        name=f"Nick name changed\nFrom: {dn} to: `{nick}`")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Nick(client))
