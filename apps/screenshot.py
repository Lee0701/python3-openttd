
import asyncio
import openttd.admin
import openttd.packet
import logging
import sys
import datetime

async def main(hostname, port, password, map_types):
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

    sys_date = datetime.datetime.now().isoformat(timespec='seconds')

    game_date = await client.rcon_command(f'getdate')
    game_date = [d for _, d in game_date][0]
    game_date = game_date.split(':')[1].strip()

    allowed_map_types = ['minimap', 'topography', 'industry']
    map_types = map_types.split(',')
    for map_type in map_types:
        if map_type not in allowed_map_types:
            print(f'invalid type: {map_type}')
            return
        filename = f'screenshot_{sys_date}_{game_date}_{map_type}'
        await client.rcon_command(f'screenshot {map_type} "{filename}"')

    await client.disconnect()

if __name__ == "__main__":
    [hostname, port, password, type] = sys.argv[1:]
    asyncio.run(main(hostname, int(port), password, type))
