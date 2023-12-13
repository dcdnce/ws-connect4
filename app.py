#!/usr/bin/_env_python
import asyncio
import websockets
import json
import secrets
from connect4 import PLAYER1, PLAYER2, Connect4

JOIN = {}

async def error(websocket, message):
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))

async def start(websocket):
    # Init game inst
    game = Connect4()
    # Init set of WebSocket connections receiving moves
    connected = {websocket}
    # Init secret token.
    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    try:
        event = {
            "type": "init",
            "join": join_key,
        }
        await websocket.send(json.dumps(event))
        
        # Game loop
        await play(websocket, game, PLAYER1, connected)

    finally:
        del JOIN[join_key]

async def join(websocket, join_key):
    # Find the Connect Four game.
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        print(join_key)
        await error(websocket, "Game not found.")
        return

    # Register to receive moves from this game.
    connected.add(websocket)

    try:
        await play(websocket, game, PLAYER2, connected)

    finally:
        connected.remove(websocket)


async def handler(websocket):
    # Receive and parse the "init" event from the UI.
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    # Second player joins an existing game.
    # First player starts a new game.
    if "join" in event:
        await join(websocket, event["join"])
    else:
        await start(websocket)

async def play(websocket, game, player, connected):
    async for message in websocket:
        event = json.loads(message)

        if event["type"] != "play":
            await error(websocket, "Wrong event type.")
            continue

        currentRow = 0;
        currentColumn = event["column"]

        try:
            currentRow = game.play(player, event["column"])
        except RuntimeError as e:
            await websocket.send(str(e))
            continue

        if game.last_player_won:
            response = {
                    "type": "win",
                    "player": game.last_player
            }
            for ws in connected:
                await ws.send(json.dumps(response));
            return ;
        else:
            response = {
                    "type": "play",
                    "player": game.last_player,
                    "column": str(currentColumn),
                    "row": str(currentRow)
            }
            for ws in connected:
                await ws.send(json.dumps(response));

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()
    
if __name__ == "__main__":
    asyncio.run(main())
