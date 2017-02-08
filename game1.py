from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

new_game_state = {"current_turn": "A",
                                "setup": True,
                                "selected": "",
                                "c1": [], "d1": [], "e1": [], "f1": [], "g1": [], "h1": [], "i1": [], "j1": [], "k1": [],
                                "b2": [], "c2": [], "d2": [], "e2": [], "f2": [], "g2": [], "h2": [], "i2": [], "j2": [], "k2": [], 
                                "a3": [], "b3": [], "c3": [], "d3": [], "e3": [], "f3": [], "g3": [], "h3": [], "i3": [], "j3": [], "k3": [], 
                                "a4": [], "b4": [], "c4": [], "d4": [], "e4": [], "f4": [], "g4": [], "h4": [], "i4": [], "j4": [], 
                                "a5": [], "b5": [], "c5": [], "d5": [], "e5": [], "f5": [], "g5": [], "h5": [], "i5": []}

dummy_game_state = {"current_turn": "A",
                                "setup": False,
                                "selected": "",
                                "c1": ["magic"], "d1": ["B"], "e1": ["A"], "f1": ["B"], "g1": ["A"], "h1": ["B"], "i1": ["A"], "j1": ["B"], "k1": ["A"],
                                "b2": ["A"], "c2": ["magic"], "d2": ["A"], "e2": ["B"], "f2": ["A"], "g2": ["B"], "h2": ["A"], "i2": ["B"], "j2": ["A"], "k2": ["B"], 
                                "a3": ["A"], "b3": ["B"], "c3": ["A"], "d3": ["B"], "e3": ["A"], "f3": ["B"], "g3": ["A"], "h3": ["B"], "i3": ["A"], "j3": ["B"], "k3": ["A"], 
                                "a4": ["A"], "b4": ["B"], "c4": ["A"], "d4": ["B"], "e4": ["A"], "f4": ["magic"], "g4": ["A"], "h4": ["B"], "i4": ["A"], "j4": ["B"], 
                                "a5": ["A"], "b5": ["B"], "c5": ["A"], "d5": ["B"], "e5": ["A"], "f5": ["B"], "g5": ["A"], "h5": ["B"], "i5": ["A"]}

magics_to_place = 3
game_state = dummy_game_state

@app.route("/")
def hello():
    player = "A"
    game_state = game_state["current_turn"]
    return render_template("svg.html", game_state=game_state, player=player)

@app.route("/A/")
def hello_A():
    player = "A"
    return render_template("svg.html", game_state=game_state, player=player)

@app.route("/B/")
def hello_B():
    player = "B"
    return render_template("svg.html", game_state=game_state, player=player)

# @app.route("/reset/")
# def reset():
#     player = "A"
#     game_state = new_game_state
#     socketio.emit('update_board', game_state)
#     return "OK"
#     # return render_template("svg.html", game_state=game_state, player=player)

def next_player(player):
    if player == "A":
        return "B"
    if player == "B":
        return "A"
    return "uhoh"

@app.route("/new_click/<player>/<point>/", methods=["POST"])
def new_click(player, point):
    # Check if it's this user's turn
    if player != game_state["current_turn"]:
        socketio.emit('update_board', game_state)
        return "OK"
    do_game(player, point)
    socketio.emit('update_board', game_state)
    return "OK"

def do_game(player, point):
    # manage game logic

    if (game_state["setup"] == True):
        # change ownership of point if a user selects one
        if game_state[point] == "[]":
            if magics_to_place:
                game_state[point] = "magic"
                magics_to_place = magics_to_place - 1
            else:
                game_state[point] = player
            game_state["current_turn"] = next_player(player)
        return

    if (game_state["selected"] == point):
        # unselect current point
        game_state["selected"] = ""
    elif (game_state["selected"] == ""):
        # select point
        if (game_state[point][-1] == player):
            # make sure the stack belongs to this player
            game_state["selected"] = point
    else:
        if check_valid_move(game_state["selected"], point, player):
            # move a stack
            # add stack from old location onto the stack at the new location
            [game_state[point].append(a) for a in game_state[game_state["selected"]]]
            # set stack at old location to empty
            game_state[game_state["selected"]] = []
            game_state["selected"] = ""
            game_state["current_turn"] = next_player(player)
    return

def check_move_length(start_point, end_point):
        status = True
        move_length = 0
        row_move = ord(end_point[0]) - ord(start_point[0])
        row_delta = abs(row_move)
        column_move = int(end_point[1]) - int(start_point[1])
        column_delta = abs(column_move)
        if (start_point[0] == end_point[0]):
            # same column
            move_length = column_delta
        elif (start_point[1] == end_point[1]):
            # same row
            move_length = row_delta
        else:
            # only other move is across both rows and columns
            if row_delta != column_delta:
                # this move is "diagonal": The number of rows skipped has to equal the number of columns skipped
                return False
            if (column_move + row_move) != 0:
                # need to check that the diagonal is in the right direction
                # otherwise it would be possible to move from C2 to D3 for example
                # A valid diagonal move is either increasing in row number and decreasing in column number
                # or vice versa. As they're the same magnitude, adding together should == 0.
                return False
            move_length = row_delta
        if (move_length != len(game_state[start_point])):
            return False
        return True

def check_valid_move(start_point, end_point, player):
    if game_state[end_point] == []:
        # is destination empty?
        return False
    if surrounded(start_point):
        return False
    if not check_move_length(start_point, end_point):
        return False
    return True

def surrounded(point):
    # check if a point is surrounded.
    # only tiles that are not surrounded are allowed to move
    edge_points = ['']
    if point[1] in ['1', '5']:
        # top row and bottom row
        return False
    if point[0] in ['a', 'k']:
        # first column and last column
        return False
    if point in ['b2', 'j4']:
        return False
    if [] in [game_state[a] for a in get_valid_neighbours(point)]:
        # point has at least one empty neighbour
        return False
    return True

def get_valid_neighbours(point):
    # return names of neighbouring points

    column = ord(point[0])
    prev_column = chr(column-1)
    next_column = chr(column+1)
    row = int(point[1])
    prev_row = row-1
    next_row = row+1

    # dumb add all possible neighbours
    neighbours = []
    neighbours.append(chr(column-1)+str(row))
    neighbours.append(chr(column+1)+str(row))
    neighbours.append(chr(column)+str(row-1))
    neighbours.append(chr(column+1)+str(row-1))
    neighbours.append(chr(column-1)+str(row+1))
    neighbours.append(chr(column)+str(row+1))

    # remove neighbours that don't exist on the board
    bad_board_points = ["a1", "a2", "b1", "j5", "k4", "k5"]
    neighbours = [a for a in neighbours if a not in bad_board_points]
    neighbours = [a for a in neighbours if '0' not in a]
    neighbours = [a for a in neighbours if '6' not in a]
    neighbours = [a for a in neighbours if 'l' not in a]
    neighbours = [a for a in neighbours if '`' not in a]
    return neighbours

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)
    # socketio.run(app, host="0.0.0.0", debug=True)