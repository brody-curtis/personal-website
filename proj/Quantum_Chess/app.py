from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

# --- ORIGINAL GAME STATE & INITIALIZATION ---
R_W_1 = {"Pos" : [1, 1], "Team" : "W", "Name" : "R_W_1", "Type" : "R", "Beg" : 1, "Split" : False, "Real" : True}
R_W_2 = {"Pos" : [1, 8], "Team" : "W", "Name" : "R_W_2", "Type" : "R", "Beg" : 1, "Split" : False, "Real" : True}
N_W_1 = {"Pos" : [1, 2], "Team" : "W", "Name" : "N_W_1", "Type" : "N", "Split" : False, "Real" : True}
N_W_2 = {"Pos" : [1, 7], "Team" : "W", "Name" : "N_W_2", "Type" : "N", "Split" : False, "Real" : True}
B_W_1 = {"Pos" : [1, 3], "Team" : "W", "Name" : "B_W_1", "Type" : "B", "Split" : False, "Real" : True}
B_W_2 = {"Pos" : [1, 6], "Team" : "W", "Name" : "B_W_2", "Type" : "B", "Split" : False, "Real" : True}
Q_W_1 = {"Pos" : [1, 5], "Team" : "W", "Name" : "Q_W_1", "Type" : "Q", "Beg" : 0, "Split" : False, "Real" : True}
K_W_1 = {"Pos" : [1, 4], "Team" : "W", "Name" : "K_W_1", "Type" : "K", "Beg" : 1, "Split" : False, "Real" : True}

