import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import parse_pre, sanga_seperator


@bot.on(admin_cmd(pattern="(sg|sgu)($| (.*))"))
@bot.on(sudo_cmd(pattern="(sg|sgu)($| (.*))", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_delete(
            event,
            "__reply to  user's text message to get name/username history or give userid/username__",
        )
    if input_str:
        try:
            uid = int(input_str)
        except ValueError:
            try:
                u = await event.client.get_entity(input_str)
            except ValueError:
                await edit_delete(
                    event, "__Give userid or username to find name history__"
                )
            uid = u.id
    else:
        uid = reply_message.sender_id
    chat = "@SangMataInfo_bot"
    catevent = await edit_or_reply(event, "__Processing...__")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"/search_id {uid}")
        except YouBlockedUserError:
            await edit_delete(catevent, "__unblock @Sangmatainfo_bot and then try__")
        responses = []
        while True:
            try:
                response = await conv.get_response(timeout=2)
            except asyncio.TimeoutError:
                break
            responses.append(response.text)
        await event.client.send_read_acknowledge(conv.chat_id)
    if not responses:
        await edit_delete(catevent, "__bot can't fetch results__")
    if "No records found" in responses:
        await edit_delete(catevent, "__The user doesn't have any record__")
    names, usernames = await sanga_seperator(responses)
    cmd = event.pattern_match.group(1)
    if cmd == "sg":
        sandy = None
        for i in names:
            if sandy:
                await event.reply(i, parse_mode=parse_pre)
            else:
                sandy = True
                await catevent.edit(i, parse_mode=parse_pre)
    elif cmd == "sgu":
        sandy = None
        for i in usernames:
            if sandy:
                await event.reply(i, parse_mode=parse_pre)
            else:
                sandy = True
                await catevent.edit(i, parse_mode=parse_pre)


CMD_HELP.update(
    {
        "sangmata": "**Plugin : **__sangmata__\
    \n\n**Syntax : **__.sg <username/userid/reply>__\
    \n**Function : **__Shows you the previous name history of user.__\
    \n\n**Syntax : **__.sgu <username/userid/reply>__\
    \n**Function : **__Shows you the previous username history of user.__\
    "
    }
)