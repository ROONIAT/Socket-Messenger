import asyncio
import websockets

HOST = "localhost"
PORT = 8765

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
