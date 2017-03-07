from game1.db import get_game, save_game, games
import game1.db

empty_point = [] # we use this to represent any point on the board that doesn't have any tiles on it
game_points =   ["c1", "d1", "e1", "f1", "g1", "h1", "i1", "j1", "k1",
                            "b2", "c2", "d2", "e2", "f2", "g2", "h2", "i2", "j2", "k2", 
                            "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "i3", "j3", "k3", 
                            "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "i4", "j4", 
                            "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "i5"]

magics_to_place = 3


def create_new_game(first_player, second_player, game_state):
    return game1.db.create_new_game(first_player, second_player, game_state)

def next_player(game_state):
    if game_state["current_turn"] == game_state["playerA"]:
        return game_state["playerB"]
    else:
        return game_state["playerA"]

def do_game(player, game_id, point):
    # manage game logic
    game_state = get_game(game_id)
    if (game_state["setup"] == True):
        # change ownership of point if a user selects one
        if game_state[point] == empty_point:
            if magics_to_place:
                game_state[point] = "magic"
                magics_to_place = magics_to_place - 1
            else:
                game_state[point] = player
            game_state["current_turn"] = next_player(game_state)
        return

    if (game_state["selected"] == point):
        # unselect current point
        game_state["selected"] = ""
    elif (game_state["selected"] == ""):
        # select a point
        if (game_state[point][-1] == player):
            # make sure the stack belongs to this player
            game_state["selected"] = point
    else:
        if check_valid_move(game_state, game_state["selected"], point, player):
            # move a stack
            # add stack from old location onto the stack at the new location
            [game_state[point].append(a) for a in game_state[game_state["selected"]]]
            # set stack at old location to empty
            game_state[game_state["selected"]] = empty_point
            game_state["selected"] = ""
            game_state["current_turn"] = next_player(game_state)
    check_for_stranded_islands(game_state)
    save_game(game_id, game_state)
    return

def check_valid_move(game_state, start_point, end_point, player):
    if game_state[end_point] == empty_point:
        # is destination empty?
        return False
    if surrounded(game_state, start_point):
        return False
    if not check_move_length(game_state, start_point, end_point):
        return False
    return True

def check_move_length(game_state, start_point, end_point):
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

def check_for_stranded_islands(game_state):
    islands = get_islands(game_state, game_points)
    for island in islands:
        stranded = True
        for point in island:
            if 'magic' in game_state[point]:
                stranded = False
                break
        if stranded:
            for a in island:
                game_state[a] = empty_point
    return

def surrounded(game_state, point):
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
    if empty_point in [game_state[a] for a in get_valid_neighbours(point)]:
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

def get_islands(game_state, searchspace):
    unsearched_land = list(searchspace)
    islands = []
    island = []
    while True:
        island = build_island(game_state, unsearched_land[0], None)
        if not island:
            unsearched_land.remove(unsearched_land[0])
        else:
            [unsearched_land.remove(a) for a in island]
            islands.append(island)
        if len(unsearched_land) == 0:
            break
        pass
    return islands

def build_island(game_state, start_point="c1", island=None):
    # find islands of points that don't hold a magic piece
    # if game_state[start_point] == "" or game_state[start_point] == [""]:
    if game_state[start_point] == empty_point:
        return
    if island is None:
        island = []
    elif start_point not in island:
        island.append(start_point)

    neighbours = get_valid_neighbours(start_point)
    for a in neighbours:
        if a in island:
            continue
        land = build_island(game_state, a, island)
        if land:
            [island.append(b) for b in land if b not in island]
    return island
