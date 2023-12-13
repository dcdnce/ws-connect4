#!/usr/bin/_env_python
import asyncio
import websockets
import json
import secrets
from connect4 import PLAYER1, PLAYER2, Connect4

JOIN = {}

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

        # Temporary - for testing.
        print("first player started game", id(game))
        async for message in websocket:
            print("first player sent", message)

    finally:
        del JOIN[join_key]

async def handler(websocket):
    # Receive and parse the "init" event from the UI.
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    # First player starts a new game.
    await start(websocket)

#    # Initialize a Connect Four game
#    game = Connect4()
#    async for message in websocket:
#        event = json.loads(message)
#
#        if event["type"] != "play":
#            await websocket.send("wrong event type")
#            continue
#
#        currentRow = 0;
#        currentColumn = event["column"]
#        currentPlayer = PLAYER1 if game.last_player == PLAYER2 else PLAYER2
#
#        try:
#            currentRow = game.play(currentPlayer, event["column"])
#        except RuntimeError as e:
#            await websocket.send(str(e))
#            continue
#
#        if game.last_player_won:
#            response = {
#                    "type": "win",
#                    "player": game.last_player
#            }
#            await websocket.send(json.dumps(response))
#        else:
#            response = {
#                    "type": "play",
#                    "player": game.last_player,
#                    "column": str(currentColumn),
#                    "row": str(currentRow)
#            }
#            await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()
    
if __name__ == "__main__":
    asyncio.run(main())
