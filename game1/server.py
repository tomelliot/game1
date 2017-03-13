from flask import Flask, url_for
from flask import render_template
from flask import request
from flask import redirect
from flask_login import login_required, current_user
import flask_login

from game1 import app, db, login_manager, socketio
from game1.logic import do_game
from game1 import db_api

from game1.models import User, Game
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
admin = Admin(app, name='game1', template_mode='bootstrap3')
# Create customized model view class
class MyModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and current_user.admin)

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Game, db.session))

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db_api.get_user(id=user_id)

@app.route("/")
def hello():
    return redirect(url_for("home"))

@app.route("/login")
@app.route("/login/")
def login():
    return render_template("login.html", users=db_api.get_users())

@app.route("/new_user/")
@app.route("/new_user")
def new_user():
    return render_template("new_user.html")

@app.route("/new_user/create/", methods=["POST"])
@app.route("/new_user/create", methods=["POST"])
def new_user_create():
    db_api.new_user(request.form['username'])
    return redirect(url_for("login"))

@app.route("/logout")
@app.route("/logout/")
def logout():
    flask_login.logout_user()
    return redirect(url_for("login"))

@app.route("/login/<user_id>")
@app.route("/login/<user_id>/")
def login_user(user_id):
    user = db_api.get_user(id=user_id)
    if user:
        flask_login.logout_user()
        flask_login.login_user(user, force=True)
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/home/")
@app.route("/home")
@login_required
def home():
    cu = current_user
    return render_template("home.html", user=cu.username, games=db_api.get_users_game_list(current_user))

@app.route("/game/<game_id>")
@app.route("/game/<game_id>/")
@login_required
def game(game_id):
    return render_template("svg.html", game_state=db_api.get_game_state(game_id), game_id=game_id, player=current_user.username)

@app.route("/new_game/")
@app.route("/new_game")
def new_game():
    return render_template("new_game.html", users=[a for a in db_api.get_users() if a.id != current_user.id])

@app.route("/new_game/<opponent_id>")
@app.route("/new_game/<opponent_id>/")
def spawn_new_game(opponent_id):
    game_id = db_api.create_new_game(current_user, db_api.get_user(id=int(opponent_id)))
    return redirect(url_for("game", game_id=game_id))

@app.route("/new_click/<player>/<game_id>/<point>/", methods=["POST"])
def new_click(player, game_id, point):
    # Check if it's this user's turn
    if player != db_api.get_game_state(game_id)["current_turn"]:
        socketio.emit('update_board', db_api.get_game_state(game_id))
        return "OK"
    do_game(player, game_id, point)
    socketio.emit('update_board', db_api.get_game_state(game_id))
    return "OK"

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)
    # socketio.run(app, host="0.0.0.0", debug=True)