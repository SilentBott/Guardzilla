from nextcord.ext import commands
import nextcord
import json
from datetime import datetime, timezone, date
import pymongo


def msg_f(msg: dict):
    name = msg.get("title") if bool(msg.get("title")) else "None"
    values = msg.get("value") if bool(msg.get("value")) else []

    embed = nextcord.Embed(color=0x00ff00, title=name)
    for i in values:
        inline = i[-1] if isinstance(i[-1], bool) else True
        embed.add_field(name=i[0], value=i[1],
                        inline=inline)
    time = datetime.now(timezone.utc).strftime('%Y-%m-%d | %H:%M')

    embed.set_footer(text=f"{time}UTC")
    return embed


class Log(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command()
    async def log(self, ctx, i=None):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        r = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            r = prefix.find_one({"_id": 0})
        if str(message.guild.id) not in log:
            logs.insert_one({"_id": 0})
            r = prefix.find_one({"_id": 0})

        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False, send_messages=False),
            ctx.guild.me: nextcord.PermissionOverwrite(
                read_messages=True, send_messages=False)
        }
        category = await ctx.message.guild.create_category("Logs", reason=None, overwrites=overwrites)

        # log chat; edit, delete message
        chatL = await ctx.message.guild.create_text_channel(f'chat log', category=category)

        # log role; add, remove, edit role
        roleL = await ctx.message.guild.create_text_channel(f'role log', category=category)

        # log voice;swich vc, join vc, leave vc
        vcL = await ctx.message.guild.create_text_channel(f'vc log', category=category)
        # log banned; banned, unbanned, kicked
        bannedL = await ctx.message.guild.create_text_channel(f'kick ban log', category=category)

        # log channel; edited, deleted, added channels
        channelsL = await ctx.message.guild.create_text_channel(f'channel log', category=category)

        # log member; nickname
        memberL = await ctx.message.guild.create_text_channel(f'member log', category=category)

        await chatL.edit(sync_permissions=True)
        await roleL.edit(sync_permissions=True)
        await vcL.edit(sync_permissions=True)
        await bannedL.edit(sync_permissions=True)
        await channelsL.edit(sync_permissions=True)
        await memberL.edit(sync_permissions=True)

        r.update(
            {
                str(ctx.message.guild.id): {
                    "chat": chatL.id,
                    "role": roleL.id,
                    "vc": vcL.id,
                    "banned": bannedL.id,
                    "channel": channelsL.id,
                    "member": memberL.id
                }})

        logs.delete_one({"_id": 0})
        log.insert_one(r)

        embed = nextcord.Embed(
            title="", description="LOG category and its channels\nCreated", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})

        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        try:
            if str(before.guild.id) in log:
                log_c = log[str(before.guild.id)]["chat"]
                if before.content != after.content:

                    embed = msg_f({
                        "title": "Message edited",
                        "value": [["From: ", f"{before.author.name} | {before.author.id}"],
                                  ["Before: ", f"{before.content}"],
                                  ["after: ", f"{after.content}"],
                                  ["channel:",
                                   f"{before.channel.name} | {before.channel.id}"],
                                  ["Msg id:", f"{before.id}"]
                                  ]})
                    channel = await before.guild.fetch_channel(log_c)
                    await channel.send(embed=embed)
                    # message edited
        except AttributeError:
            pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        async for entry in message.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.message_delete):
            deleter = entry.user
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        if str(message.guild.id) in log:
            log_c = log[str(message.guild.id)]["chat"]
            if message.content == "":
                embed = msg_f({
                    "title": "Message Deleted",
                    "value": [
                        ["From: ",
                            f"{message.author.name} | {message.author.id}"],
                        ["The msg: ", "is embed"],
                        ["Deleter: ", f"{deleter.name} | {deleter.id}"],
                        ["channel:",
                            f"{message.channel.name} | {message.channel.id}"],
                        ["Msg id:", message.id]
                    ]})
            else:
                embed = msg_f({
                    "title": "Message Deleted",
                    "value": [
                        ["From: ",
                            f"{message.author.name} | {message.author.id}"],
                        ["The msg: ", f"{message.content}"],
                        ["Deleter: ", f"{deleter.name} | {deleter.id}"],
                        ["channel:",
                            f"{message.channel.name} | {message.channel.id}"],
                        ["Msg id:", message.id]
                    ]})
            channel = await message.guild.fetch_channel(log_c)
            await channel.send(embed=embed)
            # message deleted

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_member_join(self, member):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        if str(member.guild.id) in log:
            log_c = log[str(member.guild.id)]["member"]
            embed = msg_f({
                "title": "Member Joined",
                "value": [["Member: ", f"{member.name} | {member.id}"]]})
            channel = await member.guild.fetch_channel(log_c)
            await channel.send(embed=embed)
            # member joined

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        now = datetime.now(timezone.utc)
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        if str(member.guild.id) in log:
            async for entry in member.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.kick):
                entery = entry
            async for entryy in member.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.ban):
                enteryy = entryy
            if entery.target.id == member.id and abs(entery.created_at - now).total_seconds() < 2:
                log_c = log[str(member.guild.id)]["banned"]
                embed = msg_f({
                    "title": "Member kicked",
                    "value": [
                        ["Member:", f"{member.name} | {member.id}"],
                        ["Kicked By:",
                            f"{entery.user.name} | {entery.user.id}"],
                        ["Reason:", f"{entery.reason}", False]]})
                channel = await member.guild.fetch_channel(log_c)
                await channel.send(embed=embed)
            elif enteryy:
                return
            else:
                log_c = log[str(member.guild.id)]["member"]
                embed = msg_f({
                    "title": "Member Leaved",
                    "value": [
                        ["Member:", f"{member.name} | {member.id}"]]})
                channel = await member.guild.fetch_channel(log_c)
                await channel.send(embed=embed)

            # the messege deleted

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        try:
            if str(before.guild.id) in log:  # nickname changed
                if before.display_name != after.display_name:
                    log_c = log[str(before.guild.id)]["member"]
                    async for entry in before.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.member_update):
                        entery = entry
                    embed = msg_f({
                        "title": "Nickname changed",
                        "value": [
                            ["The account name:", f"{before.name}", False],
                            ["Old:", f"{before.display_name}"],
                            ["New:", f"{after.display_name}"],
                            ["Changed by:",
                             f"{entry.user.name} | {entry.user.id}", False]]})
                    channel = await before.guild.fetch_channel(log_c)
                    await channel.send(embed=embed)
                elif before.roles != after.roles:  # role changed
                    log_c = log[str(before.guild.id)]["role"]
                    async for entry in before.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.member_role_update):
                        entery = entry
                    o = False
                    if len(before.roles) < len(after.roles):  # role removed
                        embed = msg_f({
                            "title": "Role added",
                            "value": [
                                ["TO:", f"{before.name} | {before.id}"],
                                ["By:", f"{entery.user.name} | {entery.user.id}"],
                                ["Role:", f"{entery.changes.after.roles[0].name} | {entery.changes.after.roles[0].id}"]]})
                        o = True
                    elif len(before.roles) > len(after.roles):
                        embed = msg_f({
                            "title": "Role removed",
                            "value": [
                                ["From:", f"{before.name} | {before.id}"],
                                ["By:", f"{entery.user.name} | {entery.user.id}"],
                                ["Role:", f"{entery.changes.before.roles[0].name} | {entery.changes.before.roles[0].id}"]]})
                        o = True
                    if o:
                        channel = await before.guild.fetch_channel(log_c)
                        await channel.send(embed=embed)
        except AttributeError:
            pass

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if after.bot:
            return
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        try:
            if str(before.guild.id) in log:
                if before.name != after.name:
                    log_c = log[str(before.guild.id)]["member"]
                    embed = msg_f({
                        "title": "name changed",
                        "value": [
                            ["Old:", f"{before.name}"],
                            ["New:", f"{after.name}"]]})
                    channel = await before.guild.fetch_channel(log_c)
                    await channel.send(embed=embed)
                    # username changed
                elif before.discriminator != after.discriminator:
                    log_c = log[str(before.guild.id)]["member"]
                    embed = msg_f({
                        "title": "discriminator changed",
                        "value": [
                            ["Old:", f"{before.discriminator}"],
                            ["New:", f"{after.discriminator}"]]})
                    channel = await before.guild.fetch_channel(log_c)
                    await channel.send(embed=embed)
                    # discriminator changed
                elif before.avatar.url != after.avatar.url:
                    log_c = log[str(before.guild.id)]["member"]
                    embed = msg_f({
                        "title": "avatar changed",
                        "value": [
                            ["Old:", f"{before.avatar.url}"],
                            ["New:", f"{after.avatar.url}"]]})
                    channel = await before.guild.fetch_channel(log_c)
                    await channel.send(embed=embed)
                    # avatar changed
        except AttributeError:
            pass

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        if str(role.guild.id) in log:
            log_c = log[str(role.guild.id)]["role"]
            async for entry in role.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.role_create):
                entery = entry
            embed = msg_f({
                "title": "Role created",
                "value": [
                    ["Role:", f"{role.name} | {role.id}"],
                    ["Created by", f"{entery.user.name} | {entery.user.id}"],
                    ["Permissions", ', '.join([perm[0].replace("_", " ") for perm in role.permissions if perm[1]]), False]]})
            channel = await role.guild.fetch_channel(log_c)
            await channel.send(embed=embed)
            # role created

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        if str(role.guild.id) in log:
            log_c = log[str(role.guild.id)]["role"]
            async for entry in role.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.role_delete):
                entery = entry
            embed = msg_f({
                "title": "Role deleted",
                "value": [
                    ["Role:", f"{role.name} | {role.id}"],
                    ["Deleted by", f"{entery.user.name} | {entery.user.id}"]]})
            channel = await role.guild.fetch_channel(log_c)
            await channel.send(embed=embed)
            # role deleted

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        try:
            if str(before.guild.id) in log:
                async for entry in before.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.role_update):
                    entery = entry
                if entry.target.id != before.id:
                    return
                print(before, after)
                log_c = log[str(before.guild.id)]["role"]
                r = [perm[0].replace(
                    "_", " ").replace("guild", "server") for perm in before.permissions if perm not in after.permissions and perm[1]]
                a = [perm[0].replace(
                    "_", " ").replace("guild", "server") for perm in after.permissions if perm not in before.permissions and perm[1]]
                s = []
                if after.name == before.name:
                    s.append(
                        ["Role Name:", f"{before.name} | {before.id}"])
                else:
                    s.append(
                        ["Old name:", f"{before.name} | {before.id}"])
                    s.append(
                        ["New name:", f"{after.name} | {after.id}"])
                s.append(["Added Permissions", ", ".join(
                    a if len(a) != 0 else ["No added perms"]), False])
                s.append(["Removed Permissions", ", ".join(
                    r if len(r) != 0 else ["No removed perms"])])

                msg = {
                    "title": "Role edited",
                    "value": s}

                embed = msg_f(msg)
                channel = await before.guild.fetch_channel(log_c)
                await channel.send(embed=embed)
                # role edited
        except AttributeError:
            pass

    @ commands.guild_only()
    @ commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        check_l = None
        if before.channel is None:
            check_l = after.channel
        elif after.channel is None:
            check_l = before.channel
        else:
            check_l = before.channel or after.channel
        if str(check_l.guild.id) in log:
            log_c = log[str(check_l.guild.id)]["vc"]
            if before.channel is None and after.channel is not None:
                msg = {"title": "Join VC", "value": [["Member", f"{member.name} | {member.id}", False],
                                                     ["Joining to:", f"{after.channel.name} | {after.channel.id}"]]}
                # join vc
            elif after.channel is None and before.channel is not None:
                msg = {"title": "Leave VC", "value": [["Member", f"{member.name} | {member.id}", False],
                                                      ["Leaving from:", f"{before.channel.name} | {before.channel.id}"]]}
                # leave vc
            else:
                if before.channel.id == after.channel.id:
                    return
                msg = {"title": "Switch VC", "value": [["Member", f"{member.name} | {member.id}", False], ["Switching from:", f"{before.channel.name} | {before.channel.id}"], [
                    "Switching to:", f"{after.channel.name} | {after.channel.id}"]]}
                # switch vc
            embed = msg_f(msg)
            channel = await check_l.guild.fetch_channel(log_c)
            await channel.send(embed=embed)

    @ commands.guild_only()
    @ commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        if str(guild.id) in log:
            async for entry in guild.audit_logs(limit=1, action=nextcord.AuditLogAction.ban):
                entery = entry
            log_c = log[str(guild.id)]["banned"]
            embed = msg_f({
                "title": "Member Banned",
                "value": [
                    ["Member:", f"{user.name} | {user.id}"],
                    ["Banned By:",
                        f"{entery.user.name} | {entery.user.id}"],
                    ["Reason:", f"{entery.reason}", False]]})
            channel = await guild.fetch_channel(log_c)
            await channel.send(embed=embed)

            # member banned

    @ commands.guild_only()
    @ commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        if str(guild.id) in log:
            async for entry in guild.audit_logs(limit=1, action=nextcord.AuditLogAction.unban):
                entery = entry
            log_c = log[str(guild.id)]["banned"]
            embed = msg_f({
                "title": "Member Unbanned",
                "value": [
                    ["Member:", f"{user.name} | {user.id}"],
                    ["Unbanned By:",
                        f"{entery.user.name} | {entery.user.id}"]]})
            channel = await guild.fetch_channel(log_c)
            await channel.send(embed=embed)

    @ commands.guild_only()
    @ commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        if str(channel.guild.id) in log:
            async for entry in channel.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.channel_create):
                entery = entry
            log_c = log[str(channel.guild.id)]["channel"]
            embed = msg_f({
                "title": "Channel created",
                "value": [
                    ["Channel:", f"{channel.name} | {channel.id}"],
                    ["Created By:",
                        f"{entery.user.name} | {entery.user.id}"]]})
            channell = await channel.guild.fetch_channel(log_c)
            await channell.send(embed=embed)

    @ commands.guild_only()
    @ commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        logs = cluster["logs"]
        log = logs.find_one({"_id": 0})
        if not log:
            logs.insert_one({"_id": 0})
            log = prefix.find_one({"_id": 0})
        if str(channel.guild.id) in log:
            async for entry in channel.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.channel_create):
                entery = entry
            log_c = log[str(channel.guild.id)]["channel"]
            embed = msg_f({
                "title": "Channel deleted",
                "value": [
                    ["Channel:", f"{channel.name} | {channel.id}"],
                    ["Deleted By:",
                        f"{entery.user.name} | {entery.user.id}"]]})
            channell = await channel.guild.fetch_channel(log_c)
            await channell.send(embed=embed)


def setup(client):
    client.add_cog(Log(client))
