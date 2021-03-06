from sense_emu import SenseHat
from time import sleep

sense = SenseHat()
player_one = True  # Flag to keep track of whose turn it is.

'''
TODO
Problems to solve - no particular order
1 - //Move between "cells"
2 - //Select a cell (not an existing cells)
3 - //Indicate which is X and which is O
4 - //swap between players
4a - //disallow selecting cells already selected.
5 - //Detect "win"
6 - //Detect "loss" when drawn.
7 - //Reset the game
8 - //Move in multiple directions
'''

def draw_hash():
    """
    Draws the # on the Raspberry Pi Sense Hat in white pixels,
    leaving the others black.
    The # is the 'board' for naughts and crosses.
    Parameters:
    None
    E.g. id (int): An int for the 'cell' of the naughts and crosses board
    Returns:
    None
    E.g. student_name: a string with the firstname + ' ' + secondname
    """
    
    # sets black and white
    b = [0,0,0]            # black
    w = [255,255,255]      # white
    
    # grid of 64 leds, black or white, to show the # board.
    grid = [
    b,b,w,b,b,w,b,b,    
    b,b,w,b,b,w,b,b,
    w,w,w,w,w,w,w,w,
    b,b,w,b,b,w,b,b,    
    b,b,w,b,b,w,b,b,
    w,w,w,w,w,w,w,w,
    b,b,w,b,b,w,b,b,    
    b,b,w,b,b,w,b,b
    ]
    
    sense.set_pixels(grid) # draws the grid on the sense hat leds
    
def highlight_cell(id):
    """
    On each 'refresh' of the sense hat led matrix, redraws the game screen.
    Highlights the cell (green) that the user is scrolling through using the sense hat joystick.
    If player 1 has selected a cell, highlight that cell red
    If player 2 has selected a cell, highlight that cell blue
    Redraws the grid as white #.
    
    All other cells are left as black.
    Parameters:
    id (int): The value of the cell that the user is currently highlighting.
    Returns:
    None
    """
    g = [0,255,0]        # green is the highlight colour
    b = [0,0,0]          # black is the colour when cells are not highlighted or selected
    w = [255,255,255]    # White is for the grid #
    r = [255,0,0]        # Player 1's colour
    bl = [0,0,255]       # Player 2's colour
    
    grid = [
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0
        ]
    
    #These are the indexes of the LEDs in grid that need to be white for the hash
    hash = [2,5,10,13,16,17,18,19,20,21,22,23,26,29,34,37,40,41,42,43,44,45,46,47,50,53,58,61]
    
    starting_pixels = [0,3,6,24,27,30,48,51,54] # TODO: what does this do?
    
    '''
    This loop iterates over the game_grid.
    If the value is 1, set the cell as blue
    If the value is 2, set the cell as red
    Uses the starting pixel to set the four pixels as the intended colour
    '''
    for index in range (0,9):
        starting_pixel = starting_pixels[index]
        if game_grid[index] == 1:
            colour = bl
        elif game_grid[index] == 2:
            colour = r
        else:
            colour = 0
        grid[starting_pixel] = colour
        grid[starting_pixel+1] = colour
        grid[starting_pixel+8] = colour
        grid[starting_pixel+9] = colour 
        
    
    # This sets the cell the user is highlighting to be green
    starting_pixel = starting_pixels[id]
    
    grid[starting_pixel] = g
    #grid[starting_pixel+1] = g
    #grid[starting_pixel+8] = g
    grid[starting_pixel+9] = g
    
    
    # Draws the white # game board
    # and replaces any remaining 0's in grid to be black
    # This for loop is to be the last code run in this function.
    # because it captures any remaining 0's in grid and makes it black.
    for index in range (0,64):
        if index in hash:
            grid[index] = w
        if grid[index] == 0:
            grid[index] = b

    
    sense.set_pixels(grid)

def initialise_game_grid():
    """Creates the game grid list to represent the cells
       that players have selected or not.
    Parameters:
    None
    Returns:
    None
   """
    global game_grid
    # 0 = not selected
    # 1 = O selected
    # 2 = X selected
    
    game_grid = [0,0,0,0,0,0,0,0,0]
    
