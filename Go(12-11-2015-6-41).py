import pygame
from pygame.locals import *
import copy
list_of_boards = [[[[0, x, y] for y in range(0,19)]for x in range(0,19)], [[[0, x, y] for y in range(0,19)]for x in range(0,19)]]
move_list = []
#Establishes which player is playing
def player_move(turn):
	

	if turn % 2 == 0:
		player = 1
	else:
		player = 2

	if player == 1:
		enemy_player = 2
	else:
		enemy_player = 1
	
	return player, enemy_player

#Creates the board storage,with piece information and position # y is vertical (index[1]) x is horizontal (index[2])	
# y is vertical (index[1]) x is horizontal (index[2])
def make_board():
	board = [[[0, x, y] for y in range(0,19)]for x in range(0,19)]
	return board

#Prints board in terminal
#def print_board(board):
#	for row in board:
#		print row

#Manages search algorithm and controls piece capture
def gameplay_logic(board, player, enemy_player):
		
	for row in board:
		for index in row:
			temp_list = []
			if index[0] == enemy_player:
				temp_list.append([index[0], index[1], index[2]])
				search_all(enemy_player, board, index[1], index[2], temp_list)
				perimeter_ammend(board, enemy_player, temp_list)
			else:
				pass

#Combines all directional search functions to create the cycle
def search_all(enemy_player, board, vertical_index, horizontal_index, temp_list):
	found = True
	while found:
		found = False
		for item in temp_list:
			found_right_piece = search_right(board, item[1], item[2] )
			if found_right_piece and found_right_piece not in temp_list and found_right_piece[0] == enemy_player:
				temp_list.append([found_right_piece[0], found_right_piece[1], found_right_piece[2]])
				found = True
		for item in temp_list:
			found_down_piece = search_down(board, item[1], item[2] )
			if found_down_piece and found_down_piece not in temp_list and found_down_piece[0] == enemy_player:
				temp_list.append([found_down_piece[0], found_down_piece[1], found_down_piece[2]])
				found = True
		for item in temp_list:
			found_left_piece = search_left(board, item[1], item[2] )
			if found_left_piece and found_left_piece not in temp_list and found_left_piece[0] == enemy_player:
				temp_list.append([found_left_piece[0], found_left_piece[1], found_left_piece[2]])
				found = True
		for item in temp_list:
			found_up_piece = search_up(board, item[1], item[2] )
			if found_up_piece and found_up_piece not in temp_list and found_up_piece[0] == enemy_player:
				temp_list.append([found_up_piece[0], found_up_piece[1], found_up_piece[2]])
				found = True	

def search_right(board, vertical_index, horizontal_index):
	if board[vertical_index][horizontal_index][2] == 18:
		found_piece = [99,99,99]
	else:
		found_piece = board[vertical_index][horizontal_index+1]
	return found_piece 

def search_down(board, vertical_index, horizontal_index):
	if board[vertical_index][horizontal_index][1] == 18:
		found_piece = [99, 99, 99]
	else:
		found_piece = board[vertical_index+1][horizontal_index]
	return found_piece

def search_left(board, vertical_index, horizontal_index):
	if board[vertical_index][horizontal_index][2] == 0:
		found_piece = [99, 99, 99]
	else:
		found_piece = board[vertical_index][horizontal_index-1]
	return found_piece

def search_up(board, vertical_index, horizontal_index):
	if board[vertical_index][horizontal_index][1] == 0:
		found_piece = [99, 99, 99]
	else:
		found_piece = board[vertical_index-1][horizontal_index]
	return found_piece

#Capture function
def perimeter_ammend(board, enemy_player, temp_list):
	for i in range(0, len(temp_list)):
		temp_list.append(search_right(board, temp_list[i][1], temp_list[i][2]))
		temp_list.append(search_down(board, temp_list[i][1], temp_list[i][2]))
		temp_list.append(search_left(board, temp_list[i][1], temp_list[i][2]))
		temp_list.append(search_up(board, temp_list[i][1], temp_list[i][2]))
	liberty = False	
	for i in range(0, len(temp_list)):
		if temp_list[i][0] == 0:
			liberty = True
		else:
			pass
	if not liberty:
		for i in range(0, len(temp_list)):
			if temp_list[i][0] == enemy_player:
				board[temp_list[i][1]][temp_list[i][2]][0] = 0
			else:
				pass

