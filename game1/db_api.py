from flask_login import UserMixin
# from game1.models import User as sqluser
from game1 import db, models
import json

empty_point = [] # we use this to represent any point on the board that doesn't have any tiles on it
magic_point = "m"

default_new_game_state = {"current_turn": "A",
                                "playerA":"A",
                                "playerB":"B",
                                "setup": True,
                                "magics_to_place":3,
                                "selected": "",
                                "c1": empty_point, "d1": empty_point, "e1": empty_point, "f1": empty_point, "g1": empty_point, "h1": empty_point, "i1": empty_point, "j1": empty_point, "k1": empty_point,
                                "b2": empty_point, "c2": empty_point, "d2": empty_point, "e2": empty_point, "f2": empty_point, "g2": empty_point, "h2": empty_point, "i2": empty_point, "j2": empty_point, "k2": empty_point, 
                                "a3": empty_point, "b3": empty_point, "c3": empty_point, "d3": empty_point, "e3": empty_point, "f3": empty_point, "g3": empty_point, "h3": empty_point, "i3": empty_point, "j3": empty_point, "k3": empty_point, 
                                "a4": empty_point, "b4": empty_point, "c4": empty_point, "d4": empty_point, "e4": empty_point, "f4": empty_point, "g4": empty_point, "h4": empty_point, "i4": empty_point, "j4": empty_point, 
                                "a5": empty_point, "b5": empty_point, "c5": empty_point, "d5": empty_point, "e5": empty_point, "f5": empty_point, "g5": empty_point, "h5": empty_point, "i5": empty_point}

dummy_game_state = {"current_turn": "A",
                                "playerA":"A",
                                "playerB":"B",
                                "setup": False,
                                "magics_to_place":3,
                                "selected": "",
                                "c1": [magic_point], "d1": ["B"], "e1": ["A"], "f1": ["B"], "g1": ["A"], "h1": ["B"], "i1": ["A"], "j1": ["B"], "k1": ["A"],
                                "b2": ["A"], "c2": [magic_point], "d2": ["A"], "e2": ["B"], "f2": ["A"], "g2": ["B"], "h2": ["A"], "i2": ["B"], "j2": ["A"], "k2": ["B"], 
                                "a3": ["A"], "b3": ["B"], "c3": ["A"], "d3": ["B"], "e3": ["A"], "f3": ["B"], "g3": ["A"], "h3": ["B"], "i3": ["A"], "j3": ["B"], "k3": ["A"], 
                                "a4": ["A"], "b4": ["B"], "c4": ["A"], "d4": ["B"], "e4": ["A"], "f4": [magic_point], "g4": ["A"], "h4": ["B"], "i4": ["A"], "j4": ["B"], 
                                "a5": ["A"], "b5": ["B"], "c5": ["A"], "d5": ["B"], "e5": ["A"], "f5": ["B"], "g5": ["A"], "h5": ["B"], "i5": ["A"]}

dummy_game_state1 = {"current_turn": "Tom",
                                "playerA":"Tom",
                                "playerB":"Rebort",
                                "setup": False,
                                "magics_to_place":3,
                                "selected": "",
                                "c1": [magic_point], "d1": ["B"], "e1": ["A"], "f1": empty_point, "g1": ["A"], "h1": ["B"], "i1": ["A"], "j1": ["B"], "k1": ["A"],
                                "b2": ["A"], "c2": [magic_point], "d2": ["A"], "e2": empty_point, "f2": ["A"], "g2": ["B"], "h2": ["A"], "i2": ["B"], "j2": ["A"], "k2": ["B"], 
                                "a3": ["A"], "b3": ["B"], "c3": ["A"], "d3": empty_point, "e3": ["A"], "f3": ["B"], "g3": ["A"], "h3": ["B"], "i3": ["A"], "j3": ["B"], "k3": ["A"], 
                                "a4": ["A"], "b4": ["B"], "c4": ["A"], "d4": empty_point, "e4": ["A"], "f4": empty_point, "g4": ["A"], "h4": ["B"], "i4": ["A"], "j4": ["B"], 
                                "a5": ["A"], "b5": ["B"], "c5": ["A"], "d5": empty_point, "e5": [magic_point], "f5": empty_point, "g5": ["A"], "h5": ["B"], "i5": ["A"]}

def new_user(username):
    new_user = models.User(username)
    db.session.add(new_user)
    db.session.commit()
    return new_user.id

def new_game(game_state="", game_type="game1", players=None):
    json_game_state = json.dumps(game_state)
    game = models.Game(json_game_state, game_type)
    for player in players:
        game.players.append(player)
    db.session.add(game)
    db.session.commit()
    return game.id

def save_game(game_id, game_state):
    game = models.Game.query.filter_by(id=game_id).first()
    game.game_state = json.dumps(game_state)
    db.session.commit()

def get_game(game_id):
    game = models.Game.query.filter_by(id=game_id).first()
    return game

def get_game_state(game_id):
    game = models.Game.query.filter_by(id=game_id).first()
    return json.loads(game.game_state)

def get_user_list():
    return users.keys()

def get_users():
    return models.User.query.all()

def get_usernames():
    return [a.username for a in models.User.query.all()]

def get_user(id=None, username=None):
    if id:
        return models.User.query.filter_by(id=id).first()
    if username:
        return models.User.query.filter_by(username=username)
    return None

def get_users_game_list(user):
    return user.games.all()

def create_new_game(first_player, second_player, game_state=None):
    if game_state:
        new_game_state = game_state
    else:
        new_game_state = default_new_game_state
    new_game_state['current_turn'] = first_player.username
    new_game_state['playerA'] = first_player.username
    new_game_state['playerB'] = second_player.username
    game_id = new_game(game_state=new_game_state, players=[first_player, second_player])
    return game_id