def isWinner(id):
    """Checks all possible combination of win scenarios for a particular playerid
    Parameters:
        id (int): Players Id to check for a row/col/line of 3.
    Returns:
        True if there is a line of 3.
        False if there is no line of 3.
   """
    global game_grid
    if game_grid[0] == id and game_grid[1] == id and game_grid[2] == id or game_grid[3] == id and game_grid[4] == id and game_grid[5] == id or game_grid[6] == id and game_grid[7] == id and game_grid[8] == id or game_grid[0] == id and game_grid[3] == id and game_grid[6] == id or game_grid[1] == id and game_grid[4] == id and game_grid[7] == id or game_grid[2] == id and game_grid[5] == id and game_grid[8] == id or game_grid[0] == id and game_grid[4] == id and game_grid[8] == id or game_grid[2] == id and game_grid[4] == id and game_grid[6] == id:
        # Someone won
        print("Player {} won the game!".format(id))
        return True
    return False

def isDraw():
    """
    Detects if there is a no-win scenario
    Parameters:
        None
    Returns:
        True if there is a draw (all spaces/cells have been filled with no win)
        False if there is no draw - still a possibility of a win scenario
   """
    global game_grid
    for index in range(0,9):
        #scans the game_grid. If any cell is 0, then there are still plays left.
        if game_grid[index] == 0:
            return False
    return True


def flash_feedback(colour):
    for counter in range (0,30):
        sense.clear(colour)
        sleep(0.1)
        sense.clear()
        sleep(0.1)

def select_cells():
    """The user uses the joystick on the sense hat api to scroll through the cells before chosing one
    As the user presses right, it calls the highlight_cell function to change the cell to green.
    If the user chooses a cell, it updates the game grid to indicate which user chose it.
    Parameters:
    None
    Returns:
    None
   """
    global player_one
    '''
    ids of the cells
    0,1,2,
    3,4,5,
    6,7,8
    '''
    
    current_id = -1
    
    while True:
        
        event = sense.stick.wait_for_event()
        if event.action == "pressed":
            #print("The joystick was {} {}".format(event.action, event.direction))
            # first move
            if event.direction == "right":
                #ignores right command on the right column
                if not(current_id == 2 or current_id == 5 or current_id == 8):
                    current_id = current_id + 1
                
                # Loops the selection from the end back to beginning
                if current_id == 9:
                    current_id = 0
            if event.direction == "left":
                
                # Ignores a left command on the left column
                if not(current_id == 0 or current_id == 3 or current_id == 6):
                    current_id = current_id - 1
            
            if event.direction == "up":
              
                # ignores up command on the top row
                if not(current_id == 0 or current_id == 1 or current_id == 2):
                    current_id = current_id - 3
                
            if event.direction == "down":
                # ignores down command on the bottom row
                if not(current_id == 6 or current_id == 7 or current_id == 8):
                    current_id = current_id + 3
                
            
            if event.direction == "middle":
                # this fixes the bug when the user presses the joystick when the game first starts
                if current_id == -1:
                    current_id = 0
                # store the id of the cell selected
                
                if player_one:
                    # if the player clicks middle, and it's player one, then change that cell to blue.
                    # if it's player 2, then change the cell to red.
                    if game_grid[current_id] == 0:
                        game_grid[current_id] = 1
                        player_one = False
                        if isWinner(1):
                            highlight_cell(current_id)
                            flash_feedback([0,0,255])
                            break
                else:
                    if game_grid[current_id] == 0:
                        game_grid[current_id] = 2
                        player_one = True
                        if isWinner(2):
                            highlight_cell(current_id)
                            flash_feedback([255,0,0])
                            break
                
                print(game_grid)
            if isDraw():
                print("Draw")
                highlight_cell(current_id)
                flash_feedback([0,255,0])
                break
            
            # print current_id
            print(current_id)
            highlight_cell(current_id)
     
while (True):
    initialise_game_grid()
    draw_hash()
    select_cells()
