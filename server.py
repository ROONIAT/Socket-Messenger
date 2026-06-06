import asyncio
import websockets
import json

HOST = "localhost"
PORT = 8765

# {websocket: username}
clients = {}


async def broadcast(message, exclude=None):
    if clients:
        await asyncio.gather(
            *(client.send(message)
              for client in clients
              if client != exclude)
        )


async def send_private(sender, target_username, text):
    target_socket = None

    for client, username in clients.items():

        if username == target_username:
            target_socket = client
            break

    if target_socket:

        await target_socket.send(
            json.dumps({
                "type": "private",
                "from": sender,
                "to": target_username,
                "message": text
            })
        )

        for client, username in clients.items():

            if username == sender:

                await client.send(
                    json.dumps({
                        "type": "private_sent",
                        "from": sender,
                        "to": target_username,
                        "message": text
                    })
                )
                break

    else:
        for client, username in clients.items():

            if username == sender:

                await client.send(
                    json.dumps({
                        "type": "system",
                        "message": f"User '{target_username}' not found."
                })
                )
                break


async def handler(websocket):

    try:
        username = await websocket.recv()

    except websockets.ConnectionClosed:
        return

    clients[websocket] = username

    print(f"{username} connected.")

    for user in clients.values():
        if user != username:
            await websocket.send(
                json.dumps({
                    "type": "join",
                    "user": user
                })
            )


    await broadcast(
        json.dumps({
            "type": "join",
            "user": username
        }),
    )

    try:

        async for message in websocket:

            if message.lower() == "/exit":
                break

            if message.startswith("@"):

                parts = message.split(" ", 1)

                if len(parts) < 2:
                    continue

                target_username = parts[0][1:]
                private_text = parts[1]

                print(
                    f"[PRIVATE] {username} -> {target_username}: {private_text}"
                )

                await send_private(
                    username,
                    target_username,
                    private_text
                )

            else:

                await broadcast(
                    json.dumps({
                        "type": "public",
                        "from": username,
                        "message": message
                    })
                )

                print(
                    f"[public] {username} : {message}"
                )

    except websockets.ConnectionClosed:
        pass

    finally:

        if websocket in clients:

            user_leaving = clients[websocket]

            del clients[websocket]

            print(f"{user_leaving} disconnected.")

            await broadcast(
                json.dumps({
                    "type": "left",
                    "user": user_leaving
                })
            )


async def main():

    print(f"Server running on ws://{HOST}:{PORT}")

    async with websockets.serve(handler, HOST, PORT):

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())





#Implementation of Phase 1&2

"""
async def handler(websocket):
    client_ip, client_port, *unused = websocket.remote_address
    client_id = f"{client_ip}:{client_port}" 

    print(f"[+] New connection: {client_id}")

    try:
        async for message in websocket:
            print(f"[{client_id}] says: {message}")

            await websocket.send(f"Server received your message: {message}")

    except websockets.ConnectionClosed:
        pass
    finally:
        print(f"[-] Connection closed: {client_id}")

async def main():
    print(f"--- Server running on ws://{HOST}:{PORT} ---")
    async with websockets.serve(handler, HOST, PORT, ping_interval=20, ping_timeout=20):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")

"""

