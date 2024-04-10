
import sys
import openttd.admin
import openttd.packet

async def connect(hostname, port, password):
    client = openttd.admin.Client()
    try:
        await client.connect_tcp(hostname, port)
    except OSError as err:
        print("failed to connect:", err, file=sys.stderr)
        return

    await client.authenticate(
        password,
        "bot",
        "devel")

    print("Connected to server: %s" % client.server_info.name)

    return client

async def disconnect(client):
    client.disconnect()
