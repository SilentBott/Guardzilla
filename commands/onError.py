import os
import nextcord
from nextcord.ext import commands
import pymongo


def bot_admin(ctx):
    db = pymongo.MongoClient(os.environ["mongoDBclient"])['settings']
    bot_admin = db["bot_admins"]
    admin = bot_admin.find_one({"_id": 0})
    if not admin:
        bot_admin.insert_one({"_id": 0, "Admins": ["821486817957642242"]})
        admin = bot_admin.find_one({"_id": 0})

    is_admin = str(ctx.message.author.id) in admin["Admins"][0]
    return is_admin


class OnCommandError(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.allCommands = []
        for pyFile in os.listdir("./commands"):
            if pyFile.endswith(".py"):
                self.allCommands.append(pyFile[:-3])

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        msg = ctx.message.content
        command = str(msg).split(" ")[0][1:]
        prefix = str(msg)[0]
        if isinstance(error, commands.errors.MissingRequiredArgument):
            try:
                r = {
                    "Home": [{}, "", ""],
                    "General Commands": [{
                        "ticket":
                        ["", "to make tickets", "", ["prefix-ticket"], ""]
                    }, "", "To show General Commands"],
                    "Admin Commands": [{
                        "kick": [
                            "<member> [reason]", "to kick someone",
                            "Kick members perms", [], "922786678454771742"
                        ],
                        "ban": [
                            "<member> [reason]", "to ban someone",
                            "Ban members perms", [], "922790457556226078"
                        ],
                        "unban": [
                            "<member>", "to unban someone",
                            "Ban members perms", [], ""
                        ],
                        "add-bad-words": [
                            "[words]",
                            "to make reaction that if any one pressed it will get role",
                            "manage messages perms",
                            ["prefix-add-bad-words f*** trash"], ""
                        ],
                        "remove-bad-words": [
                            "[words]", "to remove the bad words in the list",
                            "manage messages perms",
                            ["prefix-remove-bad-words f*** trash"], ""
                        ],
                        "clear": [
                            "<number> <member> <channel>",
                            "to clear messages in a channel / to clear messages from someone only in the last 100 msg on each channel",
                            "manage messages perms",
                            ["prefix-clear 1", "prefix-clear 20"], ""
                        ],
                        "mute": [
                            "<member>",
                            "to make someone unable to send messages in text channels",
                            "manage messages perms", [], ""
                        ],
                        "unmute": [
                            "<member>",
                            "to Cancel the effect of the mute command",
                            "manage messages perms", [], ""
                        ],
                        "hide": [
                            "<channel>",
                            "Make any channel unvisible to normal people",
                            "manage messages perms",
                            [
                                "prefix-hide room-mention",
                                "prefix-show room-id"
                            ], ""
                        ],
                        "show": [
                            "<channel>",
                            "Make any channel visible to normal people",
                            "manage messages perms",
                            [
                                "prefix-show room-mention",
                                "prefix-show room-id"
                            ], ""
                        ],
                        "nick": [
                            "<member> [nick name]",
                            "to change member nickname",
                            "manage nicknames perms",
                            ["prefix-nick member-id Awsome person"], ""
                        ],
                        "embed": [
                            "[phrase]",
                            "to make reaction that if any one pressed it will get role",
                            "manage messages perms", ["prefix-embed Hi all"],
                            ""
                        ],
                        "warn": [
                            "<member> [reason]", "to warn someone",
                            "manage messages perms",
                            [
                                "prefix-warn member-id",
                                "prefix-warn member-mention cuz i hate him/her"
                            ], ""
                        ],
                        "removewarn": [
                            "<member> <number>", "to remove warn from someone",
                            "manage messages perms",
                            [
                                "prefix-removewarn member-id 1",
                                "prefix-warn member-mention 2"
                            ], ""
                        ],
                        "show-bad-words": [
                            "", "to show bad words list", "",
                            ["prefix-show-bad-words"], ""
                        ]
                    }, "", "To show Admin Commands"],
                    "Server admin commands": [{
                        "set-prefix": [
                            "<prefix>", "to change server prefix",
                            "manage messages perms",
                            ["prefix-set-prefix -", "prefix-set-prefix #"], ","
                        ],
                        "chat-filter": [
                            "<true / false>",
                            "enable/disable the chat filter (delete bad words)",
                            "manage messages perms",
                            [
                                "prefix-chat-filter Enable",
                                "prefix-chat-filter Disable"
                            ], ""
                        ],
                        "suggest-room": [
                            "<Text channel>", "to make room for suggestion",
                            "manage messages perms",
                            [
                                "prefix-suggest-room",
                                "prefix-suggest-room room-mention",
                                "prefix-suggest-room room-id"
                            ], ""
                        ],
                        "reaction-role": [
                            "<message id> <custom emoji> <role>",
                            "to put reaction and make anyone click it it get the role",
                            "manage roles perms",
                            ["prefix-reaction-role msg-id emoji- role-"], ""
                        ]
                    }, "", "To show Admin Commands"],
                    "Bot Admin Commands": [{
                        "load": [
                            "<cog name>", "to load cog",
                            "You need to be: The Bot developer",
                            ["prefix-load kick", "prefix-load ban"], ""
                        ],
                        "unload": [
                            "<cog name>", "to unload cog",
                            "You need to be: The Bot developer",
                            ["prefix-unload kick", "prefix-unload ban"], ""
                        ],
                        "reload": [
                            "<cog name>", "to reload cog",
                            "You need to be: The Bot developer",
                            ["prefix-reload kick", "prefix-reload ban"], ""
                        ]
                    }, "", "To show Bot Admin Commands"]
                }
                if not bot_admin(ctx):
                    r.pop("Bot Admin Commands")
                cm = {}
                for i in r:
                    for ii in r[i][0]:
                        if i != "Home page":
                            cm.update({str(ii): list(r[i][0][ii])})
                cm = cm[command]
                usage = cm[0]
                description = cm[1]
                needing = cm[2]
                examples = cm[3]
                if bool(examples):
                    emm = self.client.get_emoji(932702977976836136)
                    example_val = f"\n".join([
                        x.replace("prefix-",
                                  prefix).replace("member-mention",
                                                  ctx.author.mention).
                        replace("member-id", f"{ctx.author.id}").replace(
                            "msg-id", f"{ctx.message.id}").replace(
                                "role-",
                                str(ctx.guild.roles[1].mention)).replace(
                                    "emoji-", f"{emm}").replace(
                                        "room-mention",
                                        f"{ctx.channel.mention}").replace(
                                            "room-id", f"{ctx.channel.id}")
                        for x in examples
                    ])
                else:
                    example_val = f"{prefix}{command} {ctx.author.mention}\n{prefix}{command} {ctx.author.id}"
                embedVar = nextcord.Embed(title=f"Command: {command}",
                                          description=f"{description}",
                                          color=0x00ff00)
                embedVar.add_field(name="Usage: ",
                                   value=f"{prefix}{command} {usage}",
                                   inline=False)
                if needing != '':
                    embedVar.add_field(name="Permission requirements: ",
                                       value=needing,
                                       inline=False)
                embedVar.add_field(name="Examples: ",
                                   value=example_val,
                                   inline=False)
                await ctx.reply(embed=embedVar)
            except KeyError:
                pass
                # await ctx.reply("Please tell The Bot maker to add help to this command")
        elif isinstance(error, commands.errors.CommandNotFound):
            if str(msg).split(" ")[0].replace(prefix, '') in self.allCommands:
                await ctx.send(
                    f"Sorry but the Bot admin disabled the command for now")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply(f"Missing permissions {error}")
        else:
            print(error)


def setup(client):
    client.add_cog(OnCommandError(client))


"""
{
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
"""
