import asyncio
import websockets

# This handler will be called for each new client connection
async def handler(websocket):
    print("A client connected!")
    try:
        # Wait for messages from the client
        async for message in websocket:
            print(f"Received message: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("A client disconnected.")

async def main():
    # Start the WebSocket server on localhost, port 8765
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server is running at ws://localhost:8765")
        await asyncio.Future()  # Keep the server running forever

if __name__ == "__main__":
    asyncio.run(main())