P_W_1= {"Pos" : [2, 1], "Team" : "W", "Name" : "P_W_1", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_W_2 = {"Pos" : [2, 2], "Team" : "W", "Name" : "P_W_2", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_W_3 = {"Pos" : [2, 3], "Team" : "W", "Name" : "P_W_3", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_W_4 = {"Pos" : [2, 4], "Team" : "W", "Name" : "P_W_4", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_W_5 = {"Pos" : [2, 5], "Team" : "W", "Name" : "P_W_5", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_W_6 = {"Pos" : [2, 6], "Team" : "W", "Name" : "P_W_6", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_W_7 = {"Pos" : [2, 7], "Team" : "W", "Name" : "P_W_7", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_W_8 = {"Pos" : [2, 8], "Team" : "W", "Name" : "P_W_8", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}

R_B_1 = {"Pos" : [8, 1], "Team" : "B", "Name" : "R_B_1", "Type" : "R", "Beg" : 1, "Split" : False, "Real" : True}
R_B_2 = {"Pos" : [8, 8], "Team" : "B", "Name" : "R_B_2", "Type" : "R", "Beg" : 1, "Split" : False, "Real" : True}
N_B_1 = {"Pos" : [8, 2], "Team" : "B", "Name" : "N_B_1", "Type" : "N", "Split" : False, "Real" : True}
N_B_2 = {"Pos" : [8, 7], "Team" : "B", "Name" : "N_B_2", "Type" : "N", "Split" : False, "Real" : True}
B_B_1 = {"Pos" : [8, 3], "Team" : "B", "Name" : "B_B_1", "Type" : "B", "Split" : False, "Real" : True}
B_B_2 = {"Pos" : [8, 6], "Team" : "B", "Name" : "B_B_2", "Type" : "B", "Split" : False, "Real" : True}
Q_B_1 = {"Pos" : [8, 5], "Team" : "B", "Name" : "Q_B_1", "Type" : "Q", "Beg" : 0, "Split" : False, "Real" : True}
K_B_1 = {"Pos" : [8, 4], "Team" : "B", "Name" : "K_B_1", "Type" : "K", "Beg" : 1, "Split" : False, "Real" : True}

P_B_1 = {"Pos" : [7, 1], "Team" : "B", "Name" : "P_B_1", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_B_2 = {"Pos" : [7, 2], "Team" : "B", "Name" : "P_B_2", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_B_3 = {"Pos" : [7, 3], "Team" : "B", "Name" : "P_B_3", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_B_4 = {"Pos" : [7, 4], "Team" : "B", "Name" : "P_B_4", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_B_5 = {"Pos" : [7, 5], "Team" : "B", "Name" : "P_B_5", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_B_6 = {"Pos" : [7, 6], "Team" : "B", "Name" : "P_B_6", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_B_7 = {"Pos" : [7, 7], "Team" : "B", "Name" : "P_B_7", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}
P_B_8 = {"Pos" : [7, 8], "Team" : "B", "Name" : "P_B_8", "Type" : "P", "Beg" : 1, "Split" : False, "Real" : True}

kings = {"W" : K_W_1, "B" : K_B_1}
turn = "W"
winner = None
active_piece = None
links = {}

pieces = [R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2,
          P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8,
          P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8,
          R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2]

board = np.array([
    [R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2],
    [P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8],
    ['0','0','0','0','0','0','0','0'],
    ['0','0','0','0','0','0','0','0'],
    ['0','0','0','0','0','0','0','0'],
    ['0','0','0','0','0','0','0','0'],
    [P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8],
    [R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2]])

# --- MODIFIED LOGIC FOR BACKEND ---
def resetBoard():
    global turn, links, pieces, board, winner, active_piece
    turn = "W"
    winner = None
    active_piece = None
    if len(links) != 0:
        links.clear()
    
    for i in pieces[:]:
        if i.get("Split") == True:
            if "Actual" in i:
                del i["Actual"]
        if i.get("Real") == False:
            pieces.remove(i)
    pieces.clear()

    board = np.full((8,8), '0', dtype=object)
    
    # Reset all base attributes
    for p in [R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2,
              P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8,
              P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8,
              R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2]:
        p["Split"] = False
        p["Real"] = True
        if p["Type"] in ["R", "K", "P"]: p["Beg"] = 1
        if p["Type"] == "Q": p["Beg"] = 0
    
    # Restore Initial Positions
    for idx, p in enumerate([R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2]): p["Pos"] = [1, idx+1]
    for idx, p in enumerate([P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8]): p["Pos"] = [2, idx+1]
    for idx, p in enumerate([P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8]): p["Pos"] = [7, idx+1]
    for idx, p in enumerate([R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2]): p["Pos"] = [8, idx+1]

    pieces.extend([R_W_1, N_W_1, B_W_1, K_W_1, Q_W_1, B_W_2, N_W_2, R_W_2,
             P_W_1, P_W_2, P_W_3, P_W_4, P_W_5, P_W_6, P_W_7, P_W_8,
             P_B_1, P_B_2, P_B_3, P_B_4, P_B_5, P_B_6, P_B_7, P_B_8,
             R_B_1, N_B_1, B_B_1, K_B_1, Q_B_1, B_B_2, N_B_2, R_B_2])
    update()

def win(t):
    global winner
    winner = t

def showW():
    # White on bottom (row 1 at bottom), King to the right of Queen
    temp = np.full((8,8), '--0--', dtype=object)
    for i in pieces:
        y, x = i["Pos"][0], i["Pos"][1]
        if i["Split"] == True and i["Real"] == True and i["Team"] == "B":
            temp[8 - y][8 - x] = i["Name"] + "_S"
        else:
            temp[8 - y][8 - x] = i["Name"]
    return temp.tolist()

def showB():
    # Black on bottom (row 8 at bottom), King to the left of Queen
    temp = np.full((8,8), '--0--', dtype=object)
    for i in pieces:
        y, x = i["Pos"][0], i["Pos"][1]
        if i["Split"] == True and i["Real"] == True and i["Team"] == "W":
            temp[y - 1][x - 1] = i["Name"] + "_S"
        else:
            temp[y - 1][x - 1] = i["Name"]
    return temp.tolist()

def showTrue():
    # Same orientation as Black view
    temp = np.full((8,8), '--0--', dtype=object)
    for i in sorted(pieces, key=lambda p: p.get("Real", False)):
        y, x = i["Pos"][0], i["Pos"][1]
        temp[y - 1][x - 1] = i["Name"]
    return temp.tolist()

def update():
    global board
    board = np.full((8,8), '0', dtype=object)
    if K_W_1 not in pieces:
        win("B")
    elif K_B_1 not in pieces:
        win("W")

    for i in pieces:
        board[i["Pos"][0]-1][i["Pos"][1]-1] = i

# --- UNCHANGED ORIGINAL GAME LOGIC ---
def move(p, coords):
    global turn, active_piece
    active_piece = p
    if turn == p["Team"]:
        legal = False
        if p["Type"] == "R" and legalR(p["Pos"], coords, p): legal = True
        elif p["Type"] == "N" and legalN(p["Pos"], coords): legal = True
        elif p["Type"] == "B" and legalB(p["Pos"], coords): legal = True
        elif p["Type"] == "Q" and legalQ(p["Pos"], coords, p): legal = True
        elif p["Type"] == "P" and legalP(p["Pos"], coords, p): legal = True
        elif p["Type"] == "K" and legalK(p["Pos"], coords, p): legal = True
        
        if legal:
            p["Pos"] = coords
            update()
            if "Beg" in p: p["Beg"] = 0
            turn = "B" if turn == "W" else "W"
        return legal
    return False

def legalN(pos, coords):
    if pos[0] == coords[0] + 2 and pos[1] in [coords[1] + 1, coords[1] - 1]: return take(pos, coords)
    elif pos[0] == coords[0] - 2 and pos[1] in [coords[1] + 1, coords[1] - 1]: return take(pos, coords)
    elif pos[1] == coords[1] + 2 and pos[0] in [coords[0] + 1, coords[0] - 1]: return take(pos, coords)
    elif pos[1] == coords[1] - 2 and pos[0] in [coords[0] + 1, coords[0] - 1]: return take(pos, coords)
    return False

def legalB(pos, coords):
    dify = pos[0] - coords[0]
    difx = pos[1] - coords[1]
    wayY = "N" if dify > 0 else "S" if dify < 0 else ""
    wayX = "W" if difx > 0 else "E" if difx < 0 else ""
    way = wayY + wayX
    if abs(pos[0] - coords[0]) == abs(pos[1] - coords[1]) and pos[0] != coords[0]:
        return wayB(pos, coords, way)
    return False

def legalR(pos, coords, p):
    dify = pos[0] - coords[0]
    difx = pos[1] - coords[1]
    way = "N" if dify > 0 else "S" if dify < 0 else "W" if difx > 0 else "E" if difx < 0 else ""
    if pos[0] == coords[0] and pos[1] != coords[1]: return wayR(pos, coords, way)
    elif pos[1] == coords[1] and pos[0] != coords[0]: return wayR(pos, coords, way)
    return False

def legalQ(pos, coords, p): return legalB(pos, coords) or legalR(pos, coords, p)

def legalP(pos, coords, p):
    if p["Team"] == "W":
        if p["Pos"][0] + 1 == coords[0] and coords[1] in [p["Pos"][1] - 1, p["Pos"][1] + 1]: return take(pos, coords)
        if p["Beg"] == 1 and pos[0] in [coords[0] - 1, coords[0] - 2] and pos[1] == coords[1]: return wayP(pos, coords, "W")
        elif pos[0] == coords[0] - 1 and pos[1] == coords[1]: return wayP(pos, coords, "W")
    elif p["Team"] == "B":
        if p["Pos"][0] - 1 == coords[0] and coords[1] in [p["Pos"][1] - 1, p["Pos"][1] + 1]: return take(pos, coords)
        if p["Beg"] == 1 and pos[0] in [coords[0] + 1, coords[0] + 2] and pos[1] == coords[1]: return wayP(pos, coords, "B")
        elif pos[0] == coords[0] + 1 and pos[1] == coords[1]: return wayP(pos, coords, "B")
    return False

def legalK(pos, coords, p):
    # Standard King move
    if abs(pos[0] - coords[0]) <= 1 and abs(pos[1] - coords[1]) <= 1: 
        return wayK(pos, coords)
    
    # Castling: King moves exactly 2 squares horizontally
    if p.get("Beg") == 1 and pos[0] == coords[0] and abs(pos[1] - coords[1]) == 2:
        team = p["Team"]
        row_idx = pos[0] - 1
        
        if coords[1] == pos[1] + 2: # East (Kingside)
            rook = next((r for r in pieces if r["Type"] == "R" and r["Team"] == team and r["Pos"] == [pos[0], 8] and r.get("Beg") == 1), None)
            if rook:
                # Check if path is clear between King and Rook
                path_clear = all(board[row_idx][c] == '0' for c in range(pos[1], rook["Pos"][1] - 1))
                if path_clear:
                    rook["Pos"] = [pos[0], pos[1] + 1] # Move rook to the other side of the King
                    return True
                    
        elif coords[1] == pos[1] - 2: # West (Queenside)
            rook = next((r for r in pieces if r["Type"] == "R" and r["Team"] == team and r["Pos"] == [pos[0], 1] and r.get("Beg") == 1), None)
            if rook:
                # Check if path is clear between Rook and King
                path_clear = all(board[row_idx][c] == '0' for c in range(rook["Pos"][1], pos[1] - 1))
                if path_clear:
                    rook["Pos"] = [pos[0], pos[1] - 1] # Move rook to the other side of the King
                    return True
                
    return False

def cast(p):
    global turn
    if turn == p["Team"]:
        team = p["Team"]
        if p["Type"] == "R" and p["Beg"] == 1 and kings[team]["Beg"] == 1:
            kings[team]["Beg"] = 0
            dif = abs(kings[team]["Pos"][1] - p["Pos"][1])
            if dif == 3:
                if wayR(p["Pos"], [p["Pos"][0], p["Pos"][1] + (dif-1)], "E"):
                    p["Pos"] = [p["Pos"][0], p["Pos"][1] + (dif-1)]
                    kings[team]["Pos"] = [kings[team]["Pos"][0], kings[team]["Pos"][1] - (dif-1)]
                    update()
                    turn = "B" if turn == "W" else "W"
            elif dif == 4:
                if wayR(p["Pos"], [p["Pos"][0], p["Pos"][1] - (dif-1)], "W"):
                    p["Pos"] = [p["Pos"][0], p["Pos"][1] - (dif-1)]
                    kings[team]["Pos"] = [kings[team]["Pos"][0], kings[team]["Pos"][1] + (dif-2)]
                    update()
                    turn = "B" if turn == "W" else "W"

def wayR(pos, coords, way):
    dif = abs(pos[0] - coords[0]) if way in ["N", "S"] else abs(pos[1] - coords[1])
    for i in range(dif):
        if way == "N" and board[pos[0]-(i+1)-1][pos[1]-1] != '0': return take(pos, coords) if i == dif - 1 else False
        elif way == "S" and board[pos[0]+(i+1)-1][pos[1]-1] != '0': return take(pos, coords) if i == dif - 1 else False
        elif way == "E" and board[pos[0]-1][pos[1]+(i+1)-1] != '0': return take(pos, coords) if i == dif - 1 else False
        elif way == "W" and board[pos[0]-1][pos[1]-(i+1)-1] != '0': return take(pos, coords) if i == dif - 1 else False
    return True

def wayB(pos, coords, way):
    dif = abs(pos[0] - coords[0])
    for i in range(dif):
        if way == "NW" and board[pos[0]-(i+1)-1][pos[1]-(i+1)-1] != '0': return take(pos, coords) if i == dif - 1 else False
        elif way == "NE" and board[pos[0]-(i+1)-1][pos[1]+(i+1)-1] != '0': return take(pos, coords) if i == dif - 1 else False
        elif way == "SW" and board[pos[0]+(i+1)-1][pos[1]-(i+1)-1] != '0': return take(pos, coords) if i == dif - 1 else False
        elif way == "SE" and board[pos[0]+(i+1)-1][pos[1]+(i+1)-1] != '0': return take(pos, coords) if i == dif - 1 else False
    return True

def wayP(pos, coords, team):
    dif = abs(pos[0] - coords[0])
    for i in range(dif):
        if team == "W" and board[pos[0]+(i+1)-1][pos[1]-1] != '0': return False
        elif team == "B" and board[pos[0]-(i+1)-1][pos[1]-1] != '0': return False
    return True

def wayK(pos, coords):
    if board[coords[0]-1][coords[1]-1] != '0': return take(pos, coords)
    return True

def take(pos, coords):
    global active_piece
    p = active_piece
    if p["Real"] == False:
        return True if board[coords[0]-1][coords[1]-1] == '0' else False

    for i in pieces[:]:
        if i["Pos"] == coords:
            if i["Team"] != p["Team"]:
                if i["Split"] == True:
                    if i["Real"] == False:
                        pieces.remove(i)
                        del links[i["Name"][:-2]]
                        i["Actual"]["Split"] = False
                        del i
                        return True
                    elif i["Real"] == True:
                        pieces.remove(links[i["Name"]])
                        del links[i["Name"]]
                        i["Split"] = False
                        pieces.remove(i)
                        return True
                else:
                    pieces.remove(i)
                    return True
            else:
                return False
    if p["Type"] == "N": return True
    return False

def split(p):
    global turn
    if turn == p["Team"] and p["Split"] == False:
        s = p.copy()
        s["Split"] = True
        p["Split"] = True
        s["Real"] = False
        s["Name"] = f'{p["Name"]}_S'
        links[f'{p["Name"]}'] = s
        s["Actual"] = p
        pieces.append(s)
        update()
        turn = "B" if turn == "W" else "W"
        return True
    return False

def splitMove(copy, copycoords, real, realcoords):
    global turn
    current_turn = turn
    if move(copy, copycoords):
        turn = current_turn
        move(real, realcoords)
    return True

# --- FLASK API ROUTES ---
def get_piece_by_name(name):
    for p in pieces:
        if p["Name"] == name:
            return p
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/state', methods=['GET'])
def get_state():
    dev_mode = request.args.get('dev', 'false').lower() == 'true'
    
    if dev_mode:
        board_view = showTrue()
    elif turn == "W":
        board_view = showW()
    else:
        board_view = showB()
        
    return jsonify({
        "turn": turn,
        "winner": winner,
        "board": board_view
    })

@app.route('/move', methods=['POST'])
def api_move():
    data = request.json
    piece = get_piece_by_name(data['piece_name'])
    if not piece: return jsonify({"success": False, "msg": "Piece not found"}), 400
    
    success = move(piece, data['coords'])
    return jsonify({"success": success})

@app.route('/split', methods=['POST'])
def api_split():
    data = request.json
    piece = get_piece_by_name(data['piece_name'])
    if not piece: return jsonify({"success": False}), 400
    
    success = split(piece)
    return jsonify({"success": success})

@app.route('/split_move', methods=['POST'])
def api_split_move():
    data = request.json
    real = get_piece_by_name(data['real_name'])
    copy = get_piece_by_name(data['copy_name'])
    
    if not real or not copy: return jsonify({"success": False}), 400
    
    splitMove(copy, data['copy_coords'], real, data['real_coords'])
    return jsonify({"success": True})

@app.route('/reset', methods=['POST'])
def api_reset():
    resetBoard()
    return jsonify({"success": True})

if __name__ == '__main__':
    resetBoard()  # Initialize board on start
    app.run(debug=True, port=5000)
