###### This File is to test the effectiveness of the three different algorithms: random, minimax, and modified alpha beta ##############

import numpy as np
import pygame
import sys
import random
import math
###################### CONSTANTS ##################
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 8
COLUMN_COUNT = 10

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

ONE_COUNT = 0 
TWO_COUNT = 0
#####################################################


###########Board Creation from FreeCodeCamp: https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py ##########################
def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

###########################################################


#######Developed Algorithm for Random ##########################
def choose_random(columns):
    choose_column = random.randint(0,columns-1)
    return choose_column 

######################################################

############Modified Algorithm for Minimax and Alpha-Beta (Alpha and Beta pruning can be removed to test combos with just normal Minimax) - Implemented based
# on example from FreeCodeCamp  ###################
def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE


######### Changed weightings to make more optimal ###########################
	if window.count(piece) == 4:
		score += 200
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 10
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 4

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 8

	return score

########################################################################
def score_position(board, piece):
	score = 0
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score


def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: 
				return (None, 0)
		else: 
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: 
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col
##################### Modified to work with scenarios where there is a predetermined move, rather than using mouse cursor ###########################
for i in range(100):   # For testing make a small number like 3, since it takes forever to run 
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    pygame.init()

    SQUARESIZE = 100

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT+1) * SQUARESIZE

    size = (width, height)

    RADIUS = int(SQUARESIZE/2 - 5)

    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    while not game_over:
        if turn == 0:
            col = choose_random(10) #choose between random, minimax (remove alpha beta pruning from algo), or the alpha-beta
            #col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                ONE_COUNT += 1
                game_over = True

        else:				
            col = choose_random(10)   #choose between random, minimax (remove alpha beta pruning from algo), or the alpha-beta
            #col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                game_over = True
                TWO_COUNT += 1  

        print_board(board)
        draw_board(board)

        turn += 1
        turn = turn % 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if game_over:
        pygame.time.wait(3000)
        print("Algo One Wins:", ONE_COUNT)
        print("Algo Two Wins:", TWO_COUNT)
    ################################################

        