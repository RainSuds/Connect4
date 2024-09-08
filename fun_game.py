#    By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Giovan Ramirez-Rodarte
#               Samantha Christian
#               Tee Li
#               Michael Dukissis
# Section:      576
# Assignment:   13 LAB: Game Plan
# Date:         06 Dec 2022


import random as rd  # random number
import tkinter as tk  # popup window
import numpy as np # import np for board
import pygame  # for game
import sys  # for system stuff
import math 

#global variables
row_count = 6
col_count = 7

#colors
maroon = (128,0,0)
dark_blue = (0,0,139)
violet = (238,130,238)
black = (0,0,0)
white = (255, 255, 255)


### BOARD FUNCTION ###
def board():
    """
    Create a numpy array with x rows and y columns, generate a board with all zeros.

    Parameters
    ----------
    x (int): row_count
    y (int): col_count

    Returns
    -------
    board : array
        A 6*7 board filled with zeros.

    """
    board = np.zeros((row_count, col_count))
    return board

def board_flipped(board):
    """
    Printing the board with the bottommost row as index [0].

    Parameters
    ----------
    board : array
        Take in board then printing it flipped.

    Returns
    -------
    None.

    """
    print(np.flip(board, 0)) # 0 is the orientation

def drop_pieces(board, row, col, piece):
    """
    Replace each 0 piece a piece.

    Parameters
    ----------
    board : array
        The array surface of the game.
    row : int
        The x coordinate of the piece.
    col : int
        The y coordinate of the piece.
    piece : int
        The piece which the player or AI is placing on the board.

    Returns
    -------
    None.

    """
    board[row][col] = piece

def check_valid_location(board, col):
    return board[row_count - 1][col] == 0

def get_next_row(col):
    for row in range(row_count):
        if board[row][col] == 0:
            return row

