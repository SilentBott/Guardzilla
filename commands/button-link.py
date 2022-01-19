import discord.ui
from nextcord.ext import commands, menus
from nextcord.ui import View, Button
import nextcord


class ButtonLink(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="button-link")
    async def embed(self, ctx, link, label, emoji: nextcord.Emoji or nextcord.PartialEmoji,  *, embed_message):
        embed = nextcord.Embed(title="", description=embed_message, color=0x00ff00)
        butt = Button(style=nextcord.ButtonStyle.link, label=str(label).replace("_", " "), url=link, emoji=emoji)
        view = View()
        view.add_item(butt)
        await ctx.send(embed=embed, view=view)


def setup(client):
    client.add_cog(ButtonLink(client))