#Visual interface prompt informing of player turn		
def player_print(player, screen):
	
	myfont = pygame.font.SysFont("monospace", 25)
	if player == 1:
		playcolour = "Black"
	else:
		playcolour = "White"
	player_update = myfont.render("It is {}'s go!".format(playcolour), 1, (0,0,0))
	screen.blit(player_update, (50, 967))

#Creates a list of exisitng pieces on the current board for quick reference by the program			
def get_grid(board):
    living_pieces = []
    for row in board:
	for i in row:
	    if i[0] != 0:
		living_pieces.append((i[0], i[1], i[2]))
	    else:
	    	pass
    return living_pieces

#Logic for establishing mouse position and returning it, playing pieces and contains logic to halt turn if trying to play on a taken place, suicide moves or breaking Ko
def mouse_processing(board, player, living_pieces, screen, enemy_player, pass_button, pass_count, turn, board_turn):
	board_position_x = "no click"
	board_position_y = "no click"
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONUP:
			mouse_position = pygame.mouse.get_pos()
			if pass_button.collidepoint(mouse_position[0], mouse_position[1]):
				pass_count += 1
				turn += 1
				break
			else:
				pass
			board_position_x = mouse_position[0] / 50
			board_position_y = mouse_position[1] / 50
			if board_position_y > 18 or board_position_x > 18:
				board_position_x = "no click"
				board_position_y = "no click"
			else:
				pass
			print "\nHORIZONTAL" + str(board_position_x)
			print "VERTICAL" + str(board_position_y)
			#Stops playing on occupied spaces
			if board_position_x == "no click" or board_position_y == "no click":
				pass
			else:	
				for piece in living_pieces:
					if int(board_position_x) == int(piece[2]) and int(board_position_y) == int(piece[1]):
						if player == 1:
							playcolour = "Black"
						else:
							playcolour = "White"
						myfont = pygame.font.SysFont("monospace", 15)
						taken_space_warning = myfont.render("That place is taken {}. Please pick another place".format(playcolour), 1, (0,0,0))
						screen.blit(taken_space_warning, (400, 967))
			
						board_position_x = "no click"
						board_position_y = "no click"
						pass
					else:
						pass
			#Stops suicide moves
			#program considers the move, creates temp group using search all, sees if its full, if it is give warning of a suicide move and asks user to take their go again
			if board_position_x == "no click" or board_position_y == "no click":
				pass
			else:
				temp_list = []
				temp_list.append((player, board_position_y, board_position_x))
				search_all(player, board, board_position_y, board_position_y, temp_list)
				suicide_capture = True
				for cord in temp_list:
					if cord[0] == 0:
						suicide_capture = False
					else:
						pass
				if suicide_capture:
					pass
				else:
					temp_list = []
					temp_list.append((player, board_position_y, board_position_x))
					search_all(player, board, board_position_y, board_position_x, temp_list)
					for i in range(0, len(temp_list)):
						temp_list.append(search_right(board, temp_list[i][1], temp_list[i][2]))
						temp_list.append(search_down(board, temp_list[i][1], temp_list[i][2]))
						temp_list.append(search_left(board, temp_list[i][1], temp_list[i][2]))
						temp_list.append(search_up(board, temp_list[i][1], temp_list[i][2]))
					liberty = False	
					for i in range(0, len(temp_list)):
						if temp_list[i][0] == 0:
							liberty = True
						else:
							pass
					if not liberty:
						if player == 1:
							playcolour = "Black"
						else:
							playcolour = "White"
						myfont = pygame.font.SysFont("monospace", 15)
						suicide_warning = myfont.render("Do you want to die {}?. Please pick another place".format(playcolour), 1, (0,0,0))
						screen.blit(suicide_warning, (400, 967))
						board_position_x = "no click"
						board_position_y = "no click"
						temp_list = []
			#Stops breaking Ko
			if board_position_x == "no click" or board_position_y == "no click":
				pass 	
			else:
				print list_of_boards
				temp_board = copy.deepcopy(board)
				temp_board[board_position_y][board_position_x][0] = player
				print temp_board
				if temp_board == list_of_boards[board_turn-2] or temp_board == list_of_boards[board_turn-1]:
					print "invaild"
					if player == 1:
						playcolour = "Black"
					else:
						playcolour = "White"
					myfont = pygame.font.SysFont("monospace", 15)
					taken_space_warning = myfont.render("You are breaking ko {}. Please pick another place".format(playcolour), 1, (0,0,0))
					screen.blit(taken_space_warning, (400, 967))
			
					board_position_x = "no click"
					board_position_y = "no click"
				else:
					list_of_boards.append(temp_board)
					pass
			break


		else:
			pass
	return board_position_x, board_position_y, turn, pass_count   


