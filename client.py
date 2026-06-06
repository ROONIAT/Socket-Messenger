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




#Implementation of Phase 1&2
"""
async def receive_messages(websocket):
    try:
        async for message in websocket:
            print(f"\n[Server]: {message}")
            print("> ", end="", flush=True) 
    except websockets.ConnectionClosed:
        print("\n[!] Error: Server disconnected!")
        return # پایان این تسک

async def send_messages(websocket):
    loop = asyncio.get_event_loop()
    try:
        while True:
            msg = await loop.run_in_executor(None, input, "> ")

            if msg.lower() == "/exit":
                await websocket.close()
                break

            await websocket.send(msg)
    except websockets.ConnectionClosed:
        pass

async def main():
    try:
        async with websockets.connect(URI) as ws:
            print("Successfully connected to the server.")
            print("Type your message and press Enter. Type '/exit' to quit.")

            receive_task = asyncio.create_task(receive_messages(ws))
            send_task = asyncio.create_task(send_messages(ws))

            done, pending = await asyncio.wait(
                [receive_task, send_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()

            print("Exiting application...")

    except Exception as e:
        print(f"Connection failed: {e}")

if name == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient stopped.")
"""
