const boardEl = document.getElementById('chessboard');
const turnIndicator = document.getElementById('turn-indicator');
const devModeSelect = document.getElementById('dev-mode');
const instructionPanel = document.getElementById('instruction-panel');
const winnerIndicator = document.getElementById('winner-indicator');

// Action Buttons
const btnMove = document.getElementById('btn-move');
const btnSplit = document.getElementById('btn-split');
const btnSplitMove = document.getElementById('btn-split-move');
const btnReset = document.getElementById('btn-reset');

let currentBoard = [];
let turn = 'W'; // local UI copy of whose turn it is, refreshed from ChessLogic after every action
let actionState = 'move'; // move, split, split_move
let selectionState = {};

// Helper to construct backend-friendly coordinates from grid click
// ChessLogic expects [row, col] (1-indexed based on the original structure)
function getPythonCoords(r, c) {
    if (devModeSelect.value === 'false' && turn === 'W') {
        // White View orientation
        return [8 - r, 8 - c];
    } else {
        // Black View & True View orientation
        return [r + 1, c + 1];
    }
}

// Map piece name to image file name
function getImagePath(pieceName) {
    if (pieceName === '--0--') return null;

    // Example piece name: P_W_1 or P_W_1_S
    const parts = pieceName.split('_');
    const type = parts[0];
    const team = parts[1];
    const isSplit = pieceName.endsWith('_S');

    const fileName = `${type}_${team}${isSplit ? '_S' : ''}.png`;
    return `../static/img/${fileName}`;
}

// Pulls current game state directly from ChessLogic instead of fetching from a server
function getState(devMode) {
    const currentTurn = ChessLogic.getTurn();
    let board;

    if (devMode === 'true') {
        board = ChessLogic.showTrue();
    } else if (currentTurn === 'W') {
        board = ChessLogic.showW();
    } else {
        board = ChessLogic.showB();
    }

    return {
        turn: currentTurn,
        winner: ChessLogic.getWinner(),
        board: board
    };
}

function refreshState() {
    const devMode = devModeSelect.value;
    const data = getState(devMode);

    // Store the previous turn to check if it toggled
    const previousTurn = turn;

    currentBoard = data.board;
    turn = data.turn;

    // If the turn changed, force the UI back to standard move mode
    if (previousTurn !== turn) {
        resetActionState('move');
    }

    turnIndicator.innerText = `Turn: ${turn === 'W' ? 'White' : 'Black'}`;
    if (data.winner) {
        winnerIndicator.innerText = `${data.winner === 'W' ? 'White' : 'Black'} WINS!`;
        winnerIndicator.classList.remove('hidden');
    } else {
        winnerIndicator.classList.add('hidden');
    }
    renderBoard();
}

function renderBoard() {
    boardEl.innerHTML = '';
    for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 8; c++) {
            const square = document.createElement('div');
            square.className = `square ${(r + c) % 2 === 0 ? 'light' : 'dark'}`;
            square.dataset.r = r;
            square.dataset.c = c;

            const pieceName = currentBoard[r][c];
            if (pieceName !== '--0--') {
                square.dataset.piece = pieceName;
                const img = document.createElement('img');
                img.src = getImagePath(pieceName);
                img.className = 'piece-img';

                // Add fallback for missing images to show text temporarily
                img.onerror = () => {
                    img.style.display = 'none';
                    square.innerText = pieceName;
                };
                square.appendChild(img);
            }

            // Highlighting
            if (selectionState.selectedSquare && selectionState.selectedSquare.r === r && selectionState.selectedSquare.c === c) {
                square.classList.add('selected');
            }
            if (selectionState.splitRealDest && selectionState.splitRealDest.r === r && selectionState.splitRealDest.c === c) {
                square.classList.add('highlight');
            }

            square.addEventListener('click', () => handleSquareClick(r, c, pieceName));
            boardEl.appendChild(square);
        }
    }
}

function handleSquareClick(r, c, pieceName) {
    if (actionState === 'move') {
        if (!selectionState.selectedSquare) {
            if (pieceName !== '--0--') {
                selectionState.selectedSquare = { r, c, name: pieceName };
            }
        } else {
            const destCoords = getPythonCoords(r, c);
            const piece = ChessLogic.get_piece_by_name(selectionState.selectedSquare.name);
            if (piece) {
                ChessLogic.move(piece, destCoords);
            }
            selectionState = {};
            refreshState();
        }
    }
    else if (actionState === 'split') {
        if (pieceName !== '--0--') {
            const piece = ChessLogic.get_piece_by_name(pieceName);
            if (piece) {
                ChessLogic.split(piece);
            }
            selectionState = {};
            refreshState();
        }
    }
    else if (actionState === 'split_move') {
        // Step 1: Select the piece pair
        if (!selectionState.realPiece) {
            if (pieceName !== '--0--') {
                // Grab the base piece name regardless of whether the real or fake piece is clicked on top
                const baseName = pieceName.endsWith('_S') ? pieceName.replace('_S', '') : pieceName;

                selectionState.realPiece = baseName;
                selectionState.fakePiece = baseName + '_S';
                selectionState.selectedSquare = { r, c };
                instructionPanel.innerText = "Select destination for REAL piece.";
            }
        }
        // Step 2: Select real dest
        else if (!selectionState.realDest) {
            selectionState.realDest = getPythonCoords(r, c);
            selectionState.splitRealDest = { r, c }; // visual highlight only
            selectionState.selectedSquare = null;
            instructionPanel.innerText = "Select destination for FAKE piece.";
        }
        // Step 3: Select fake dest & Send
        else {
            const fakeDest = getPythonCoords(r, c);
            const realPiece = ChessLogic.get_piece_by_name(selectionState.realPiece);
            const copyPiece = ChessLogic.get_piece_by_name(selectionState.fakePiece);
            if (realPiece && copyPiece) {
                ChessLogic.splitMove(copyPiece, fakeDest, realPiece, selectionState.realDest);
            }
            resetActionState('move'); // return to normal mode
            refreshState();
        }
    }
    //end here
    renderBoard();
}

function resetActionState(newState) {
    actionState = newState;
    selectionState = {};
    [btnMove, btnSplit, btnSplitMove].forEach(b => b.classList.remove('active'));

    if (newState === 'move') {
        btnMove.classList.add('active');
        instructionPanel.innerText = "Select a piece, then select a destination square.";
    } else if (newState === 'split') {
        btnSplit.classList.add('active');
        instructionPanel.innerText = "Click one of your pieces to split it.";
    } else if (newState === 'split_move') {
        btnSplitMove.classList.add('active');
        instructionPanel.innerText = "Select the REAL piece to move.";
    }
    renderBoard();
}

// Event Listeners
btnMove.addEventListener('click', () => resetActionState('move'));
btnSplit.addEventListener('click', () => resetActionState('split'));
btnSplitMove.addEventListener('click', () => resetActionState('split_move'));
devModeSelect.addEventListener('change', refreshState);

btnReset.addEventListener('click', () => {
    ChessLogic.resetBoard();
    winnerIndicator.classList.add('hidden');
    resetActionState('move');
    refreshState();
});

// Init
ChessLogic.resetBoard(); // mirrors the original Python startup behavior
refreshState();