#!/usr/bin/_env_python
import asyncio
import websockets
import json
from connect4 import PLAYER1, PLAYER2, Connect4

async def handler(websocket):
    # Initialize a Connect Four game
    game = Connect4()
    async for message in websocket:
        event = json.loads(message)

        if event["type"] != "play":
            await websocket.send("wrong event type")
            continue

        currentRow = 0;
        currentColumn = event["column"]
        currentPlayer = PLAYER1 if game.last_player == PLAYER2 else PLAYER2

        try:
            currentRow = game.play(currentPlayer, event["column"])
        except RuntimeError as e:
            await websocket.send(str(e))
            continue

        if game.last_player_won:
            response = {
                    "type": "win",
                    "player": game.last_player
            }
            await websocket.send(json.dumps(response))
        else:
            response = {
                    "type": "play",
                    "player": game.last_player,
                    "column": str(currentColumn),
                    "row": str(currentRow)
            }
            await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()
    
if __name__ == "__main__":
    asyncio.run(main())
