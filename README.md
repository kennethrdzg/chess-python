# ChessAI
Repository for a chess game engine and an AI to play against

The "AI" is not a complete or true Artificial Intelligence. What the program does is explore a tree graph, using the current board state as the root and the possible moves as the branches. This process is repeated recursively until we reach a terminal node (checkmate or a stalemate) or until the tree reaches a particular depth, at which point it evaluates the board state and uses this value to select its next move. 

Current Objectives (in no particular order): 
	- En passant is currently unavailable for pawns as a legal move. 
	- Include command line options like the following
	  - "--depth [num]" to set a specific depth search
	  - "--time" to display execution time for best move search
	- Allow the player to undo moves.  
	- Allow a 2-player game
