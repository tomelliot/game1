from game1 import db

player_games = db.Table('player_games',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_state = db.Column(db.String(2000))
    game_type = db.Column(db.String(80))
    players = db.relationship('User', secondary=player_games, backref=db.backref('games', lazy='dynamic'))

    def __init__(self, game_state=None, game_type="game1", players=None):
        if game_state:
            self.game_state=game_state
        if game_type:
            self.game_type=game_type
        if players:
            self.players=players

    def __repr__(self):
        return '<Game %r>' % self.id
