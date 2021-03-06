from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError


@bot.on(admin_cmd(pattern="ctg$", outgoing=True))
@bot.on(sudo_cmd(pattern="ctg$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    if not reply_message:
        await edit_or_reply(event, "______Reply to a Link.______")
        return
    if not reply_message.text:
        await edit_or_reply(event, "______Reply to a Link______")
        return
    chat = "@chotamreaderbot"
    catevent = await edit_or_reply(event, "______Processing______")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=272572121)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit(
                "__RIP Check Your Blacklist Boss and unblock @chotamreaderbot__"
            )
            return
        if response.text.startswith(""):
            await catevent.edit("Am I Dumb Or Am I Dumb?")
        else:
            await catevent.delete()
            await event.client.send_message(event.chat_id, response.message)


CMD_HELP.update(
    {
        "linkpreview": "**Plugin : **__linkpreview__\
    \n\n**Syntax : **__.ctg__ reply to link\
    \n**Function : **Converts the given link to link preview"
    }
)
