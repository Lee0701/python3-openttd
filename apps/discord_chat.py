
import asyncio
import sys
import discord
import bot
import openttd.admin
import openttd.info

async def launch(ttd_client, args):
    [token, channel_id] = args
    intents = discord.Intents.default()
    intents.message_content = True
    discord_client = discord.Client(intents=intents)

    def log_message(message):
        print(message)

    async def broadcast_to_discord(source, author, text):
        if text == '':
            return
        content = f'[{source}] {author}: {text}'
        log_message(content)
        await discord_client.get_channel(int(channel_id)).send(content)

    async def broadcast_to_ttd(source, author, text):
        if text == '':
            return
        content = f'[{source}] {author}: {text}'
        log_message(content)
        await ttd_client.rcon_command(f'say "{content}"')

    async def handle_ttd_chat(info):
        if info.desttype != openttd.info.DestType.BROADCAST:
            return
        if info.dest == 1:
            return
        name = (await ttd_client.poll_client_info(info.dest)).name
        await broadcast_to_discord('TTD', name, info.msg)

    async def handle_discord_chat(message):
        if message.author == discord_client.user:
            return
        if message.channel.id!= int(channel_id):
            return
        await broadcast_to_ttd('Discord', message.author.display_name, message.content)

    def ttd_chat_callback(info):
        asyncio.create_task(handle_ttd_chat(info))

    ttd_client.subscribe_callback_to_push(
        openttd.admin.UpdateType.CHAT,
        ttd_chat_callback
    )

    @discord_client.event
    async def on_message(message):
        await handle_discord_chat(message)

    await discord_client.start(token)
    await ttd_client.disconnected_event.wait()

async def main(hostname, port, password, token, channel_id):
    client = await bot.connect(hostname, port, password)
    args = [token, channel_id]
    await launch(client, args)
    await bot.disconnect(client)

if __name__ == "__main__":
    [hostname, port, password, token, channel_id] = sys.argv[1:]
    asyncio.run(main(hostname, int(port), password, token, channel_id))
