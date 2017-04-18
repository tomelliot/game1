from game1 import db_api
from game1.db_api import magic_point, empty_point

player_A_token = "A"
player_B_token = "B"

empty_point = [] # we use this to represent any point on the board that doesn't have any tiles on it
game_points =   ["c1", "d1", "e1", "f1", "g1", "h1", "i1", "j1", "k1",
                            "b2", "c2", "d2", "e2", "f2", "g2", "h2", "i2", "j2", "k2", 
                            "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "i3", "j3", "k3", 
                            "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "i4", "j4", 
                            "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "i5"]

class game1():
    def __init__(self, game_id=None, first_player=None, second_player=None, game_state=None):
        if game_id is None:
            if first_player is None or second_player is None:
                raise ValueError("Need to specify either a game ID, or both of the players that will play this game")
                return
            if game_state:
                self.state = game_state
            else:
                self.state = db_api.default_new_game_state
            self.state['current_turn'] = first_player.username
            self.state['playerA'] = first_player.username
            self.state['playerB'] = second_player.username
            self.game_id = new_game(game_state=self.state, players=[first_player, second_player])
        else:
            self.state = db_api.get_game_state(game_id)
            self.game_id = game_id
        return

    def save_game(self):
        db_api.save_game(self.game_id, self.state)
        return

    def next_player(self):
        if self.state["current_turn"] == self.state["playerA"]:
            self.state["current_turn"] = self.state["playerB"]
        else:
            self.state["current_turn"] = self.state["playerA"]
        return self.state["current_turn"]

    def player_token(self):
        if self.state["playerA"] == self.state['current_turn']:
            player_token = player_A_token
        else:
            player_token = player_B_token
        return player_token

    def do_game(self, player, point):
        # manage game logic

        if (self.state["setup"] == True):
            # change ownership of point if a user selects one
            if self.state[point] == empty_point:
                if self.state["magics_to_place"]:
                    self.state[point] = [magic_point]
                    self.state["magics_to_place"] = self.state["magics_to_place"] - 1
                else:
                    self.state[point] = [self.player_token()]
                self.next_player()
            self.state["setup"] = False
            for point in game_points:
                if self.state[point] == empty_point:
                    self.state["setup"] = True
            if self.state["setup"] == False:
                self.state["current_turn"] = self.state["playerA"]  # Once set up is completed, PlayerA (aka white) gets to make the first move
            self.save_game()
            return

        if (self.state["selected"] == point):
            # unselect current point
            self.state["selected"] = ""
        elif (self.state["selected"] == ""):
            # select a point
            if (self.state[point][-1] == self.player_token()):
                # make sure the stack belongs to this player
                self.state["selected"] = point
        else:
            if self.check_valid_move(self.state["selected"], point, player):
                # move a stack
                # add stack from old location onto the stack at the new location
                [self.state[point].append(a) for a in self.state[self.state["selected"]]]
                # set stack at old location to empty
                self.state[self.state["selected"]] = empty_point
                self.state["selected"] = ""
                self.next_player()
        self.check_for_stranded_islands()
        if not self.get_valid_moves(self.player_token()):
            self.next_player()
        self.check_for_winner()
        self.save_game()
        return

    def check_valid_move(self, start_point, end_point, player):
        if self.state[end_point] == empty_point:
            # is destination empty?
            return False
        if self.surrounded(start_point):
            return False
        if not self.check_move_length(start_point, end_point):
            return False
        return True

    def check_move_length(self, start_point, end_point):
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
            if (move_length != len(self.state[start_point])):
                return False
            return True

    def check_for_stranded_islands(self):
        islands = self.get_islands(game_points)
        for island in islands:
            stranded = True
            for point in island:
                if magic_point in self.state[point]:
                    stranded = False
                    break
            if stranded:
                for a in island:
                    self.state[a] = empty_point
        return

    def surrounded(self, point):
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
        if empty_point in [self.state[a] for a in self.get_valid_neighbours(point)]:
            # point has at least one empty neighbour
            return False
        return True

    def get_valid_neighbours(self, point):
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

    def get_islands(self, searchspace):
        unsearched_land = list(searchspace)
        islands = []
        island = []
        while True:
            island = self.build_island(unsearched_land[0], None)
            if not island:
                unsearched_land.remove(unsearched_land[0])
            else:
                [unsearched_land.remove(a) for a in island]
                islands.append(island)
            if len(unsearched_land) == 0:
                break
            pass
        return islands

    def build_island(self, start_point="c1", island=None):
        # find all points connected to start_point using a recursive depth first search
        if self.state[start_point] == empty_point:
            return
        if island is None:
            island = []
        if start_point not in island:
            island.append(start_point)

        neighbours = self.get_valid_neighbours(start_point)
        for a in neighbours:
            if a in island:
                continue
            land = self.build_island(a, island)
            if land:
                [island.append(b) for b in land if b not in island]
        return island

    def get_valid_moves(self, player_token):
        moves = []
        for start_point in game_points:
            if len(self.state[start_point]) == 0:
                continue
            if self.state[start_point][-1] == player_token:
                # find valid moves
                end_points = self.get_valid_moves_from_point(player_token, start_point)
                new_moves = [(start_point, a) for a in end_points if len(a) != 0]
                if new_moves:
                    [moves.append(a) for a in new_moves]
        return moves

    def get_valid_moves_from_point(self, player_token, start_point):
        start_tiles = self.state[start_point]
        move_length = len(start_tiles)
        end_points = set()
        if start_tiles[-1] != player_token:
            return list(end_points)
        if self.surrounded(start_point):
            return list(end_points)

        for move_type in ["column", "row", "diagonal"]:
            for move_direction in [-1, 1]:
                end_point = self.get_end_point(start_point, move_type, move_direction*move_length)
                if end_point in game_points and self.state[end_point] != empty_point:
                    end_points.add(end_point)

        return list(end_points)

    def get_end_point(self, start_point, move_type, move_length):
        # for a tile at start_point, a given move_type, and a given move_length, where is the move's end_point?
        #
        # move_type: one of ["column", "row", "diagonal"]
        # move_length: depending on move_type:
        #     column: positive for increasing (from a towards k), negative for decreasing (from k towards a)
        #     row: positive for increasing, negative for decreasing
        #     diagonal: positive for increasing column (from a towards k), but decreasing row number.
        #                     negative for decreasing column (from k towards a), but increasing row number.

        if move_type not in ["column", "row", "diagonal"]:
            raise ValueError("Invalid move direction: %s" % move_type)
            return

        if move_type == "column":
            new_column = ord(start_point[0]) + move_length
            end_point = chr(new_column) + str(start_point[-1])
        elif move_type == "row":
            new_row = int(start_point[1]) + move_length
            end_point = start_point[0] + str(new_row)
        else:
            new_column = ord(start_point[0]) + move_length
            new_row = int(start_point[1]) - move_length
            end_point = chr(new_column) + str(new_row)

        if end_point not in game_points:
            return ""
        else:
            return end_point

    def check_for_winner(self):
        if self.get_valid_moves("A"):
            return False
        if self.get_valid_moves("B"):
            return False

        # count stacks to find winner
        result = {"A": 0, "B": 0, "m": 0}
        for point in game_points:
            tiles = self.state[point]
            if tiles != empty_point:
                result[tiles[-1]] = result[tiles[-1]] + len(tiles)
        self.state["result"] = result
        return True