def win_move(board, piece):
    #horizontal
    for col in range(col_count - 3):
        for row in range(row_count):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True
    #vertical 
    for col in range(col_count):
        for row in range(row_count - 3):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True
            
    #positive slope diagonal 
    for col in range(col_count - 3):
        for row in range(row_count - 3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True
            
    #negative sloped diagonal 
    for col in range(col_count - 3):
        for row in range(3 ,row_count):
            if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True


def draw_check():
    sumb = 0
    
    #Check draw
    for x in range(col_count):
        for r in range(row_count):
            sumb += 1
    if sumb == 63:
        return True
    else:
        return False

def create_board(board):
    
    #draw board
    for col in range(col_count): #for every column
        for row in range(row_count): #for every row
            pygame.draw.rect(game_screen, dark_blue, (col * square_size, row * square_size + square_size, square_size, square_size))
            pygame.draw.circle(game_screen, black, (int(col * square_size + square_size / 2), int(row * square_size + square_size + square_size / 2)), radius)
            
    #draw pieces
    for col in range(col_count): #for every column
        for row in range(row_count): #for every row
            if board[row][col] == 1:
                pygame.draw.circle(game_screen, maroon, (int(col * square_size + square_size /2), height - int(row * square_size + square_size/2 )), radius)
            elif board[row][col] == 2:
                pygame.draw.circle(game_screen, violet, (int(col * square_size + square_size /2) , height - int(row * square_size + square_size/2 )), radius)
    
    pygame.display.update()


### FILE FUNCTIONS ###
def add_winners(winner):  # appends winner for each round
    with open("Win_Loss.txt", "a") as myfile:
        if winner.lower() == "player1":
            myfile.write("Win Player1! \n")

        elif winner.lower() == "computer":
            myfile.write("Win Computer! \n")

        else:
            myfile.write("Draw! \n")

def score():  # checks the current score
	try:
		with open("Win_Loss.txt", "r") as myfile:
			players = []
			player1 = 0
			computer = 0
			draw = 0

			for line in myfile:
				result, player = line.strip().split()
				players.append([result, player])

		for i in range(len(players)):
			current = players[i]

			if current[-1] == "Player1!":
				if current[0] == "Win":
					player1 += 1

				if current[-1] == "Computer!":
					if current[0] == "Win":
						computer += 1

				if current == "Draw!":
					draw += 1
	except ValueError:
		player1 = 0
		computer = 0
		draw = 0

	return player1, computer, draw

### LEARN SOMETHING NEW FUNCTION (GUI FOR W/L/D) ###
def animate_win():  # for a W:)
	reg_font = ("Verdana", 100)
	msg = "You WON!"
	msg2 = ":)"
	### POPUP CONFIG ###
	popup = tk.Tk()
	popup.minsize(800, 600)
	popup.wm_title("Result")
	w = popup.winfo_screenwidth()  # gets info from comp
	h = popup.winfo_screenheight()
	x = int(int(w / 2) - int(1000 / 2))
	y = int(int(h / 2) - int(1000 / 2))
	popup.geometry(f"1000x1000+{x}+{y}")  # equation to display in center
	### TEXT ###
	text = tk.Label(popup, text=msg, font=reg_font)
	text.pack(side="top")
	### BUTTON ###
	b1 = tk.Button(popup, text=msg2, font=reg_font, command=popup.destroy)
	b1.config(height=5, width=10)
	b1.pack()
	
	popup.mainloop()


def animate_loss():  # for an L:
	reg_font = ("Verdana", 100)
	msg = "You LOST!"
	msg2 = ":("
	### POPUP CONFIG ###
	popup = tk.Tk()
	popup.minsize(800, 600)
	popup.wm_title("Result")
	w = popup.winfo_screenwidth()  # gets info from comp
	h = popup.winfo_screenheight()
	x = int(int(w / 2) - int(1000 / 2))
	y = int(int(h / 2) - int(1000 / 2))
	popup.geometry(f"1000x1000+{x}+{y}")  # equation to display in center
	### TEXT ###
	text = tk.Label(popup, text=msg, font=reg_font)
	text.pack(side="top")
	### BUTTON ###
	b1 = tk.Button(popup, text=msg2, font=reg_font, command=popup.destroy)
	b1.config(height=5, width=10)
	b1.pack()

	popup.mainloop()


def animate_draw():  # for a draw 
	reg_font = ("Verdana", 100)
	msg = "DRAW!"
	msg2 = "Really Dude... :|"
	### POPUP CONFIG ###
	popup = tk.Tk()
	popup.minsize(800, 600)
	popup.wm_title("Result")
	w = popup.winfo_screenwidth()  # gets info from comp
	h = popup.winfo_screenheight()
	x = int(int(w / 2) - int(1000 / 2))
	y = int(int(h / 2) - int(1000 / 2))
	popup.geometry(f"1000x1000+{x}+{y}")  # equation to display in center
	### TEXT ###
	text = tk.Label(popup, text=msg, font=reg_font)
	text.pack(side="top")
	### BUTTON ###
	b1 = tk.Button(popup, text=msg2, font=reg_font, command=popup.destroy)
	b1.config(height=5, width=14)
	b1.pack()

	popup.mainloop()



#function calling
board = board()
FPS = 60
#pygame stuff
pygame.init()

square_size = 100 #pixels
radius = int(square_size/2 - 5)

width = col_count * square_size
height = (row_count + 1) * square_size
size = (width, height)
font = pygame.font.SysFont("monospace", 35)
font2 = pygame.font.SysFont("monospace", 15)

game_screen = pygame.display.set_mode(size)
pygame.display.set_caption("CONNECT FOUR: Human vs AI")
create_board(board)

pygame.display.update()

print("Welcome to Connect 4, click anywhere to start playing against AI.")

### MAIN FUNCTION TO RUN EVERYTHING ###
def main():


    ### VARIABLES ###
    gameover = False
    paused = False
    turn = 0
    
    clock = pygame.time.Clock()
    
    board_flipped(board) #print the flipped board

    while not gameover:
        clock.tick(FPS)
        
        if paused:
            box = pygame.Rect(width/2 - 75, height/2 - 75, 200, 150)
            button_1 = pygame.Rect(325, 325, 100, 25)
            button_2 = pygame.Rect(325, 375, 100, 25)
            
            pygame.draw.rect(game_screen, black, box)
            pygame.draw.rect(game_screen, white, button_1)
            pygame.draw.rect(game_screen, white, button_2)
            
            text1 = font2.render("Paused", 1, white)
            game_screen.blit(text1, (box.x+75, box.y))
            
            text2 = font2.render("Continue", 1, black)
            game_screen.blit(text2, (button_1.x+10, button_1.y))
            
            text3 = font2.render("Exit", 1, black)
            game_screen.blit(text3, (button_2.x+10, button_2.y))
            
            pos_x, pos_y = pygame.mouse.get_pos()
            
            ### OPTIONS FUNCTION ###
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.collidepoint((pos_x, pos_y)):
                        paused = False
                        pygame.draw.rect(game_screen, black, (275, 275, 200, 150))
                        text4 = font2.render("Click anywhere to place", 1, white)
                        game_screen.blit(text4, (275,350))
                        break
                    if button_2.collidepoint((pos_x, pos_y)):
                        sys.exit()
            
            pygame.display.update()
            
        else:
            text5 = font.render("Press [O] for options", 1, white)
            game_screen.blit(text5, (50,50))

        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                gameover = True
                
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(game_screen, black, (0, 0, width, square_size))
    
                pos_x = event.pos[0]
                
                if turn == 0:
                    pygame.draw.circle(game_screen, maroon, (pos_x, int(square_size / 2)), radius)
                elif turn == 1:
                    pygame.draw.circle(game_screen, violet, (pos_x, int(square_size / 2)), radius)
                    text6 = font.render("Click anywhere to continue", 1, white)
                    game_screen.blit(text6, (50,50))
                    
            pygame.display.update()
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(game_screen, black, (0, 0, width, square_size))
                
                #player 1 play
                if turn == 0:
                    pos_x = event.pos[0] #x position of the mouse
                    col = int(math.floor(pos_x/square_size))
                
                    if check_valid_location(board, col):
                        row = get_next_row(col)
                        drop_pieces(board, row, col, 1)
                
                        if win_move(board, 1):
                            print("Player 1 wins")
                            win = "player1"
                            add_winners(win)
                            animate_win()
                            gameover = True
                            break
                
                        elif draw_check():
                            print("Draw!")
                            win = "draw"
                            add_winners(win)
                            animate_draw()
                            gameover = True
                        
                        
                        board_flipped(board)
                        create_board(board)
                        
                        turn += 1
                        turn = turn % 2
        
                    #computer play
                else:
                    pos_x = event.pos[0]
                    col = rd.randint(0, col_count - 1) #random
        
                    if check_valid_location(board, col):
                        row = get_next_row(col)
                        drop_pieces(board, row, col, 2)
                
                        if win_move(board, 2):
                            print("Computer wins")
                            win = "computer"
                            add_winners(win)
                            animate_loss()
                            gameover = True
                            
                
                        elif draw_check():
                            print("Draw!")
                            win = "draw"
                            add_winners(win)
                            animate_draw()
                            gameover = True
                        
          
                        board_flipped(board)
                        create_board(board)
                        
                        turn += 1 #add turn
                        turn = turn % 2 #even/odd turns
                          
            keys_pressed = pygame.key.get_pressed()       
            if keys_pressed[pygame.K_o]: #options
                paused = True
            
        if gameover:
            pygame.time.wait(5000)
            break
    
    print("Game over! Re-run game to play again.")



if __name__ == "__main__":
    main()