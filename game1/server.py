from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import redirect
from flask_login import login_required, current_user
import flask_login

from game1 import app, db, login_manager, socketio
from game1.logic import do_game, create_new_game, games
from game1.db import get_game, users, user_games_list

@login_manager.user_loader
def load_user(user_id):
    return users[user_id]

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

@app.route("/login")
@app.route("/login/")
def login():
    return render_template("login.html", users=users.keys())

@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect("/login")

@app.route("/login/<user>")
def login_user(user):
    # if user in [a['name'] for a in users]:
    if user in users:
        flask_login.login_user(users[user], force=True)
        return redirect("/home/")
    return redirect("/login")

@app.route("/home/")
@app.route("/home")
@login_required
def home():
    cu = current_user
    return render_template("home.html", user=cu.name, games=user_games_list[cu.name])

@app.route("/game/<game_id>")
@login_required
def game(game_id):
    return render_template("svg.html", game_state=games[game_id], player=current_user.name)

@app.route("/new_game/<player>/")
@app.route("/new_game/<player>")
def new_game(player):
    return render_template("new_game.html", player=player, users=[a for a in get_user_list() if a != player])

@app.route("/new_game/<player>/<opponent>")
@app.route("/new_game/<player>/<opponent>/")
def spawn_new_game(player, opponent):
    game_id = create_new_game(player, opponent)
    return redirect("/game/"+str(game_id))

@app.route("/new_click/<player>/<game_id>/<point>/", methods=["POST"])
def new_click(player, game_id, point):
    # Check if it's this user's turn
    if player != get_game(game_id)["current_turn"]:
        socketio.emit('update_board', get_game(game_id))
        return "OK"
    do_game(player, game_id, point)
    socketio.emit('update_board', get_game(game_id))
    return "OK"

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)
    # socketio.run(app, host="0.0.0.0", debug=True)