#def board_save(board, turn):
#	list_of_boards.append(board)
#	return list_of_boards

#scans current terminal board state and translates it to the GUI board
def circle_generate(screen, position_x, position_y, player, board):
	for row in board:
		for i in row:
			if i[0] == 2:
				colour = (255,255,255)
			else:
				colour = (0,0,0,)
			if i[0] == 1 or i[0] == 2:
				pygame.draw.circle(screen, colour, (25 + i[2] * 50, 25 + i[1] * 50), 25, 0) 
			else:
				pass

def victory_score(living_pieces, board, screen):
	white_liberty = 0
	black_liberty = 0
	for p in living_pieces:
		if p[0] == 1:
			black_piece = [] 
			black_piece.append(search_right(board, p[1], p[2]))
			black_piece.append(search_down(board, p[1], p[2]))
			black_piece.append(search_left(board, p[1], p[2]))
			black_piece.append(search_up(board, p[1], p[2]))
			for b in black_piece:
				if b[0] == 0:
					black_liberty += 1

		elif p[0] == 2:
			white_piece = [] 
			white_piece.append(search_right(board, p[1], p[2]))
			white_piece.append(search_down(board, p[1], p[2]))
			white_piece.append(search_left(board, p[1], p[2]))
			white_piece.append(search_up(board, p[1], p[2]))
			for w in white_piece:
				if w[0] == 0:
					white_liberty += 1
		else:
			pass
	myfont = pygame.font.SysFont("monospace", 15)
	white_score = myfont.render("WHITE: {}".format(white_liberty), 1, (0,0,0))
	black_score = myfont.render("BLACK: {}".format(black_liberty), 1, (0,0,0))
	pygame.draw.rect(screen, (255, 255, 255),(965, 80 , 80, 80))
	screen.blit(white_score, (965, 80))
	screen.blit(black_score, (965, 120))

#Will establish the game window, main control flow for the game 
def main():
	pygame.init()
	pygame.display.set_caption('Go!')
	screen = pygame.display.set_mode((1050,1000))
	pygame.draw.rect(screen, (255, 255, 255),(0, 950, 950, 50))
	pygame.draw.rect(screen, (255, 255, 255),(950, 0, 100, 1000))
	#pygame.draw.lines(screen, (0,0,0), True, [(960, 15), (1040, 15), (1040, 55), (960, 55)], 5)
	pass_button = pygame.draw.rect(screen, (255,0,0), (962,17, 76, 36))
	myfont = pygame.font.SysFont("monospace", 30)
	pass_button_text = myfont.render("PASS", 1, (0,0,0))
	screen.blit(pass_button_text, (965, 20))
	go_graph_board = pygame.image.load('Blank_Go_board.png')
	stop_play = False
	board = make_board()
	turn = 0
	board_turn = 2
	screen.blit(go_graph_board, (0, 0))
	pass_count = 0
	while not stop_play:
		if pass_count == 2:
			stop_play = True
		else:
			pass
		pygame.display.update()
		player, enemy_player = player_move(turn)
		player_print(player, screen)
		
		living_pieces = get_grid(board)
		position_x, position_y, turn, pass_count = mouse_processing(board, player, living_pieces, screen, enemy_player, pass_button, pass_count, turn, board_turn)
		if position_x == "no click":
			continue
		else:
			#list_of_boards = board_save(board, turn)
			pass_count = 0
			move_list.append((player, position_y, position_x))
			screen.blit(go_graph_board, (0, 0))
			board[position_y][position_x][0] = player
			pygame.display.update()
			gameplay_logic(board, player, enemy_player)
			circle_generate(screen, position_x, position_y, player, board)
			#print_board(board)
			turn += 1
			board_turn += 1
			pygame.draw.rect(screen, (255, 255, 255),(0, 950, 950, 50))
			living_pieces = get_grid(board) 
			victory_score(living_pieces, board, screen)
	pygame.display.update()

main()





