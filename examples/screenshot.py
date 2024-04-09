
import asyncio
import openttd.admin
import openttd.packet
import logging
import sys
import datetime

async def main(hostname, port, password, type):
    logger = logging.getLogger(__name__ + '.main')
    client = openttd.admin.Client()
    client.on_error = logger.error
    try:
        await client.connect_tcp(hostname, port)
    except OSError as err:
        print("failed to connect:", err, file=sys.stderr)
        return

    try:
        await client.authenticate(
            password,
            "cameraman",
            "devel")
    except:
        logger.exception("during authentication: ")
        return

    logger.info("Connected to server: %s", client.server_info.name)

    sys_date = await client.rcon_command(f'getsysdate')
    sys_date = [d for _, d in sys_date][0]
    game_date = await client.rcon_command(f'getdate')
    game_date = [d for _, d in game_date][0]

    sys_date, game_date = [d.split(':')[1].strip() for d in [sys_date, game_date]]
    
    # print(f'system date: {sys_date}, game date: {game_date}')

    allowed_types = ['minimap', 'topography', 'industry']
    if type not in allowed_types:
        print(f'invalid type: {type}')
        return

    filename = f'screenshot_{type}_{sys_date}_{game_date}'
    await client.rcon_command(f'screenshot {type} "{filename}"')

    await client.disconnect()

if __name__ == "__main__":
    [hostname, port, password, type] = sys.argv[1:]
    asyncio.run(main(hostname, int(port), password, type))
