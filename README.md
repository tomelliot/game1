# Game1

go to http://127.0.0.1:5000/A/ and http://127.0.0.1:5000/B/ to bring up a game

## To do
1. Backend
 - [x] Backend maintains game-state between users
 - [ ] Maintain multiple active games
 - [ ] User logins
 - [x] Backend enforces user turns
 - [ ] Backend enforces game rules
 - [ ] Tiles are lost if they're not connected to a magic tile
 - [ ] Highlight valid moves for user, once they've selected a tile
 - [ ] Set up a "reset" endpoint so I don't have to keep restarting the server

2. Frontend
 - [x] Generate game board
 - [ ] Only current player has tiles highlighted, not both players
 - [ ] Skin game board so it's not ugly
 - [ ] Draw tile stacks in reverse height order (so tall stacks overlap short stacks)
 - [ ] User login
 - [ ] Select active game
