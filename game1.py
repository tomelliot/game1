from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

new_game_state = {"current_turn": "A",
                                "player": "A",
                                "new_game": False,
                                "selected": [],
                                "c1": "A", "d1": "B", "e1": "blank", "f1": "blank", "g1": "blank", "h1": "blank", "i1": "blank", "j1": "blank", "k1": "blank",
                                "b2": "blank", "c2": "blank", "d2": "blank", "e2": "blank", "f2": "blank", "g2": "blank", "h2": "blank", "i2": "blank", "j2": "blank", "k2": "blank", 
                                "a3": "blank", "b3": "blank", "c3": "blank", "d3": "blank", "e3": "blank", "f3": "blank", "g3": "blank", "h3": "blank", "i3": "blank", "j3": "blank", "k3": "blank", 
                                "a4": "blank", "b4": "blank", "c4": "blank", "d4": "blank", "e4": "blank", "f4": "blank", "g4": "blank", "h4": "blank", "i4": "blank", "j4": "blank", 
                                "a5": "blank", "b5": "blank", "c5": "blank", "d5": "blank", "e5": "blank", "f5": "blank", "g5": "blank", "h5": "blank", "i5": "blank"}

game_state = new_game_state

@app.route("/")
def hello():
    game_state["player"] = game_state["current_turn"]
    return render_template("svg.html", game_state=game_state)

def next_player(player):
    if player == "A":
        return "B"
    if player == "B":
        return "A"
    return "uhoh"

@app.route("/new_click/<player>/<point>/", methods=["POST"])
def new_click(player, point):
    print request.get_json()
    if (game_state["selected"] == point):
        game_state["selected"] = ""
    else:
        game_state["selected"] = point
    socketio.emit('update_board', game_state)
    return "OK"

@app.route("/new_move/<player>/<point>/", methods=["POST"])
def new_move(player, point):
    print request.get_json()
    valid_move = True
    # if player != game_state["current_turn"]:
    #     valid_move = False
    if valid_move:
        game_state[point] = player
        game_state["current_turn"] = next_player(player)
    socketio.emit('update_board', game_state)
    return "OK"

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)
    # socketio.run(app, host="0.0.0.0", debug=True)