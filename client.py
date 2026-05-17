import asyncio
import websockets
import sys

URI = "ws://localhost:8765"

async def sender(ws):
    while True:
        msg = await asyncio.to_thread(sys.stdin.readline)
        msg = msg.strip()

        if msg == "":
            continue

        await ws.send(msg)

        if msg.lower() == "/exit":
            break

async def receiver(ws):
    try:
        async for msg in ws:
            print(msg)
    except websockets.ConnectionClosed:
        print("Disconnected from server.")

async def main():
    async with websockets.connect(URI) as ws:

        username = input("Enter username: ")
        await ws.send(username)

        await asyncio.gather(
            sender(ws),
            receiver(ws)
        )

if __name__ == "__main__":
    asyncio.run(main())




#Implementation of Phase 1
"""
async def main():
    async with websockets.connect(URI) as ws:
        print("Connected. Type a message (or /exit to quit).")

        first = True

        while True:
            msg = input("> ")

            if msg.strip() == "":
                continue

            if msg == "/exit":
                print("Closing connection...")
                break

            await ws.send(msg)

            if first:
                reply = await ws.recv()
                print("Server replied:", reply)
                first = False

if __name__ == "__main__":
    asyncio.run(main())
"""
