#imports
import pygame as game
import sys
import time
from pygame.locals import *

# Global Var
#gamepiece being placed
piece = 'X'

# Winner
winner = ''

#X and O score
xCount = 0
oCount = 0

#Draw
isDraw = False

#game window width
WIDTH = 400

#game window height
HEIGHT = 400

#set colours I will use
WHITE = (255,255,255)
RED = (200,0,0)
brightRED = (255,0,0)
GREEN = (50,205,20)
#Game board dividers
divCOLOUR = (0,0,0)

#Creating 3x3 game board
board = [[("Empty") for x in range(3)] for y in range(3)] 

# initialize game window
game.init()

#set fps
FPS = 30

#clock 
CLOCK = game.time.Clock()

#Create game window
gameWindow = game.display.set_mode((WIDTH,HEIGHT+100),0,32)

#Application Name
game.display.set_caption("Morgan Ward's Tic Tac Toe")

#Grabbing images 
openingWindow = game.image.load("frontPage.png")
xGraphic = game.image.load("X.png")
oGraphic = game.image.load("O.png")

#Resizing
openingWindow = game.transform.scale(openingWindow, (WIDTH,HEIGHT+100))
xGraphic = game.transform.scale(xGraphic, (70,70))
oGraphic = game.transform.scale(oGraphic, (70,70))

#Set default Font
defFont = game.font.Font(None, 30)
scoreFont = game.font.Font(None, 50)

#Function to check if game is over, checks win conditions or draw condition
#Returns true if game is over and increases winning players # games won, returns false otherwise
def isOver():
    global board, winner, isDraw, xCount, oCount
   
    #Checking if all 3 columns in any given row match and are not empty, this means a player has won
    #If a winner, draw a line through the tiles where the game has been won, increase winning players score and return true
    for row in range(3): 
        if((board[row][0]) == board[row][1] == board[row][2]) and (board[row][0] != 'Empty'):
            winner = board[row][0]
            if winner == 'X':
                lineColour = GREEN
                xCount +=1
            else:
                lineColour = RED
                oCount += 1
            game.draw.line(gameWindow, lineColour, (0, (row + 1)*HEIGHT / 3 - HEIGHT / 6), 
                         (WIDTH, (row + 1)*HEIGHT / 3 - HEIGHT / 6 ), 7) 
            gameStatus()
            return True
    
    #Checking if all 3 rows in any given row match and are not empty, this means a player has won
    #If a winner, draw a line through the tiles where the game has been won, increase winning players score and return true
    for col in range(3): 
        if((board[0][col]) == board[1][col] == board[2][col]) and (board[0][col] != 'Empty'):
            winner = board[0][col]
            if winner == 'X':
                lineColour = GREEN
                xCount +=1
            else:
                lineColour = RED
                oCount += 1
            game.draw.line(gameWindow, lineColour, ((col + 1)* WIDTH / 3 - WIDTH / 6, 0),
                          ((col + 1)* WIDTH / 3 - WIDTH / 6, HEIGHT), 7) 
            gameStatus()
            return True
    
    #Checking the diagonals for a win
    if ((board[0][0] == board[1][1] == board[2][2]) and (board[0][0] != 'Empty')):
        winner = board[0][0]
        if winner == 'X':
            lineColour = GREEN
            xCount +=1
        else:
            lineColour = RED
            oCount += 1            
        game.draw.line(gameWindow, lineColour, (0,0),(400,400), 7)
        gameStatus()
        return True

    if ((board[0][2] == board[1][1] == board[2][0]) and (board[0][2] != 'Empty')):
        winner = board[0][2]
        if winner == 'X':
            lineColour = GREEN
            xCount += 1
        else:
            lineColour = RED
            oCount += 1
        game.draw.line(gameWindow, lineColour, (400,0),(0,400), 7)
        gameStatus()
        return True
    
    #If there hasn't been a win determined yet, check for a draw
    #See if every space has a game piece, if there's a piece, add to the counter
    drawCounter = 0
    for row in range(3):
        for col in range(3):
            if board[row][col] != 'Empty':
                drawCounter += 1   
    #if there are 9 pieces placed and no win, then there is a draw
    if drawCounter == 9:
        isDraw = True
        gameStatus()
        return True

    gameStatus()
    return False

