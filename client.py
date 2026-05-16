import asyncio
import websockets

URI = "ws://localhost:8765"

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
