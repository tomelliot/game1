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
                                "c1": ["A"], "d1": ["B"], "e1": ["A"], "f1": ["B"], "g1": ["A"], "h1": ["B"], "i1": ["A"], "j1": ["B"], "k1": ["A"],
                                "b2": ["A"], "c2": ["B"], "d2": ["A"], "e2": ["B"], "f2": ["A"], "g2": ["B"], "h2": ["A"], "i2": ["B"], "j2": ["A"], "k2": ["B"], 
                                "a3": ["A"], "b3": ["B"], "c3": ["A"], "d3": ["B"], "e3": ["A"], "f3": ["B"], "g3": ["A"], "h3": ["B"], "i3": ["A"], "j3": ["B"], "k3": ["A"], 
                                "a4": ["A"], "b4": ["B"], "c4": ["A"], "d4": ["B"], "e4": ["A"], "f4": ["B"], "g4": ["A"], "h4": ["B"], "i4": ["A"], "j4": ["B"], 
                                "a5": ["A"], "b5": ["B"], "c5": ["A"], "d5": ["B"], "e5": ["A"], "f5": ["B"], "g5": ["A"], "h5": ["B"], "i5": ["A"]}


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
            game_state[point] = player
            game_state["current_turn"] = next_player(player)
        return

    if (game_state["selected"] == point):
        # unselect current point
        game_state["selected"] = ""
    elif (game_state["selected"] == ""):
        # select point
        game_state["selected"] = point
    else:
        # move a stack
        [game_state[point].append(a) for a in game_state[game_state["selected"]]]
        game_state[game_state["selected"]] = []
        game_state["selected"] = ""
        game_state["current_turn"] = next_player(player)
    return

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)
    # socketio.run(app, host="0.0.0.0", debug=True)