#This function draws what appears to be a filled rectangle with a coloured border
#In reality it is two rectangles on top of eachother, with one rectangle being bigger to create the "border"
def draw_rect(surface, fill_colour, outline_colour, rect, border=1):
        surface.fill(outline_colour, rect)
        surface.fill(fill_colour, rect.inflate(-border*2, -border*2))

#This function restarts the game, it clears the board, and resets global variables
def gameRes():
    global board, winner, piece, isDraw 
    XO = 'X'
    isDraw = False
    winner = ''
    board = [[("Empty") for x in range(3)] for y in range(3)] 
    gameBoardCreate()

#This function updates the user on the current game state, who's turn it is and if game is over, all displayed on bottom of screem
def gameStatus(): 
    global isDraw

    if winner == '':
        message = piece + "'s Turn"
    else:
        message = winner + " Won !"

    if isDraw:
        message = "Game Draw !"

    text = defFont.render(message, 1, WHITE)

    gameWindow.fill((0,0,0), (0,400,500,100))
    
    textRect = text.get_rect(center = (WIDTH/2, 500 - 50))
    gameWindow.blit(text, textRect)
    scorePrint()

    game.display.update()

#This function is called by gameStatus function, it prints out how many games each player has won
def scorePrint():
    global xCount, oCount

    xText = defFont.render("X has won ", 1, GREEN)
    oText = defFont.render("O has won ", 1, RED)
    
    xSText = scoreFont.render(str(xCount), 1, GREEN)
    oSText = scoreFont.render(str(oCount), 1, RED)

    gText1 = defFont.render("games", 1, GREEN)
    gText2 = defFont.render("games", 1, RED)

    xTextRect = xText.get_rect(center = (60, 500 - 75))
    oTextRect = oText.get_rect(center = (WIDTH - 65, 500 - 75))

    xSTextRect = xSText.get_rect(center = (60, 500 - 50))
    oSTextRect = oSText.get_rect(center = (WIDTH - 65, 500 - 50))

    gTextRect1 = gText1.get_rect(center = (60, 500 - 25))
    gTextRect2 = gText2.get_rect(center = (WIDTH - 65, 500 - 25))

    gameWindow.blit(xText, xTextRect)
    gameWindow.blit(oText, oTextRect)

    gameWindow.blit(xSText, xSTextRect)
    gameWindow.blit(oSText, oSTextRect)

    gameWindow.blit(gText1, gTextRect1)
    gameWindow.blit(gText2, gTextRect2)


#This function actually updates the board to show which piece has been placed where
#It gets passed in which tile is getting a piece placed on it, and then updates the game board by placing the proper piece on that tile
#It "places" the piece by dropping the piece image over top of the game board
#It offsets the image on the tile so that the piece looks centered in the tile
def drawPiece(row,col):
    global board, piece

    if col == 0: 
        xoffset = 30
    if col == 1: 
        xoffset = WIDTH/3 + 30
    if col == 2: 
        xoffset = (WIDTH/3)*2 + 30
    if row == 0: 
        yoffset = 30
    if row == 1: 
        yoffset = HEIGHT/3 + 30
    if row == 2: 
        yoffset = (HEIGHT/3)*2 + 30
    if(piece == 'X'):
        gameWindow.blit(xGraphic, (xoffset, yoffset))
        piece = "O"
    elif(piece == "O"): 
        gameWindow.blit(oGraphic, (xoffset, yoffset))
        piece = 'X'
    game.display.update()

#This function draws the actual game board in the application window
def gameBoardCreate():
    #Display front page over game window
    gameWindow.blit(openingWindow, (0,0))
    
    #Update display so front page is seen
    game.display.update()
   
    #pause for 1 second, adds effect of game loading
    time.sleep(1)
   
    #after "load" fill screen with white to build game board on
    gameWindow.fill(WHITE)

    #Add game board dividers
    #Vertical lines
    game.draw.line(gameWindow, divCOLOUR, (WIDTH/3,0), (WIDTH/3, HEIGHT), 5)
    game.draw.line(gameWindow, divCOLOUR, (WIDTH/3*2,0), (WIDTH/3*2, HEIGHT), 5)

    #horizontal lines
    game.draw.line(gameWindow, divCOLOUR, (0,HEIGHT/3), (WIDTH, HEIGHT/3), 5)
    game.draw.line(gameWindow, divCOLOUR, (0,HEIGHT/3*2), (WIDTH, HEIGHT/3*2), 5)

    gameStatus()

