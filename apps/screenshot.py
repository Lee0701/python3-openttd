
import asyncio
import sys
import datetime
import bot

async def launch(client, args):
    [map_types] = args

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

async def main(hostname, port, password, map_types):
    client = await bot.connect(hostname, port, password)
    args = [map_types]
    await launch(client, args)
    await bot.disconnect(client)

if __name__ == "__main__":
    [hostname, port, password, type] = sys.argv[1:]
    asyncio.run(main(hostname, int(port), password, type))
