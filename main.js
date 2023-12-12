import { createBoard, playMove } from "./connect4.js";

window.addEventListener("DOMContentLoaded", () => {
	// Initialize the UI
	const board = document.querySelector(".board");
	createBoard(board);

	// Open the WebSocket connection 
	const websocket = new WebSocket("ws://localhost:8001/");
	// Register event handlers
	sendMoves(board, websocket);
	receivesMoves(board, websocket);
});

function sendMoves(board, websocket) {
	// When clicking a column, send a "play" event for a move in that column.
	board.addEventListener("click", ({ target }) => {
		const column = target.dataset.column;
		if (column === undefined)
			return ;
		const newEvent = {
			type: 'play',
			column: parseInt(column, 10),
		};
		websocket.send(JSON.stringify(newEvent));
	});
}

function showMessage(message) {
	window.setTimeout(() => window.alert(message), 50);
}

function receivesMoves(board, websocket) {
	websocket.addEventListener("message", ({ data }) => {
		const event = JSON.parse(data);
		switch (event.type) {
			case "play":
				// Update the UI with the move.
				playMove(board, event.player, event.column, event.row);
				break;
		 	case "win":
				showMessage(`Player ${event.player} wins!`);
				// close the WebSocket connection.
				websocket.close(1000);
				break;
			case "error":
				showMessage(event.message);
				break;
		  default:
				throw new Error(`Unsupported event type: ${event.type}.`);
    }
	});
}
