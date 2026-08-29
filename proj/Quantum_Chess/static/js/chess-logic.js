const ChessLogic = (function() {

// --- ORIGINAL GAME STATE & INITIALIZATION ---
let R_W_1 = {Pos: [1, 1], Team: "W", Name: "R_W_1", Type: "R", Beg: 1, Split: false, Real: true};
let R_W_2 = {Pos: [1, 8], Team: "W", Name: "R_W_2", Type: "R", Beg: 1, Split: false, Real: true};
let N_W_1 = {Pos: [1, 2], Team: "W", Name: "N_W_1", Type: "N", Split: false, Real: true};
let N_W_2 = {Pos: [1, 7], Team: "W", Name: "N_W_2", Type: "N", Split: false, Real: true};
let B_W_1 = {Pos: [1, 3], Team: "W", Name: "B_W_1", Type: "B", Split: false, Real: true};
let B_W_2 = {Pos: [1, 6], Team: "W", Name: "B_W_2", Type: "B", Split: false, Real: true};
let Q_W_1 = {Pos: [1, 5], Team: "W", Name: "Q_W_1", Type: "Q", Beg: 0, Split: false, Real: true};
let K_W_1 = {Pos: [1, 4], Team: "W", Name: "K_W_1", Type: "K", Beg: 1, Split: false, Real: true};

let P_W_1 = {Pos: [2, 1], Team: "W", Name: "P_W_1", Type: "P", Beg: 1, Split: false, Real: true};
let P_W_2 = {Pos: [2, 2], Team: "W", Name: "P_W_2", Type: "P", Beg: 1, Split: false, Real: true};
let P_W_3 = {Pos: [2, 3], Team: "W", Name: "P_W_3", Type: "P", Beg: 1, Split: false, Real: true};
let P_W_4 = {Pos: [2, 4], Team: "W", Name: "P_W_4", Type: "P", Beg: 1, Split: false, Real: true};
let P_W_5 = {Pos: [2, 5], Team: "W", Name: "P_W_5", Type: "P", Beg: 1, Split: false, Real: true};
let P_W_6 = {Pos: [2, 6], Team: "W", Name: "P_W_6", Type: "P", Beg: 1, Split: false, Real: true};
let P_W_7 = {Pos: [2, 7], Team: "W", Name: "P_W_7", Type: "P", Beg: 1, Split: false, Real: true};
let P_W_8 = {Pos: [2, 8], Team: "W", Name: "P_W_8", Type: "P", Beg: 1, Split: false, Real: true};

let R_B_1 = {Pos: [8, 1], Team: "B", Name: "R_B_1", Type: "R", Beg: 1, Split: false, Real: true};
let R_B_2 = {Pos: [8, 8], Team: "B", Name: "R_B_2", Type: "R", Beg: 1, Split: false, Real: true};
let N_B_1 = {Pos: [8, 2], Team: "B", Name: "N_B_1", Type: "N", Split: false, Real: true};
let N_B_2 = {Pos: [8, 7], Team: "B", Name: "N_B_2", Type: "N", Split: false, Real: true};
let B_B_1 = {Pos: [8, 3], Team: "B", Name: "B_B_1", Type: "B", Split: false, Real: true};
let B_B_2 = {Pos: [8, 6], Team: "B", Name: "B_B_2", Type: "B", Split: false, Real: true};
let Q_B_1 = {Pos: [8, 5], Team: "B", Name: "Q_B_1", Type: "Q", Beg: 0, Split: false, Real: true};
let K_B_1 = {Pos: [8, 4], Team: "B", Name: "K_B_1", Type: "K", Beg: 1, Split: false, Real: true};

let P_B_1 = {Pos: [7, 1], Team: "B", Name: "P_B_1", Type: "P", Beg: 1, Split: false, Real: true};
let P_B_2 = {Pos: [7, 2], Team: "B", Name: "P_B_2", Type: "P", Beg: 1, Split: false, Real: true};
let P_B_3 = {Pos: [7, 3], Team: "B", Name: "P_B_3", Type: "P", Beg: 1, Split: false, Real: true};
let P_B_4 = {Pos: [7, 4], Team: "B", Name: "P_B_4", Type: "P", Beg: 1, Split: false, Real: true};
let P_B_5 = {Pos: [7, 5], Team: "B", Name: "P_B_5", Type: "P", Beg: 1, Split: false, Real: true};
let P_B_6 = {Pos: [7, 6], Team: "B", Name: "P_B_6", Type: "P", Beg: 1, Split: false, Real: true};
let P_B_7 = {Pos: [7, 7], Team: "B", Name: "P_B_7", Type: "P", Beg: 1, Split: false, Real: true};
let P_B_8 = {Pos: [7, 8], Team: "B", Name: "P_B_8", Type: "P", Beg: 1, Split: false, Real: true};

let kings = {"W": K_W_1, "B": K_B_1};
let turn = "W";
let winner = null;
let active_piece = null;
let links = {};

let pieces = [R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2,
          P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8,
          P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8,
          R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2];

let board = [
    [R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2],
    [P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0'],
    [P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8],
    [R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2]
];

// --- CORE GAME LOGIC ---
function resetBoard() {
    turn = "W";
    winner = null;
    active_piece = null;
    if (Object.keys(links).length !== 0) {
        for (let key in links) delete links[key];
    }

    for (let i of pieces.slice()) {
        if (i.Split === true) {
            if ("Actual" in i) {
                delete i.Actual;
            }
        }
        if (i.Real === false) {
            pieces.splice(pieces.indexOf(i), 1);
        }
    }
    pieces.length = 0;

    board = Array.from({length: 8}, () => new Array(8).fill('0'));

    let initial_pieces = [R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2,
                          P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8,
                          P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8,
                          R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2];

    for (let p of initial_pieces) {
        p.Split = false;
        p.Real = true;
        if (["R", "K", "P"].includes(p.Type)) p.Beg = 1;
        if (p.Type === "Q") p.Beg = 0;
    }

    [R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2].forEach((p, idx) => p.Pos = [1, idx + 1]);
    [P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8].forEach((p, idx) => p.Pos = [2, idx + 1]);
    [P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8].forEach((p, idx) => p.Pos = [7, idx + 1]);
    [R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2].forEach((p, idx) => p.Pos = [8, idx + 1]);

    pieces.push(...initial_pieces);
    update();
}

function win(t) {
    winner = t;
}

function showW() {
    let temp = Array.from({length: 8}, () => new Array(8).fill('--0--'));
    for (let i of pieces) {
        let y = i.Pos[0], x = i.Pos[1];
        if (i.Split === true && i.Real === true && i.Team === "B") {
            temp[8 - y][8 - x] = i.Name + "_S";
        } else {
            temp[8 - y][8 - x] = i.Name;
        }
    }
    return temp;
}

function showB() {
    let temp = Array.from({length: 8}, () => new Array(8).fill('--0--'));
    for (let i of pieces) {
        let y = i.Pos[0], x = i.Pos[1];
        if (i.Split === true && i.Real === true && i.Team === "W") {
            temp[y - 1][x - 1] = i.Name + "_S";
        } else {
            temp[y - 1][x - 1] = i.Name;
        }
    }
    return temp;
}

function showTrue() {
    let temp = Array.from({length: 8}, () => new Array(8).fill('--0--'));
    let sortedPieces = pieces.slice().sort((a, b) => (a.Real === b.Real ? 0 : a.Real ? 1 : -1));
    for (let i of sortedPieces) {
        let y = i.Pos[0], x = i.Pos[1];
        temp[y - 1][x - 1] = i.Name;
    }
    return temp;
}

function update() {
    board = Array.from({length: 8}, () => new Array(8).fill('0'));
    if (!pieces.includes(K_W_1)) {
        win("B");
    } else if (!pieces.includes(K_B_1)) {
        win("W");
    }

    for (let i of pieces) {
        board[i.Pos[0] - 1][i.Pos[1] - 1] = i;
    }
}

function move(p, coords) {
    active_piece = p;
    if (turn === p.Team) {
        let legal = false;
        if (p.Type === "R" && legalR(p.Pos, coords, p)) legal = true;
        else if (p.Type === "N" && legalN(p.Pos, coords)) legal = true;
        else if (p.Type === "B" && legalB(p.Pos, coords)) legal = true;
        else if (p.Type === "Q" && legalQ(p.Pos, coords, p)) legal = true;
        else if (p.Type === "P" && legalP(p.Pos, coords, p)) legal = true;
        else if (p.Type === "K" && legalK(p.Pos, coords, p)) legal = true;

        if (legal) {
            p.Pos = coords;
            update();
            if ("Beg" in p) p.Beg = 0;
            turn = (turn === "W") ? "B" : "W";
        }
        return legal;
    }
    return false;
}

function legalN(pos, coords) {
    if (pos[0] === coords[0] + 2 && [coords[1] + 1, coords[1] - 1].includes(pos[1])) return take(pos, coords);
    else if (pos[0] === coords[0] - 2 && [coords[1] + 1, coords[1] - 1].includes(pos[1])) return take(pos, coords);
    else if (pos[1] === coords[1] + 2 && [coords[0] + 1, coords[0] - 1].includes(pos[0])) return take(pos, coords);
    else if (pos[1] === coords[1] - 2 && [coords[0] + 1, coords[0] - 1].includes(pos[0])) return take(pos, coords);
    return false;
}

function legalB(pos, coords) {
    let dify = pos[0] - coords[0];
    let difx = pos[1] - coords[1];
    let wayY = dify > 0 ? "N" : dify < 0 ? "S" : "";
    let wayX = difx > 0 ? "W" : difx < 0 ? "E" : "";
    let way = wayY + wayX;
    if (Math.abs(pos[0] - coords[0]) === Math.abs(pos[1] - coords[1]) && pos[0] !== coords[0]) {
        return wayB(pos, coords, way);
    }
    return false;
}

function legalR(pos, coords, p) {
    let dify = pos[0] - coords[0];
    let difx = pos[1] - coords[1];
    let way = dify > 0 ? "N" : dify < 0 ? "S" : difx > 0 ? "W" : difx < 0 ? "E" : "";
    if (pos[0] === coords[0] && pos[1] !== coords[1]) return wayR(pos, coords, way);
    else if (pos[1] === coords[1] && pos[0] !== coords[0]) return wayR(pos, coords, way);
    return false;
}

function legalQ(pos, coords, p) {
    return legalB(pos, coords) || legalR(pos, coords, p);
}

function legalP(pos, coords, p) {
    if (p.Team === "W") {
        if (p.Pos[0] + 1 === coords[0] && [p.Pos[1] - 1, p.Pos[1] + 1].includes(coords[1])) return take(pos, coords);
        if (p.Beg === 1 && [coords[0] - 1, coords[0] - 2].includes(pos[0]) && pos[1] === coords[1]) return wayP(pos, coords, "W");
        else if (pos[0] === coords[0] - 1 && pos[1] === coords[1]) return wayP(pos, coords, "W");
    } else if (p.Team === "B") {
        if (p.Pos[0] - 1 === coords[0] && [p.Pos[1] - 1, p.Pos[1] + 1].includes(coords[1])) return take(pos, coords);
        if (p.Beg === 1 && [coords[0] + 1, coords[0] + 2].includes(pos[0]) && pos[1] === coords[1]) return wayP(pos, coords, "B");
        else if (pos[0] === coords[0] + 1 && pos[1] === coords[1]) return wayP(pos, coords, "B");
    }
    return false;
}

function legalK(pos, coords, p) {
    if (Math.abs(pos[0] - coords[0]) <= 1 && Math.abs(pos[1] - coords[1]) <= 1) {
        return wayK(pos, coords);
    }

    if (p.Beg === 1 && pos[0] === coords[0] && Math.abs(pos[1] - coords[1]) === 2) {
        let team = p.Team;
        let row_idx = pos[0] - 1;

        if (coords[1] === pos[1] + 2) {
            let rook = pieces.find(r => r.Type === "R" && r.Team === team && r.Pos[0] === pos[0] && r.Pos[1] === 8 && r.Beg === 1);
            if (rook) {
                let path_clear = true;
                for (let c = pos[1]; c < rook.Pos[1] - 1; c++) {
                    if (board[row_idx][c] !== '0') {
                        path_clear = false; break;
                    }
                }
                if (path_clear) {
                    rook.Pos = [pos[0], pos[1] + 1];
                    return true;
                }
            }
        } else if (coords[1] === pos[1] - 2) {
            let rook = pieces.find(r => r.Type === "R" && r.Team === team && r.Pos[0] === pos[0] && r.Pos[1] === 1 && r.Beg === 1);
            if (rook) {
                let path_clear = true;
                for (let c = rook.Pos[1]; c < pos[1] - 1; c++) {
                    if (board[row_idx][c] !== '0') {
                        path_clear = false; break;
                    }
                }
                if (path_clear) {
                    rook.Pos = [pos[0], pos[1] - 1];
                    return true;
                }
            }
        }
    }
    return false;
}

function cast(p) {
    if (turn === p.Team) {
        let team = p.Team;
        if (p.Type === "R" && p.Beg === 1 && kings[team].Beg === 1) {
            kings[team].Beg = 0;
            let dif = Math.abs(kings[team].Pos[1] - p.Pos[1]);
            if (dif === 3) {
                if (wayR(p.Pos, [p.Pos[0], p.Pos[1] + (dif - 1)], "E")) {
                    p.Pos = [p.Pos[0], p.Pos[1] + (dif - 1)];
                    kings[team].Pos = [kings[team].Pos[0], kings[team].Pos[1] - (dif - 1)];
                    update();
                    turn = (turn === "W") ? "B" : "W";
                }
            } else if (dif === 4) {
                if (wayR(p.Pos, [p.Pos[0], p.Pos[1] - (dif - 1)], "W")) {
                    p.Pos = [p.Pos[0], p.Pos[1] - (dif - 1)];
                    kings[team].Pos = [kings[team].Pos[0], kings[team].Pos[1] + (dif - 2)];
                    update();
                    turn = (turn === "W") ? "B" : "W";
                }
            }
        }
    }
}

function wayR(pos, coords, way) {
    let dif = ["N", "S"].includes(way) ? Math.abs(pos[0] - coords[0]) : Math.abs(pos[1] - coords[1]);
    for (let i = 0; i < dif; i++) {
        if (way === "N" && board[pos[0] - (i + 1) - 1][pos[1] - 1] !== '0') return i === dif - 1 ? take(pos, coords) : false;
        else if (way === "S" && board[pos[0] + (i + 1) - 1][pos[1] - 1] !== '0') return i === dif - 1 ? take(pos, coords) : false;
        else if (way === "E" && board[pos[0] - 1][pos[1] + (i + 1) - 1] !== '0') return i === dif - 1 ? take(pos, coords) : false;
        else if (way === "W" && board[pos[0] - 1][pos[1] - (i + 1) - 1] !== '0') return i === dif - 1 ? take(pos, coords) : false;
    }
    return true;
}

function wayB(pos, coords, way) {
    let dif = Math.abs(pos[0] - coords[0]);
    for (let i = 0; i < dif; i++) {
        if (way === "NW" && board[pos[0] - (i + 1) - 1][pos[1] - (i + 1) - 1] !== '0') return i === dif - 1 ? take(pos, coords) : false;
        else if (way === "NE" && board[pos[0] - (i + 1) - 1][pos[1] + (i + 1) - 1] !== '0') return i === dif - 1 ? take(pos, coords) : false;
        else if (way === "SW" && board[pos[0] + (i + 1) - 1][pos[1] - (i + 1) - 1] !== '0') return i === dif - 1 ? take(pos, coords) : false;
        else if (way === "SE" && board[pos[0] + (i + 1) - 1][pos[1] + (i + 1) - 1] !== '0') return i === dif - 1 ? take(pos, coords) : false;
    }
    return true;
}

function wayP(pos, coords, team) {
    let dif = Math.abs(pos[0] - coords[0]);
    for (let i = 0; i < dif; i++) {
        if (team === "W" && board[pos[0] + (i + 1) - 1][pos[1] - 1] !== '0') return false;
        else if (team === "B" && board[pos[0] - (i + 1) - 1][pos[1] - 1] !== '0') return false;
    }
    return true;
}

function wayK(pos, coords) {
    if (board[coords[0] - 1][coords[1] - 1] !== '0') return take(pos, coords);
    return true;
}

function take(pos, coords) {
    let p = active_piece;
    if (p.Real === false) {
        return board[coords[0] - 1][coords[1] - 1] === '0' ? true : false;
    }

    for (let i of pieces.slice()) {
        if (i.Pos[0] === coords[0] && i.Pos[1] === coords[1]) {
            if (i.Team !== p.Team) {
                if (i.Split === true) {
                    if (i.Real === false) {
                        pieces.splice(pieces.indexOf(i), 1);
                        delete links[i.Name.slice(0, -2)];
                        i.Actual.Split = false;
                        return true;
                    } else if (i.Real === true) {
                        let linkedPiece = links[i.Name];
                        if (linkedPiece) pieces.splice(pieces.indexOf(linkedPiece), 1);
                        delete links[i.Name];
                        i.Split = false;
                        pieces.splice(pieces.indexOf(i), 1);
                        return true;
                    }
                } else {
                    pieces.splice(pieces.indexOf(i), 1);
                    return true;
                }
            } else {
                return false;
            }
        }
    }
    if (p.Type === "N") return true;
    return false;
}

function split(p) {
    if (turn === p.Team && p.Split === false) {
        let s = Object.assign({}, p); // Shallow copy to mirror Python dict.copy()
        s.Pos = [...p.Pos]; // Ensure separate position array
        s.Split = true;
        p.Split = true;
        s.Real = false;
        s.Name = `${p.Name}_S`;
        links[`${p.Name}`] = s;
        s.Actual = p;
        pieces.push(s);
        update();
        turn = (turn === "W") ? "B" : "W";
        return true;
    }
    return false;
}

function splitMove(copy, copycoords, real, realcoords) {
    let current_turn = turn;
    if (move(copy, copycoords)) {
        turn = current_turn;
        move(real, realcoords);
    }
    return true;
}

function get_piece_by_name(name) {
    for (let p of pieces) {
        if (p.Name === name) {
            return p;
        }
    }
    return null;
}

// --- PUBLIC INTERFACE ---
// Only these are accessible from outside as ChessLogic.xxx — everything above
// stays private inside this closure, so nothing here can ever collide with
// variable names in script.js or any other file.
return {
    resetBoard,
    showW,
    showB,
    showTrue,
    move,
    split,
    splitMove,
    get_piece_by_name,
    getTurn: () => turn,
    getWinner: () => winner
};

})();



// Translated from python.  Here is the original python code

// import numpy as np

// R_W_1 = {"Pos" : [1, 1], "Team" : "W", "Name" : "R_W_1", "Type" : "R", "Beg" : 1, "Split" : False, "Real" : True}
// R_W_2 = {"Pos" : [1, 8], "Team" : "W", "Name" : "R_W_2", "Type" : "R", "Beg" : 1, "Split" : False, "Real" : True}
// N_W_1 = {"Pos" : [1, 2], "Team" : "W", "Name" : "N_W_1", "Type" : "N", "Split" : False, "Real" : True}
// N_W_2 = {"Pos" : [1, 7], "Team" : "W", "Name" : "N_W_2", "Type" : "N", "Split" : False, "Real" : True}
// B_W_1 = {"Pos" : [1, 3], "Team" : "W", "Name" : "B_W_1", "Type" : "B", "Split" : False, "Real" : True}
// B_W_2 = {"Pos" : [1, 6], "Team" : "W", "Name" : "B_W_2", "Type" : "B", "Split" : False, "Real" : True}
// Q_W_1 = {"Pos" : [1, 5], "Team" : "W", "Name" : "Q_W_1", "Type" : "Q", "Beg" : 0, "Split" : False, "Real" : True}
// K_W_1 = {"Pos" : [1, 4], "Team" : "W", "Name" : "K_W_1", "Type" : "K", "Beg" : 1, "Split" : False, "Real" : True}

// P_W_1= {"Pos" : [2, 1], "Team" : "W", "Name" : "P_W_1", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_W_2 = {"Pos" : [2, 2], "Team" : "W", "Name" : "P_W_2", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_W_3 = {"Pos" : [2, 3], "Team" : "W", "Name" : "P_W_3", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_W_4 = {"Pos" : [2, 4], "Team" : "W", "Name" : "P_W_4", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_W_5 = {"Pos" : [2, 5], "Team" : "W", "Name" : "P_W_5", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_W_6 = {"Pos" : [2, 6], "Team" : "W", "Name" : "P_W_6", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_W_7 = {"Pos" : [2, 7], "Team" : "W", "Name" : "P_W_7", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_W_8 = {"Pos" : [2, 8], "Team" : "W", "Name" : "P_W_8", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}

// R_B_1 = {"Pos" : [8, 1], "Team" : "B", "Name" : "R_B_1", "Type" : "R", "Beg" : 1, "Split" : False, "Real" : True}
// R_B_2 = {"Pos" : [8, 8], "Team" : "B", "Name" : "R_B_2", "Type" : "R", "Beg" : 1, "Split" : False, "Real" : True}
// N_B_1 = {"Pos" : [8, 2], "Team" : "B", "Name" : "N_B_1", "Type" : "N", "Split" : False, "Real" : True}
// N_B_2 = {"Pos" : [8, 7], "Team" : "B", "Name" : "N_B_2", "Type" : "N", "Split" : False, "Real" : True}
// B_B_1 = {"Pos" : [8, 3], "Team" : "B", "Name" : "B_B_1", "Type" : "B", "Split" : False, "Real" : True}
// B_B_2 = {"Pos" : [8, 6], "Team" : "B", "Name" : "B_B_2", "Type" : "B", "Split" : False, "Real" : True}
// Q_B_1 = {"Pos" : [8, 5], "Team" : "B", "Name" : "Q_B_1", "Type" : "Q", "Beg" : 0, "Split" : False, "Real" : True}
// K_B_1 = {"Pos" : [8, 4], "Team" : "B", "Name" : "K_B_1", "Type" : "K", "Beg" : 1, "Split" : False, "Real" : True}

// P_B_1 = {"Pos" : [7, 1], "Team" : "B", "Name" : "P_B_1", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_B_2 = {"Pos" : [7, 2], "Team" : "B", "Name" : "P_B_2", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_B_3 = {"Pos" : [7, 3], "Team" : "B", "Name" : "P_B_3", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_B_4 = {"Pos" : [7, 4], "Team" : "B", "Name" : "P_B_4", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_B_5 = {"Pos" : [7, 5], "Team" : "B", "Name" : "P_B_5", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_B_6 = {"Pos" : [7, 6], "Team" : "B", "Name" : "P_B_6", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_B_7 = {"Pos" : [7, 7], "Team" : "B", "Name" : "P_B_7", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
// P_B_8 = {"Pos" : [7, 8], "Team" : "B", "Name" : "P_B_8", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}

// kings = {"W" : K_W_1, "B" : K_B_1}
// turn = "W"
// winner = None
// active_piece = None
// links = {}

// pieces = [R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2,
//           P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8,
//           P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8,
//           R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2]

// board = np.array([
//     [R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2],
//     [P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8],
//     ['0','0','0','0','0','0','0','0'],
//     ['0','0','0','0','0','0','0','0'],
//     ['0','0','0','0','0','0','0','0'],
//     ['0','0','0','0','0','0','0','0'],
//     [P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8],
//     [R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2]])

// # --- CORE GAME LOGIC ---
// def resetBoard():
//     global turn, links, pieces, board, winner, active_piece
//     turn = "W"
//     winner = None
//     active_piece = None
//     if len(links) != 0:
//         links.clear()

//     for i in pieces[:]:
//         if i.get("Split") == True:
//             if "Actual" in i:
//                 del i["Actual"]
//         if i.get("Real") == False:
//             pieces.remove(i)
//     pieces.clear()

//     board = np.full((8,8), '0', dtype=object)

//     for p in [R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2,
//               P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8,
//               P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8,
//               R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2]:
//         p["Split"] = False
//         p["Real"] = True
//         if p["Type"] in ["R", "K", "P"]: p["Beg"] = 1
//         if p["Type"] == "Q": p["Beg"] = 0

//     for idx, p in enumerate([R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2]): p["Pos"] = [1, idx+1]
//     for idx, p in enumerate([P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8]): p["Pos"] = [2, idx+1]
//     for idx, p in enumerate([P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8]): p["Pos"] = [7, idx+1]
//     for idx, p in enumerate([R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2]): p["Pos"] = [8, idx+1]

//     pieces.extend([R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2,
//              P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8,
//              P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8,
//              R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2])
//     update()

// def win(t):
//     global winner
//     winner = t

// def showW():
//     temp = np.full((8,8), '--0--', dtype=object)
//     for i in pieces:
//         y, x = i["Pos"][0], i["Pos"][1]
//         if i["Split"] == True and i["Real"] == True and i["Team"] == "B":
//             temp[8 - y][8 - x] = i["Name"] + "_S"
//         else:
//             temp[8 - y][8 - x] = i["Name"]
//     return temp.tolist()

// def showB():
//     temp = np.full((8,8), '--0--', dtype=object)
//     for i in pieces:
//         y, x = i["Pos"][0], i["Pos"][1]
//         if i["Split"] == True and i["Real"] == True and i["Team"] == "W":
//             temp[y - 1][x - 1] = i["Name"] + "_S"
//         else:
//             temp[y - 1][x - 1] = i["Name"]
//     return temp.tolist()

// def showTrue():
//     temp = np.full((8,8), '--0--', dtype=object)
//     for i in sorted(pieces, key=lambda p: p.get("Real", False)):
//         y, x = i["Pos"][0], i["Pos"][1]
//         temp[y - 1][x - 1] = i["Name"]
//     return temp.tolist()

// def update():
//     global board
//     board = np.full((8,8), '0', dtype=object)
//     if K_W_1 not in pieces:
//         win("B")
//     elif K_B_1 not in pieces:
//         win("W")

//     for i in pieces:
//         board[i["Pos"][0]-1][i["Pos"][1]-1] = i

// def move(p, coords):
//     global turn, active_piece
//     active_piece = p
//     if turn == p["Team"]:
//         legal = False
//         if p["Type"] == "R" and legalR(p["Pos"], coords, p): legal = True
//         elif p["Type"] == "N" and legalN(p["Pos"], coords): legal = True
//         elif p["Type"] == "B" and legalB(p["Pos"], coords): legal = True
//         elif p["Type"] == "Q" and legalQ(p["Pos"], coords, p): legal = True
//         elif p["Type"] == "P" and legalP(p["Pos"], coords, p): legal = True
//         elif p["Type"] == "K" and legalK(p["Pos"], coords, p): legal = True

//         if legal:
//             p["Pos"] = coords
//             update()
//             if "Beg" in p: p["Beg"] = 0
//             turn = "B" if turn == "W" else "W"
//         return legal
//     return False

// def legalN(pos, coords):
//     if pos[0] == coords[0] + 2 and pos[1] in [coords[1] + 1, coords[1] - 1]: return take(pos, coords)
//     elif pos[0] == coords[0] - 2 and pos[1] in [coords[1] + 1, coords[1] - 1]: return take(pos, coords)
//     elif pos[1] == coords[1] + 2 and pos[0] in [coords[0] + 1, coords[0] - 1]: return take(pos, coords)
//     elif pos[1] == coords[1] - 2 and pos[0] in [coords[0] + 1, coords[0] - 1]: return take(pos, coords)
//     return False

// def legalB(pos, coords):
//     dify = pos[0] - coords[0]
//     difx = pos[1] - coords[1]
//     wayY = "N" if dify > 0 else "S" if dify < 0 else ""
//     wayX = "W" if difx > 0 else "E" if difx < 0 else ""
//     way = wayY + wayX
//     if abs(pos[0] - coords[0]) == abs(pos[1] - coords[1]) and pos[0] != coords[0]:
//         return wayB(pos, coords, way)
//     return False

// def legalR(pos, coords, p):
//     dify = pos[0] - coords[0]
//     difx = pos[1] - coords[1]
//     way = "N" if dify > 0 else "S" if dify < 0 else "W" if difx > 0 else "E" if difx < 0 else ""
//     if pos[0] == coords[0] and pos[1] != coords[1]: return wayR(pos, coords, way)
//     elif pos[1] == coords[1] and pos[0] != coords[0]: return wayR(pos, coords, way)
//     return False

// def legalQ(pos, coords, p): return legalB(pos, coords) or legalR(pos, coords, p)

// def legalP(pos, coords, p):
//     if p["Team"] == "W":
//         if p["Pos"][0] + 1 == coords[0] and coords[1] in [p["Pos"][1] - 1, p["Pos"][1] + 1]: return take(pos, coords)
//         if p["Beg"] == 1 and pos[0] in [coords[0] - 1, coords[0] - 2] and pos[1] == coords[1]: return wayP(pos, coords, "W")
//         elif pos[0] == coords[0] - 1 and pos[1] == coords[1]: return wayP(pos, coords, "W")
//     elif p["Team"] == "B":
//         if p["Pos"][0] - 1 == coords[0] and coords[1] in [p["Pos"][1] - 1, p["Pos"][1] + 1]: return take(pos, coords)
//         if p["Beg"] == 1 and pos[0] in [coords[0] + 1, coords[0] + 2] and pos[1] == coords[1]: return wayP(pos, coords, "B")
//         elif pos[0] == coords[0] + 1 and pos[1] == coords[1]: return wayP(pos, coords, "B")
//     return False

// def legalK(pos, coords, p):
//     if abs(pos[0] - coords[0]) <= 1 and abs(pos[1] - coords[1]) <= 1:
//         return wayK(pos, coords)

//     if p.get("Beg") == 1 and pos[0] == coords[0] and abs(pos[1] - coords[1]) == 2:
//         team = p["Team"]
//         row_idx = pos[0] - 1

//         if coords[1] == pos[1] + 2:
//             rook = next((r for r in pieces if r["Type"] == "R" and r["Team"] == team and r["Pos"] == [pos[0], 8] and r.get("Beg") == 1), None)
//             if rook:
//                 path_clear = all(board[row_idx][c] == '0' for c in range(pos[1], rook["Pos"][1] - 1))
//                 if path_clear:
//                     rook["Pos"] = [pos[0], pos[1] + 1]
//                     return True

//         elif coords[1] == pos[1] - 2:
//             rook = next((r for r in pieces if r["Type"] == "R" and r["Team"] == team and r["Pos"] == [pos[0], 1] and r.get("Beg") == 1), None)
//             if rook:
//                 path_clear = all(board[row_idx][c] == '0' for c in range(rook["Pos"][1], pos[1] - 1))
//                 if path_clear:
//                     rook["Pos"] = [pos[0], pos[1] - 1]
//                     return True

//     return False

// def cast(p):
//     global turn
//     if turn == p["Team"]:
//         team = p["Team"]
//         if p["Type"] == "R" and p["Beg"] == 1 and kings[team]["Beg"] == 1:
//             kings[team]["Beg"] = 0
//             dif = abs(kings[team]["Pos"][1] - p["Pos"][1])
//             if dif == 3:
//                 if wayR(p["Pos"], [p["Pos"][0], p["Pos"][1] + (dif-1)], "E"):
//                     p["Pos"] = [p["Pos"][0], p["Pos"][1] + (dif-1)]
//                     kings[team]["Pos"] = [kings[team]["Pos"][0], kings[team]["Pos"][1] - (dif-1)]
//                     update()
//                     turn = "B" if turn == "W" else "W"
//             elif dif == 4:
//                 if wayR(p["Pos"], [p["Pos"][0], p["Pos"][1] - (dif-1)], "W"):
//                     p["Pos"] = [p["Pos"][0], p["Pos"][1] - (dif-1)]
//                     kings[team]["Pos"] = [kings[team]["Pos"][0], kings[team]["Pos"][1] + (dif-2)]
//                     update()
//                     turn = "B" if turn == "W" else "W"

// def wayR(pos, coords, way):
//     dif = abs(pos[0] - coords[0]) if way in ["N", "S"] else abs(pos[1] - coords[1])
//     for i in range(dif):
//         if way == "N" and board[pos[0]-(i+1)-1][pos[1]-1] != '0': return take(pos, coords) if i == dif - 1 else False
//         elif way == "S" and board[pos[0]+(i+1)-1][pos[1]-1] != '0': return take(pos, coords) if i == dif - 1 else False
//         elif way == "E" and board[pos[0]-1][pos[1]+(i+1)-1] != '0': return take(pos, coords) if i == dif - 1 else False
//         elif way == "W" and board[pos[0]-1][pos[1]-(i+1)-1] != '0': return take(pos, coords) if i == dif - 1 else False
//     return True

// def wayB(pos, coords, way):
//     dif = abs(pos[0] - coords[0])
//     for i in range(dif):
//         if way == "NW" and board[pos[0]-(i+1)-1][pos[1]-(i+1)-1] != '0': return take(pos, coords) if i == dif - 1 else False
//         elif way == "NE" and board[pos[0]-(i+1)-1][pos[1]+(i+1)-1] != '0': return take(pos, coords) if i == dif - 1 else False
//         elif way == "SW" and board[pos[0]+(i+1)-1][pos[1]-(i+1)-1] != '0': return take(pos, coords) if i == dif - 1 else False
//         elif way == "SE" and board[pos[0]+(i+1)-1][pos[1]+(i+1)-1] != '0': return take(pos, coords) if i == dif - 1 else False
//     return True

// def wayP(pos, coords, team):
//     dif = abs(pos[0] - coords[0])
//     for i in range(dif):
//         if team == "W" and board[pos[0]+(i+1)-1][pos[1]-1] != '0': return False
//         elif team == "B" and board[pos[0]-(i+1)-1][pos[1]-1] != '0': return False
//     return True

// def wayK(pos, coords):
//     if board[coords[0]-1][coords[1]-1] != '0': return take(pos, coords)
//     return True

// def take(pos, coords):
//     global active_piece
//     p = active_piece
//     if p["Real"] == False:
//         return True if board[coords[0]-1][coords[1]-1] == '0' else False

//     for i in pieces[:]:
//         if i["Pos"] == coords:
//             if i["Team"] != p["Team"]:
//                 if i["Split"] == True:
//                     if i["Real"] == False:
//                         pieces.remove(i)
//                         del links[i["Name"][:-2]]
//                         i["Actual"]["Split"] = False
//                         del i
//                         return True
//                     elif i["Real"] == True:
//                         pieces.remove(links[i["Name"]])
//                         del links[i["Name"]]
//                         i["Split"] = False
//                         pieces.remove(i)
//                         return True
//                 else:
//                     pieces.remove(i)
//                     return True
//             else:
//                 return False
//     if p["Type"] == "N": return True
//     return False

// def split(p):
//     global turn
//     if turn == p["Team"] and p["Split"] == False:
//         s = p.copy()
//         s["Split"] = True
//         p["Split"] = True
//         s["Real"] = False
//         s["Name"] = f'{p["Name"]}_S'
//         links[f'{p["Name"]}'] = s
//         s["Actual"] = p
//         pieces.append(s)
//         update()
//         turn = "B" if turn == "W" else "W"
//         return True
//     return False

// def splitMove(copy, copycoords, real, realcoords):
//     global turn
//     current_turn = turn
//     if move(copy, copycoords):
//         turn = current_turn
//         move(real, realcoords)
//     return True

// def get_piece_by_name(name):
//     for p in pieces:
//         if p["Name"] == name:
//             return p
//     return None