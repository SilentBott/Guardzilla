import json
from nextcord.ext import commands
import nextcord


class Warns(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command()
    async def warns(self, ctx, member=None):
        if member is None:
            member = ctx.author
        else:
            try:
                member = str(int(member))
            except ValueError:
                member = member.split("<@")[1].split(">")[0].replace("!", "")
            member = await ctx.guild.fetch_member(member)
        embed = nextcord.Embed(color=0x00ff00)
        with open("./warns.json", ) as f:
            warnings = json.loads(f.read())
        if str(ctx.guild.id) in warnings:
            if str(member.id) in warnings[str(ctx.guild.id)]:
                embed.title = f"{len(warnings[str(ctx.guild.id)][str(member.id)])} Warnings"
                decs = f""
                for i in warnings[str(ctx.guild.id)][str(member.id)]:
                    decs += f"***{i[0]}***\n***By: ***<@{i[1]}>\n``` {i[2]} ```\n"
                embed.description = decs
            else:
                embed.add_field(
                    name=f"The member: {member.display_name} | {member.id}:\nDoesn't have any warnings.", value="_ _")
        else:
            embed.add_field(
                name=f"The member: {member.display_name} | {member.id}:\nDoesn't have any warnings.", value="_ _")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Warns(client))