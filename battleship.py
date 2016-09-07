from random import randint

def gen_board(difficulty):
	board = []
	for x in range(difficulty):
		board.append(['?'] * difficulty)
	return board 
	
def diff_select():
	diff = '' 
	while diff != 'e' or diff != 'h':
		diff = raw_input("Please select a difficulty: E/H ").lower() 
		if diff == 'e':
			return 5
		elif diff == 'h':
			return 6 
		
			
"""Ensures player inputs a move that is on the grid, also used in ship generation to ensure that generated ships remain on the grid"""
def is_valid(row, col, difficulty):
	return (row >= 0 and row <= difficulty - 1) and (col >= 0 and col <= difficulty - 1)
	
def play_game():
	difficulty = diff_select()
	board = gen_board(difficulty) 
	gen_small(board, difficulty)
	gen_mid(board, difficulty) 
	guesses = difficulty - 1 
	subhits = 0
	midhits = 0
	subsunk = False
	midsunk = False
	print "Can you find the hidden ships?" 
	while guesses > 0:
		display_board(board)
		print "Chances remaining: %s" % guesses
		# the -1 in row and col are to compensate for the fact that humans would typically count 1-5, while the grid is 0-4. 
		row = int(raw_input("Guess row: ")) - 1
		col = int(raw_input("Guess column: ")) - 1 
		if not is_valid(row, col, difficulty):
			print "Out of range"
		elif board[row][col] != 'x' and board[row][col] != '?':
			print "HIT" 
			if board[row][col] == '1':
				board[row][col] = 's'
				subhits += 1
			elif board[row][col] == '2':
				board[row][col] = 'm'
				midhits += 1 
		elif board[row][col] == 'x':
			print "You've already chosen this spot"
		else: 
			print "MISS" 
			board[row][col] = 'x' 
			guesses -= 1 
		if subhits == 2 and not subsunk:
			print "You sunk my submarine!"
			subsunk = True 
		if midhits == 3 and not midsunk:
			print "You sunk my battleship!" 
			midsunk = True 
		if subhits == 2 and midhits == 3:
			print "YOU WON!"
			display_board(board)
			break
	if subhits != 2 or midhits != 3:
		print "You lost" 
		display_board(board) 
			
"""Used for ship generation to ensure no overlap"""
def is_occupied(board, row, col):
	if board[row][col] == '?':
		return True 
	else:
		return False 
		
def rand_row(board):
	return randint(0, len(board) - 1)
	
def rand_col(board): 
	return randint(0, len(board) - 1)
	
"""Makes a small sized ship, which takes up two spaces on the board"""
def gen_small(board, difficulty):
	vert_hor = randint(0,1) 
	gsrow = rand_row(board)
	gscol = rand_col(board)
	print "gsrow", gsrow
	print "gscol", gscol
	board[gsrow][gscol] = '1'
	if vert_hor == 0 and is_valid(gsrow, gscol + 1, difficulty):
		board[gsrow][gscol + 1] = '1' 
	elif vert_hor == 0 and is_valid(gsrow, gscol - 1, difficulty):
		board[gsrow][gscol - 1] = '1'
	if vert_hor == 1 and is_valid(gsrow + 1, gscol, difficulty):
		board[gsrow + 1][gscol] = '1' 
	elif vert_hor == 1 and is_valid(gsrow - 1, gscol, difficulty):
		board[gsrow - 1][gscol] = '1'

"""Makes a larger sized ship which takes up three spaces on the board""" 
def gen_mid(board, difficulty):
	print "Generating second ship" 
	vert_hor = randint(0,1) 
	switch = 0 
	msrow = rand_row(board)
	mscol = rand_col(board) 
	generated = False 
	print "msrow", msrow
	print "mscol", mscol 
	while not generated:
		if not is_occupied(board, msrow, mscol): #if it chooses an occupied spot as the first spot, reset 
			return gen_mid(board, difficulty)
		if is_occupied(board, msrow, mscol) and vert_hor == 0: #if valid spot chosen and horizontal placement
			if is_valid(msrow, mscol + 1, difficulty) and is_occupied(board, msrow, mscol + 1):
				if is_valid(msrow, mscol + 2, difficulty) and is_occupied(board, msrow, mscol + 2):
					board[msrow][mscol] = '2'
					board[msrow][mscol + 1] = '2'
					board[msrow][mscol + 2] = '2'
					generated = True
				elif is_valid(msrow, mscol - 1, difficulty) and is_occupied(board, msrow, mscol - 1):
					board[msrow][mscol] = '2'
					board[msrow][mscol + 1] = '2'
					board[msrow][mscol - 1] = '2'
					generated = True 
			elif is_valid(msrow, mscol - 1, difficulty) and is_occupied(board, msrow, mscol - 1):
				if is_valid(msrow, mscol - 2, difficulty) and is_occupied(board, msrow, mscol - 2):
					board[msrow][mscol] = '2'
					board[msrow][mscol - 1] = '2'
					board[msrow][mscol - 2] = '2' 
					generated = True 
				else: #horizontal placement impossible given starting location, switch to vertical placement 
					switch += 1 
					vert_hor = 1 
			else:
				switch += 1 
				vert_hor = 1 
				
		if is_occupied(board, msrow, mscol) and vert_hor == 1: #same as above block of code, except for vertical placement
			if is_valid(msrow + 1, mscol, difficulty) and is_occupied(board, msrow + 1, mscol):
				if is_valid(msrow + 2, mscol, difficulty) and is_occupied(board, msrow + 2, mscol):
					board[msrow][mscol] = '2'
					board[msrow + 1][mscol] = '2'
					board[msrow + 2][mscol] = '2'
					generated = True 
				elif is_valid(msrow - 1, mscol, difficulty) and is_occupied(board, msrow - 1, mscol):
					board[msrow][mscol] = '2'
					board[msrow + 1][mscol] = '2'
					board[msrow - 1][mscol] = '2'
					generated = True 
			elif is_valid(msrow - 1, mscol, difficulty) and is_occupied(board, msrow - 1, mscol): 
				if is_valid(msrow - 2, mscol, difficulty) and is_occupied(board, msrow - 2, mscol):
					board[msrow][mscol] = '2'
					board[msrow - 1][mscol] = '2'
					board[msrow - 2][mscol] = '2' 
					generated = True 
				else:
					switch += 1
					vert_hor = 0 
			else:
				switch += 1 
				vert_hor = 0 
			
			if switch == 2:
				break 
	
	if switch == 2: #horizontal and vertical placement impossible given initial starting point 
		gen_mid(board, difficulty) 
			
def display_board(board):
	for row in board:
		display = ' '.join(row) 
		#display = display.replace('1' , '?') 
		#display = display.replace('2', '?') 
		print display
		
play_game() 
