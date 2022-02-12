import nextcord
from nextcord.ext import commands, menus
import json
import pymongo
import os


def bot_admin(ctx):
    cluster = pymongo.MongoClient(
        f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")["Guardzilla"]
    bot_admin = cluster["bot_admin"]
    r = bot_admin.find_one({"_id": 0})
    if not r:
        bot_admin.insert_one({"_id": 0, "Admins": ["821486817957642242"]})
        r = bot_admin.find_one({"_id": 0})
    if str(ctx.guild.id) not in r:
        bot_admin.delete_one({"_id": 0})
        bot_admin.insert_one({"_id": 0, "Admins": ["821486817957642242"]})
        r = bot_admin.find_one({"_id": 0})
    is_admin = str(ctx.message.author.id) in r["Admins"]
    return is_admin


class MyPageSource(menus.ListPageSource):  # menus.ButtonMenuPages

    def __init__(self, data):
        # this is where you can set how many items you want per page
        super().__init__(data, per_page=1)
        # self._disable_unavailable_buttons()

    async def format_page(self, menu: menus.ButtonMenuPages, entries):
        cluster = pymongo.MongoClient(
        f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")["Guardzilla"]
        prefix = cluster["prefix"].find_one({"_id": 0})[entries[1]]
        data = {
            "Home": [{}, "", ""],

            "General Commands": [{
                "ticket": ["", "to make tickets", "", ["prefix-ticket"], ""]
            }, "", "To show General Commands"],

            "Admin Commands": [{
                "kick": ["<member> [reason]", "to kick someone", "Kick members perms", [], "922786678454771742"],
                "ban": ["<member> [reason]", "to ban someone", "Ban members perms", [], "922790457556226078"],
                "unban": ["<member>", "to unban someone", "Ban members perms", [], ""],
                "add-bad-words": ["[words]", "to make reaction that if any one pressed it will get role", "manage messages perms", ["prefix-add-bad-words f*** trash"], ""],
                "remove-bad-words": ["[words]", "to remove the bad words in the list", "manage messages perms", ["prefix-remove-bad-words f*** trash"], ""],
                "clear": ["<number> <member> <channel>", "to clear messages in a channel / to clear messages from someone only in the last 100 msg on each channel", "manage messages perms", ["prefix-clear 1", "prefix-clear 20"], ""],
                "mute": ["<member>", "to make someone unable to send messages in text channels", "manage messages perms", [], ""],
                "unmute": ["<member>", "to Cancel the effect of the mute command", "manage messages perms", [], ""],
                "hide": ["<channel>", "Make any channel unvisible to normal people", "manage messages perms", ["prefix-hide room-mention", "prefix-show room-id"], ""],
                "show": ["<channel>", "Make any channel visible to normal people", "manage messages perms", ["prefix-show room-mention", "prefix-show room-id"], ""],
                "nick": ["<member> [nick name]", "to change member nickname", "manage nicknames perms", ["prefix-nick member-id Awsome person"], ""],
                "embed": ["[phrase]", "to make reaction that if any one pressed it will get role", "manage messages perms", ["prefix-embed Hi all"], ""],
                "warn": ["<member> [reason]", "to warn someone", "manage messages perms", ["prefix-warn member-id", "prefix-warn member-mention cuz i hate him/her"], ""],
                "removewarn": ["<member> <number>", "to remove warn from someone", "manage messages perms", ["prefix-removewarn member-id 1", "prefix-warn member-mention 2"], ""],
                "show-bad-words": ["", "to show bad words list", "", ["prefix-show-bad-words"], ""]

            }, "", "To show Admin Commands"],
            "Server admin commands": [{
                "set-prefix": ["<prefix>", "to change server prefix", "manage messages perms", ["prefix-set-prefix -", "prefix-set-prefix #"], ","],
                "chat-filter": ["<true / false>", "enable/disable the chat filter (delete bad words)", "manage messages perms", ["prefix-chat-filter Enable", "prefix-chat-filter Disable"], ""],
                "suggest-room": ["<Text channel>", "to make room for suggestion", "manage messages perms", ["prefix-suggest-room", "prefix-suggest-room room-mention", "prefix-suggest-room room-id"], ""],
                "reaction-role": ["<message id> <custom emoji> <role>", "to put reaction and make anyone click it it get the role", "manage roles perms", ["prefix-reaction-role msg-id emoji- role-"], ""]

            }, "", "To show Admin Commands"],

            "Bot Admin Commands": [{
                "load": ["<cog name>", "to load cog", "You need to be: The Bot developer", ["prefix-load kick", "prefix-load ban"], ""],
                "unload": ["<cog name>", "to unload cog", "You need to be: The Bot developer", ["prefix-unload kick", "prefix-unload ban"], ""],
                "reload": ["<cog name>", "to reload cog", "You need to be: The Bot developer", ["prefix-reload kick", "prefix-reload ban"], ""]
            }, "", "To show Bot Admin Commands"]
        }
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
            for i in data[entries[0]][0]:
                msg += f"> `{prefix}{i}` | {data[entries[0]][0][i][1]}\n"
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
            client = pymongo.MongoClient(
        f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            cluster = client["Guardzilla"]
            commands = cluster["commands"]
            r = {
                "Home": [{}, "", ""],

                "General Commands": [{
                    "ticket": ["", "to make tickets", "", ["prefix-ticket"], ""]
                }, "", "To show General Commands"],

                "Admin Commands": [{
                    "kick": ["<member> [reason]", "to kick someone", "Kick members perms", [], "922786678454771742"],
                    "ban": ["<member> [reason]", "to ban someone", "Ban members perms", [], "922790457556226078"],
                    "unban": ["<member>", "to unban someone", "Ban members perms", [], ""],
                    "add-bad-words": ["[words]", "to make reaction that if any one pressed it will get role", "manage messages perms", ["prefix-add-bad-words f*** trash"], ""],
                    "remove-bad-words": ["[words]", "to remove the bad words in the list", "manage messages perms", ["prefix-remove-bad-words f*** trash"], ""],
                    "clear": ["<number> <member> <channel>", "to clear messages in a channel / to clear messages from someone only in the last 100 msg on each channel", "manage messages perms", ["prefix-clear 1", "prefix-clear 20"], ""],
                    "mute": ["<member>", "to make someone unable to send messages in text channels", "manage messages perms", [], ""],
                    "unmute": ["<member>", "to Cancel the effect of the mute command", "manage messages perms", [], ""],
                    "hide": ["<channel>", "Make any channel unvisible to normal people", "manage messages perms", ["prefix-hide room-mention", "prefix-show room-id"], ""],
                    "show": ["<channel>", "Make any channel visible to normal people", "manage messages perms", ["prefix-show room-mention", "prefix-show room-id"], ""],
                    "nick": ["<member> [nick name]", "to change member nickname", "manage nicknames perms", ["prefix-nick member-id Awsome person"], ""],
                    "embed": ["[phrase]", "to make reaction that if any one pressed it will get role", "manage messages perms", ["prefix-embed Hi all"], ""],
                    "warn": ["<member> [reason]", "to warn someone", "manage messages perms", ["prefix-warn member-id", "prefix-warn member-mention cuz i hate him/her"], ""],
                    "removewarn": ["<member> <number>", "to remove warn from someone", "manage messages perms", ["prefix-removewarn member-id 1", "prefix-warn member-mention 2"], ""],
                    "show-bad-words": ["", "to show bad words list", "", ["prefix-show-bad-words"], ""]

                }, "", "To show Admin Commands"],
                "Server admin commands": [{
                    "set-prefix": ["<prefix>", "to change server prefix", "manage messages perms", ["prefix-set-prefix -", "prefix-set-prefix #"], ","],
                    "chat-filter": ["<true / false>", "enable/disable the chat filter (delete bad words)", "manage messages perms", ["prefix-chat-filter Enable", "prefix-chat-filter Disable"], ""],
                    "suggest-room": ["<Text channel>", "to make room for suggestion", "manage messages perms", ["prefix-suggest-room", "prefix-suggest-room room-mention", "prefix-suggest-room room-id"], ""],
                    "reaction-role": ["<message id> <custom emoji> <role>", "to put reaction and make anyone click it it get the role", "manage roles perms", ["prefix-reaction-role msg-id emoji- role-"], ""]

                }, "", "To show Admin Commands"],

                "Bot Admin Commands": [{
                    "load": ["<cog name>", "to load cog", "You need to be: The Bot developer", ["prefix-load kick", "prefix-load ban"], ""],
                    "unload": ["<cog name>", "to unload cog", "You need to be: The Bot developer", ["prefix-unload kick", "prefix-unload ban"], ""],
                    "reload": ["<cog name>", "to reload cog", "You need to be: The Bot developer", ["prefix-reload kick", "prefix-reload ban"], ""]
                }, "", "To show Bot Admin Commands"]
            }

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
                r = {
                    "Home": [{}, "", ""],

                    "General Commands": [{
                        "ticket": ["", "to make tickets", "", ["prefix-ticket"], ""]
                    }, "", "To show General Commands"],

                    "Admin Commands": [{
                        "kick": ["<member> [reason]", "to kick someone", "Kick members perms", [], "922786678454771742"],
                        "ban": ["<member> [reason]", "to ban someone", "Ban members perms", [], "922790457556226078"],
                        "unban": ["<member>", "to unban someone", "Ban members perms", [], ""],
                        "add-bad-words": ["[words]", "to make reaction that if any one pressed it will get role", "manage messages perms", ["prefix-add-bad-words f*** trash"], ""],
                        "remove-bad-words": ["[words]", "to remove the bad words in the list", "manage messages perms", ["prefix-remove-bad-words f*** trash"], ""],
                        "clear": ["<number> <member> <channel>", "to clear messages in a channel / to clear messages from someone only in the last 100 msg on each channel", "manage messages perms", ["prefix-clear 1", "prefix-clear 20"], ""],
                        "mute": ["<member>", "to make someone unable to send messages in text channels", "manage messages perms", [], ""],
                        "unmute": ["<member>", "to Cancel the effect of the mute command", "manage messages perms", [], ""],
                        "hide": ["<channel>", "Make any channel unvisible to normal people", "manage messages perms", ["prefix-hide room-mention", "prefix-show room-id"], ""],
                        "show": ["<channel>", "Make any channel visible to normal people", "manage messages perms", ["prefix-show room-mention", "prefix-show room-id"], ""],
                        "nick": ["<member> [nick name]", "to change member nickname", "manage nicknames perms", ["prefix-nick member-id Awsome person"], ""],
                        "embed": ["[phrase]", "to make reaction that if any one pressed it will get role", "manage messages perms", ["prefix-embed Hi all"], ""],
                        "warn": ["<member> [reason]", "to warn someone", "manage messages perms", ["prefix-warn member-id", "prefix-warn member-mention cuz i hate him/her"], ""],
                        "removewarn": ["<member> <number>", "to remove warn from someone", "manage messages perms", ["prefix-removewarn member-id 1", "prefix-warn member-mention 2"], ""],
                        "show-bad-words": ["", "to show bad words list", "", ["prefix-show-bad-words"], ""]

                    }, "", "To show Admin Commands"],
                    "Server admin commands": [{
                        "set-prefix": ["<prefix>", "to change server prefix", "manage messages perms", ["prefix-set-prefix -", "prefix-set-prefix #"], ","],
                        "chat-filter": ["<true / false>", "enable/disable the chat filter (delete bad words)", "manage messages perms", ["prefix-chat-filter Enable", "prefix-chat-filter Disable"], ""],
                        "suggest-room": ["<Text channel>", "to make room for suggestion", "manage messages perms", ["prefix-suggest-room", "prefix-suggest-room room-mention", "prefix-suggest-room room-id"], ""],
                        "reaction-role": ["<message id> <custom emoji> <role>", "to put reaction and make anyone click it it get the role", "manage roles perms", ["prefix-reaction-role msg-id emoji- role-"], ""]

                    }, "", "To show Admin Commands"],

                    "Bot Admin Commands": [{
                        "load": ["<cog name>", "to load cog", "You need to be: The Bot developer", ["prefix-load kick", "prefix-load ban"], ""],
                        "unload": ["<cog name>", "to unload cog", "You need to be: The Bot developer", ["prefix-unload kick", "prefix-unload ban"], ""],
                        "reload": ["<cog name>", "to reload cog", "You need to be: The Bot developer", ["prefix-reload kick", "prefix-reload ban"], ""]
                    }, "", "To show Bot Admin Commands"]
                }
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


def setup(client):
    client.add_cog(General(client))
