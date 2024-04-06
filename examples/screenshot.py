
import asyncio
import openttd.admin
import openttd.packet
import logging
import sys
import datetime

async def main(hostname, port, password):
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
    
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    await client.rcon_command(f'screenshot minimap "map {now}"')
    await client.rcon_command(f'screenshot topography "topo {now}"')

    await client.disconnect()

if __name__ == "__main__":
    [hostname, port, password] = sys.argv[1:]
    asyncio.run(main(hostname, int(port), password))
