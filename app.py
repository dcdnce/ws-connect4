#!/usr/bin/_env_python
import asyncio
import websockets

async def handler(websocket):
    while (True):
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        print(message)

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()
    
if __name__ == "__main__":
    asyncio.run(main())