from flask_login import UserMixin

empty_point = [] # we use this to represent any point on the board that doesn't have any tiles on it

default_new_game_state = {"current_turn": "A",
                                "playerA":"A",
                                "playerB":"B",
                                "setup": True,
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
                                "selected": "",
                                "c1": ["magic"], "d1": ["B"], "e1": ["A"], "f1": ["B"], "g1": ["A"], "h1": ["B"], "i1": ["A"], "j1": ["B"], "k1": ["A"],
                                "b2": ["A"], "c2": ["magic"], "d2": ["A"], "e2": ["B"], "f2": ["A"], "g2": ["B"], "h2": ["A"], "i2": ["B"], "j2": ["A"], "k2": ["B"], 
                                "a3": ["A"], "b3": ["B"], "c3": ["A"], "d3": ["B"], "e3": ["A"], "f3": ["B"], "g3": ["A"], "h3": ["B"], "i3": ["A"], "j3": ["B"], "k3": ["A"], 
                                "a4": ["A"], "b4": ["B"], "c4": ["A"], "d4": ["B"], "e4": ["A"], "f4": ["magic"], "g4": ["A"], "h4": ["B"], "i4": ["A"], "j4": ["B"], 
                                "a5": ["A"], "b5": ["B"], "c5": ["A"], "d5": ["B"], "e5": ["A"], "f5": ["B"], "g5": ["A"], "h5": ["B"], "i5": ["A"]}

dummy_game_state1 = {"current_turn": "Tom",
                                "playerA":"Tom",
                                "playerB":"Rebort",
                                "setup": False,
                                "selected": "",
                                "c1": ["magic"], "d1": ["Rebort"], "e1": ["Tom"], "f1": empty_point, "g1": ["Tom"], "h1": ["Rebort"], "i1": ["Tom"], "j1": ["Rebort"], "k1": ["Tom"],
                                "b2": ["Tom"], "c2": ["magic"], "d2": ["Tom"], "e2": empty_point, "f2": ["Tom"], "g2": ["Rebort"], "h2": ["Tom"], "i2": ["Rebort"], "j2": ["Tom"], "k2": ["Rebort"], 
                                "a3": ["Tom"], "b3": ["Rebort"], "c3": ["Tom"], "d3": empty_point, "e3": ["Tom"], "f3": ["Rebort"], "g3": ["Tom"], "h3": ["Rebort"], "i3": ["Tom"], "j3": ["Rebort"], "k3": ["Tom"], 
                                "a4": ["Tom"], "b4": ["Rebort"], "c4": ["Tom"], "d4": empty_point, "e4": ["Tom"], "f4": empty_point, "g4": ["Tom"], "h4": ["Rebort"], "i4": ["Tom"], "j4": ["Rebort"], 
                                "a5": ["Tom"], "b5": ["Rebort"], "c5": ["Tom"], "d5": empty_point, "e5": ["magic"], "f5": empty_point, "g5": ["Tom"], "h5": ["Rebort"], "i5": ["Tom"]}

# this should be moved to db.py when its running from a database.
games = {'1': dummy_game_state1, '2':default_new_game_state}
games['1']['game_id'] = '1'
games['2']['game_id'] = '2'
game_id_counter = 9

class User(UserMixin):
    def __init__(self, name, img):
        self.id = name
        self.name = name
        self.img = img

tom=User("Tom", "img1")
rebort=User("Rebort", "img2")

users = {"Tom": tom, "Rebort": rebort}
# users = [{"name":"Tom", "img":"img1"}, 
#               {"name":"Rebort", "img":"img2"}]

user_games_list = {"Tom": [1, 2, 3],
                 "Rebort": [3, 4, 5]}

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)

#     def __init__(self, username, img):
#         self.username = username
#         self.img = img

#     def __repr__(self):
#         return '<User %r>' % self.username

#     @property
#     def is_active(self):
#         return True

#     @property
#     def is_authenticated(self):
#         return True

#     @property
#     def is_anonymous(self):
#         return False

#     def get_id(self):
#         try:
#             return text_type(self.id)
#         except AttributeError:
#             raise NotImplementedError('No `id` attribute - override `get_id`')

def save_game(game_id, game_state):
    global games
    games[game_id] = game_state

def get_game(game_id):
    return games[game_id]

def get_user_list():
    return users.keys()

def get_users_game_list(user):
# don't both with this until we have a database to make life easy.
    return games

def get_new_game_id():
    global game_id_counter
    new_game_id = str(game_id_counter)
    game_id_counter = game_id_counter + 1
    return new_game_id

def create_new_game(first_player, second_player, game_state):
    game_id = get_new_game_id()
    new_game_state = game_state
    new_game_state['current_turn'] = first_player
    new_game_state['playerA'] = first_player
    new_game_state['playerB'] = second_player
    save_game(game_id, new_game_state)
    return game_id
