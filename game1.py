from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

game_state = {"current_turn": "player1", "new_game": True}
# remote_points = 5

@app.route("/")
def hello():
    return render_template("svg.html", game_state=game_state)
    # return render_template("svg.html")

@app.route("/new_move/<player>/<point>/", methods=["POST"])
def new_move(player, point):
    print request.json
    print request.get_json()
    game_state["new_game"] = False
    return render_template("svg.html", game_state=game_state)

if __name__ == "__main__":
    app.run(debug=True)