#Using the mouse position on a click, this function determines which tile has been clicked in order to place a piece on that tile
def Click():
    #Determining where was clicked
    x,y = game.mouse.get_pos()
   #If the user is clicking below the game board in the score area, do nothing
    if(y>HEIGHT):
        return
    #If user has clicked anywhere along the top row, then set row to 0
    if(y < HEIGHT/3):
        row = 0
    #If user has clicked between rows 0 and 2, set row to 1
    elif(y < (HEIGHT/3)*2):
        row = 1
    #If user has clicked above score area but below row 1, set row to 2
    elif(y < HEIGHT):
        row = 2
    #If user has clicked anywhere else then row is None
    else:
        row = None
   #If user has clicked anywhere along the first column, set column to 0
    if(x < WIDTH/3):
        col = 0
    #If user has clicked between columns 0 and 2, set column to 1
    elif(x < (WIDTH/3)*2):
        col = 1
    #If user has clicked along the last column, set col to 2
    elif(x < WIDTH):
        col = 2
    #If user has clicked anywhere else then column is None
    else:
        col = None
    #Check that the tile user is trying to place piece on is actually empty
    if(board[row][col] == 'Empty'):
        global piece
        #update the board so it knows that there is a piece on the tile
        board[row][col] = piece
        #call draw function to actually place piece on tile
        drawPiece(row,col)

#This function creates the Restart Button that appears when a game has finished
#The button highlights itself if the mouse is hovering over it, and restarts the game when clicked
def resButtonCreate():
    #Creating the message and getting information about the physical sizing of the text
    resMsg = defFont.render("Click Here To Restart", 1, brightRED)
    resRect = resMsg.get_rect(center=(WIDTH/2, HEIGHT/2))
    resWidth = resMsg.get_width()
    resHeight = resMsg.get_height()
    #using size of text, make a box around it that is slightly bigger, so the text doesn't look crowded
    bigRect = game.Rect((WIDTH/2 - resWidth/2 - 5, HEIGHT/2 - resHeight/2 - 5), (resWidth+10, resHeight+10))
    #draw a bordered box around the text
    draw_rect(gameWindow, WHITE, RED, bigRect, 1)

    #this loop constantly monitors mouse position to see if it is inside the bounds of the button, if it is, highlight the button
    while(True):
        for event in game.event.get():
            #if the user wants to close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                game.quit()
                sys.exit()
            #get mouse position
            mouse = game.mouse.get_pos()  
            #if inside bounds of button, invert colours of button and text to appeaer highlighted, and if clicked inside bounds restart the game
            if WIDTH/2+(resWidth+10)/2 > mouse[0] > WIDTH/2-(resWidth+10)/2 and HEIGHT/2 + (resHeight+10)/2 > mouse[1] > HEIGHT/2 - (resHeight+10)/2: 
                draw_rect(gameWindow, brightRED, WHITE, bigRect, 1)
                resMsg = defFont.render("Click Here To Restart", 1, WHITE)
                gameWindow.blit(resMsg, resRect)
                if event.type == MOUSEBUTTONDOWN:
                    playGame()
            #if mouse position not inside bounds of button then leave button and text with original colours
            else:
                draw_rect(gameWindow, WHITE, RED, bigRect, 1)
                resMsg = defFont.render("Click Here To Restart", 1, brightRED)
                gameWindow.blit(resMsg, resRect)
        game.display.update()

#This function actually plays the game, when called resets the game so a clean board appears
def playGame():
    gameRes()
   #while the game hasn't been won or tied, keep game running
    while(not isOver()):
        #monitor for user inputs
        for event in game.event.get():
            #if user wants to end game then close application
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                game.quit()
                sys.exit()
            #if the user clicks, call Click function to determine where they clicked and if they wanted a piece to be played
            elif event.type == MOUSEBUTTONDOWN:
                Click()
        #limits the game to run at the chosen FPS
        CLOCK.tick(FPS)
    #If the while loop is exited, then the game must be over, so the restart button is created
    resButtonCreate()
#This starts the game the very first time
playGame()


