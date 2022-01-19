import nextcord
from nextcord.ext import commands, menus
import json


def bot_admin(ctx):
    with open("./bot_admin.json", ) as f:
        is_admin = str(ctx.message.author.id) in json.loads(
            f.read())["Admins"][0]
    return is_admin


class MyPageSource(menus.ListPageSource):  # menus.ButtonMenuPages

    def __init__(self, data):
        # this is where you can set how many items you want per page
        super().__init__(data, per_page=1)
        # self._disable_unavailable_buttons()

    async def format_page(self, menu: menus.ButtonMenuPages, entries):
        with open("./commands.json", ) as f:
            data = json.loads(f.read())[entries[0]]
        with open("./prefix.json", ) as f:
            prefix = json.loads(f.read())[entries[1]]
        if entries[0] == "Home":
            embed = nextcord.Embed(color=0xA020F0)
            embed.add_field(name=f"Welcome to Guardzilla",
                            value=f"The bot's  prefix here is `{prefix}`", inline=False)
            bott = entries[2]
            embed.add_field(
                name=f"_ _", value=f"The bot's latency: {round(bott.latency * 1000)}ms", inline=False)
            embed.add_field(
                name=f"click the buttons below to see help categories", value=f"_ _", inline=False)
        else:
            embed = nextcord.Embed(
                title="Guardzilla's commands", color=0xA020F0)
            msg = ""
            for i in data[0]:
                msg += f"> `{prefix}{i}` | {data[0][i][1]}\n"
            embed.add_field(name=f"**{entries[0]}**", value=msg, inline=False)
        embed.set_footer(
            text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
        return embed


class General(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, help_c=None):
        if help_c is None:
            with open("./commands.json", ) as f:
                r = json.loads(f.read())
            category = [x for x in r][:-1 if not bot_admin(ctx) else None]
            channel_ids = [str(ctx.message.guild.id)] * \
                len([x for x in r][:-1 if not bot_admin(ctx) else None])
            bott = [self.client] * len(r)
            data = list(zip(category, channel_ids, bott))
            pages = menus.ButtonMenuPages(
                source=MyPageSource(data),
                delete_message_after=True,
                style=2,
            )
            await pages.start(ctx)
        else:
            try:
                command = help_c
                prefix = str(ctx.message.content).split(
                    " ")[0].replace("help", "")
                with open("./commands.json", ) as f:
                    r = json.loads(f.read())
                    r = r if bot_admin(ctx) else r[:-2]
                    cm = {}
                    for i in r:
                        for ii in r[i][0]:
                            if i != "Home":
                                cm.update({str(ii): list(r[i][0][ii])})
                    cm = cm[command]
                    usage = cm[0]
                    description = cm[1]
                    needing = cm[2]
                    examples = cm[3]
                if bool(examples):
                    emm = self.client.get_emoji(922791127516598312)
                    example_val = f"\n".join([x.replace("prefix-", prefix).replace("member-mention", ctx.author.mention).
                                             replace("member-id", f"{ctx.author.id}").
                                              replace("msg-id", f"{ctx.message.id}").replace("role-", str(ctx.guild.roles[1].mention)).
                                              replace("emoji-", f"{emm}").
                                             replace("room-mention", f"{ctx.channel.mention}").
                                             replace("room-id", f"{ctx.channel.id}") for x in examples])
                else:
                    example_val = f"{prefix}{command} {ctx.author.mention}\n{prefix}{command} {ctx.author.id}"
                embedVar = nextcord.Embed(
                    title=f"Command: {command}", description=f"{description}", color=0xA020F0)
                embedVar.add_field(
                    name="Usage: ", value=f"{prefix}{command} {usage}", inline=False)
                if needing != '':
                    embedVar.add_field(
                        name="Permission requirements: ", value=needing, inline=False)
                embedVar.add_field(name="Examples: ",
                                   value=example_val,
                                   inline=False)
                await ctx.reply(embed=embedVar)
            except KeyError:
                await ctx.reply("There isn't any command like that")


"""
        with open("./commands.json") as f:
            bot_commands = json.loads(f.read())
            if not bot_admin(ctx):
                bot_commands.pop("Bot Admin Commands")
        if ctx.message.guild:
            with open("prefix.json", ) as file:
                prefix_x = json.loads(file.read())
            prefix = prefix_x[str(ctx.message.guild.id)]
        else:
            prefix = '!'
        embed = nextcord.Embed(color=0x00ff00)
        embed.set_author(name="Press the menu below to show help menu", icon_url=self.client.user.avatar_url)
        embed.add_field(name=f"The bot Latency is: {round(self.client.latency * 1000)}ms", value=f"_ _", inline=False)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        options = []
        ans = {}
        for i in bot_commands:
            embed_d = nextcord.Embed(color=0x00ff00)
            embed_d.set_author(name=f"{i}", icon_url=self.client.user.avatar_url)
            embed_d.set_thumbnail(url=self.client.user.avatar_url)
            for ii in bot_commands[i][0]:
                embed_d.add_field(name="_ _", value=f"``{prefix}{ii}`` | {bot_commands[i][0][ii][1]}", inline=False)
            ans.update({i: embed_d})
            options.append(SelectOption(label=i,
                                 value=i,
                                 emoji=self.client.get_emoji(int(bot_commands[i][1]) if bot_commands[i][1] != "" else 922787663352840203),
                                description=bot_commands[i][2]))

        msg = await ctx.send(embed=embed, components=[Select(
                placeholder="Click here to view the help menu!",
                options=options,
                custom_id="SelectTesting"


            )])

        def check(ctx_x):
            if ctx_x.custom_id == "SelectTesting" and ctx_x.user == ctx_x.author and ctx_x.message.id == msg.id:
                return
        for i in range(100):
            interaction = await self.client.wait_for("select_option",
             check=lambda ctx_x: ctx_x.custom_id == "SelectTesting" and ctx_x.user == ctx_x.author and ctx_x.message.id == msg.id)
            val = ans[interaction.values[0]] if interaction.values[0] not in ["Home page"]else embed
            await msg.edit(embed=val)
            try:
                await interaction.respond()
            except:
                pass
"""


def setup(client):
    client.add_cog(General(client))
