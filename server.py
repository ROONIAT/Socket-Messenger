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





#Implementation of Phase 1

"""
async def handler(websocket):
    print("Client connected.")
    first_message_received = False

    try:
        async for message in websocket:
            print("Client says:", message)

            if not first_message_received:
                await websocket.send("Hello Client!")
                first_message_received = True

    except websockets.ConnectionClosed:
        pass
    finally:
        print("Client disconnected.")

async def main():
    print(f"Server running on ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

"""

