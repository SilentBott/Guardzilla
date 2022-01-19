import os
import nextcord
import json
from nextcord.ext import commands


def bot_admin(ctx):
    with open("./bot_admin.json", ) as f:
        is_admin = str(ctx.message.author.id) in json.loads(
            f.read())["Admins"][0]
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
                with open("./commands.json", ) as f:
                    r = json.loads(f.read())
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
                    print(emm)
                    example_val = f"\n".join([x.replace("prefix-", prefix).replace("member-mention", ctx.author.mention).
                                             replace("member-id", f"{ctx.author.id}").
                                              replace("msg-id", f"{ctx.message.id}").replace("role-", str(ctx.guild.roles[1].mention)).
                                              replace("emoji-", f"{emm}").
                                             replace("room-mention", f"{ctx.channel.mention}").
                                             replace("room-id", f"{ctx.channel.id}") for x in examples])
                else:
                    example_val = f"{prefix}{command} {ctx.author.mention}\n{prefix}{command} {ctx.author.id}"
                embedVar = nextcord.Embed(
                    title=f"Command: {command}", description=f"{description}", color=0x00ff00)
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
                pass
                # await ctx.reply("Please tell The Bot maker to add help to this command")
        elif isinstance(error, commands.errors.CommandNotFound):
            if str(msg).split(" ")[0].replace(prefix, '') in self.allCommands:
                await ctx.send(f"Sorry but the Bot admin disabled the command for now")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply(f"Missing permissions {error}")
        elif isinstance(error, commands.errors.CheckFailure):
            pass
        elif isinstance(error, commands.errors.NoPrivateMessage):
            pass


def setup(client):
    client.add_cog(OnCommandError(client))


"""
    "Bot Commands": [{
        "bot": ["", "to see The bot's informations", "", ["prefix-bot"], ""],
    }, "", "To show Bot Commands"],

"""
