# Zaid Alnemer

# Stuff we will need:
import pygame as pg
import sys
import random as rand
from time import sleep
import os
import io

# Setting up our paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSET_DIR = os.path.join(BASE_DIR, "assets")
IMAGE_DIR = os.path.join(ASSET_DIR, "images")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")

def image_path(file):
    return os.path.join(IMAGE_DIR, file)

def sound_path(file):
    return os.path.join(SOUND_DIR, file)

# This locates our window to the center of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initializing Pygame
pg.init()

# File in which High Score will be stored
HS_FILE = os.path.join(BASE_DIR, "highscore.txt")

# Background color of game screen
BG_COLOR = (229, 204, 169) # Light Yellowish-Brown

# Color for inactive buttons
BTN_INACTIVE_COLOR = (240, 241, 247) # Light Gray

# Dark color for inactive buttons
BTN_INACTIVE_COLOR_DARK = (40, 41, 47) # Dark Bluish-Grey

# More color constants:
WHITE = (255,255,255)

BLACK = (0,0,0)

RED = (255,0,0)

PINK = (255, 0, 125)

ORANGE = (255, 125, 0)

GREEN = (0,255,0)

YELLOW = (255,255,0)

BLUE = (0,0,255)

GREY = (125,125,125)

PURPLE = (255,0,255)

# Constant that stores the spritesheet we will be using for sprites
SPRITESHEET = image_path("snake-graphics.png")

window_width = 900

window_height = 740

# Setting the window title
pg.display.set_caption('Snake Game')

# Creating window object
gameDisplay = pg.display.set_mode((window_width, window_height))

# Storing window icon
icon = pg.image.load(image_path("Logo.ico"))

# Setting window icon
pg.display.set_icon(icon)

# Creating frames per second object
clock = pg.time.Clock()

# Preseting size for all blocks and sprites in pixels
block_size = 32

# Default direction of snake when game first starts
direction = 'right'

# Setting font presets and storing them in variables:
font = pg.font.SysFont(None, 25)

score_font = pg.font.SysFont('comicsansms', 25)

points_font = pg.font.SysFont('comicsansms', 45)

countdown_font = pg.font.SysFont('comicsansms', 65)

points_font_2 = pg.font.SysFont('comicsansms', 30)

title_font = pg.font.SysFont('georgia', 100)

menu_font = pg.font.SysFont('bookman', 60)

smaller_menu_font = pg.font.SysFont('bookman', 45)

# Storing sound files -half of these may not even be used:
eating_apple = pg.mixer.Sound(sound_path("eating_apple.wav"))
button_press = pg.mixer.Sound(sound_path("button_click.wav"))
background_music = pg.mixer.music.load(sound_path("elevator_music.mp3"))
startMenu_music = pg.mixer.music.load(sound_path("start_menu.mp3"))
death_music = pg.mixer.Sound(sound_path("gameover.wav"))
endScreen_music = pg.mixer.music.load(sound_path("end_screen.mp3"))
tick = pg.mixer.Sound(sound_path("countdown_sound.wav"))
tock = pg.mixer.Sound(sound_path("GO_sound.wav"))


# Preset variables for button sizes
button_width = 650

button_height = 90

control_screen_button_width = 350

control_screen_button_height = 60

# Preset Variables for center locations on the screen:
window_center_x = window_width/2

window_center_y = window_height/2

center_x = window_width/2 - button_width/2

center_y = window_height/2 - button_height/2

class Spritesheet:
    'utility class for loading and parsing spritesheets'

    # filename will be the Sprtiesheet they want to pull out images from
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename)

    # Grab an image out of a larger spritesheet using its location and size
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (block_size, block_size))
        return image

# This method will get the value in the high score file and return it
def getHighScore():
    # getting the value stored in the high score file
    try:
        with open(HS_FILE, 'r') as file:
            high_score = int(file.read())
    except:
        high_score = 0

    # Returning that value as the game high score
    return high_score

# This method will save the new high score to the high score file (if there is one)
# It will also output the high score or it will let the user know if they got a new high score
def save_score(high_score, game_score):

    # If the score you just achieved is higher than the high score
    if high_score < game_score:
        with open(HS_FILE, 'w') as file:
            # Replace high score with current score
            file.write(str(game_score))

    # If the high score and the current score are equal
    if high_score == game_score:
        # Letting the user know he has achieved a new highscore
        message_to_screen('NEW HIGHSCORE!', PINK, 40, points_font_2)

    # Telling the user the high score
    else: message_to_screen('High Score: ' + str(high_score), PINK, 40, points_font_2)

# This decides the functionality of a button when clicked on depending on the keyword passed through the 'actionn' parameter 
def buttonActions(action):
    click = pg.mouse.get_pressed()
    
    if click[0] == 1:
        pg.mixer.Sound.play(button_press)
        sleep(0.8)
        if action == "play":
            gameLoop()

        if action == "instructions":
            instructions_screen()

        if action == "controls":
            controls_screen()

        if action == "quit":
            pg.quit()
            sys.exit()

        if action == "back":
            start_screen()

        else: None
        
    else: None

# This method creates a button using rectangles and text
# For this method you must, in order, pass in:
    # The text you want the button to display
    # The color of the text when the button is being hovered over
    # The color of the text when the button is NOT being hovered over
    # The buttons x-axis location
    # The buttons y-axis location
    # The width of the button
    # The height of the button
    # The color of the button when being hovered over
    # The color of the button when NOT being hovered over
    # The font of the text of the button
    # The keyword which represents the functionality of the button when clicked on
def menuButton(text, aText_color, iText_color, x, y, width, height, aButton_color, iButton_color, fontVar, function=None):
    cursor = pg.mouse.get_pos()

    if x + width > cursor[0] > x and y + height > cursor[1] > y:
        pg.draw.rect(gameDisplay, aButton_color, (x, y, width, height))
        text_to_button(text, aText_color, x, y, width, height, fontVar)
        buttonActions(action=function)
    else:
        pg.draw.rect(gameDisplay, iButton_color, (x, y, width, height))
        text_to_button(text, iText_color, x, y, width, height, fontVar)

def instructions_screen():
    while True:

        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
    
        # Coloring screen white
        gameDisplay.fill((255, 255, 255))

        # Outputting game instructions in a series of sentences
        message_to_screen('Instructions', BLUE, -320, title_font)
        message_to_screen('', BLUE, -250, title_font)
        message_to_screen('Once in game:', BLACK, -190, points_font)
        message_to_screen('The main objective is to eat as many apples as possible.', BLACK, -130, points_font_2)
        message_to_screen('Eating apples will increase the length and speed of the snake.', BLACK, -60, points_font_2)
        message_to_screen('The longer the snake gets the higher your score.', BLACK, 10, points_font_2)
        message_to_screen('Try not to run into the wall or your tail.', BLACK, 80, points_font_2)
        message_to_screen('Now go out there and play and get a high score!', BLACK, 150, points_font_2)
        
        # Creating a button that will allow you to play the game
        play_button = menuButton('Play', WHITE, GREEN,
                                 center_x + 355, center_y + 270, control_screen_button_width, control_screen_button_height,
                                 GREEN, BTN_INACTIVE_COLOR, smaller_menu_font, 'play')

        # Creating a button that will allow you to go back to the main menu
        back_to_start_screen_button = menuButton('Back to Main Menu', WHITE, RED,
                                                 center_x - 65, center_y + 270, control_screen_button_width, control_screen_button_height,
                                                 RED, BTN_INACTIVE_COLOR, smaller_menu_font, 'back')

        # Updating Display
        pg.display.update()

        # Setting frames per second to 60
        clock.tick(60)

def controls_screen():
    while True:

        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
    
        # Coloring screen white
        gameDisplay.fill(WHITE)

        # Outputting the controls of the game in a series of sentences
        message_to_screen('Controls', YELLOW, -320, title_font)
        message_to_screen('', YELLOW, -250, title_font)
        message_to_screen('Use the arrow keys to move the snake', BLACK, -190, points_font)
        message_to_screen('Press P to pause/resume', BLACK, -120, points_font)
        message_to_screen('Press M to go back to main menu', BLACK, -50, points_font)
        message_to_screen('Press C to play/play again', BLACK, 20, points_font)
        message_to_screen('Press Q or esc to quit', BLACK, 90, points_font)
        
        # Creating a button that will allow you to play the game
        play_button = menuButton('Play', WHITE, GREEN,
                                 center_x + 355, center_y + 250, control_screen_button_width, control_screen_button_height,
                                 GREEN, BTN_INACTIVE_COLOR, smaller_menu_font, 'play')

        # Creating a button that will allow you to go back to the main menu
        back_to_start_screen_button = menuButton('Back to Main Menu', WHITE, RED,
                                                 center_x - 65, center_y + 250, control_screen_button_width, control_screen_button_height,
                                                 RED, BTN_INACTIVE_COLOR, smaller_menu_font, 'back')

        # Updating Display
        pg.display.update()

        # Setting frames per second to 60
        clock.tick(60)

def start_screen():
    # Loading a logo image
    Logo = pg.image.load(image_path("Icon.png"))

    # Changing the size of the logo image in pixels
    header = pg.transform.scale(Logo, (180, 180))
    
    intro = True
    
    while intro:

        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
    
        # Coloring screen white
        gameDisplay.fill(WHITE)

        # Outputting a warm welcome and introduction to my game
        message_to_screen('Welcome to', BLACK, -320, title_font, -100)
        message_to_screen('Snake Game!', BLACK, -230, title_font, -100)
        message_to_screen('________________', BLACK, -220, title_font)

        # Creating a text object that will tell the user im the author of this program
        author = score_font.render('Made By: Zaid Alnemer', True, BLACK)

        # Creating a button that will allow you to play the game
        play_button = menuButton('Play', WHITE, GREEN,
                                 center_x, center_y - (button_height*0.8), button_width, button_height,
                                 GREEN, BTN_INACTIVE_COLOR, menu_font, 'play')

        # Creating a button that will redirect you the instructions screen
        instruction_button = menuButton('Instructions', WHITE, BLUE,
                                        center_x, center_y + (button_height*0.5), button_width, button_height,
                                        BLUE, BTN_INACTIVE_COLOR, menu_font, 'instructions')

        # Creating a button that will redirect you the controls screen
        controls_button = menuButton('Controls', WHITE, YELLOW,
                                     center_x, center_y + (button_height*1.75), button_width, button_height,
                                     YELLOW, BTN_INACTIVE_COLOR, menu_font, 'controls')

        # Creating a button that will allow to quit the program
        quit_button = menuButton('Quit', WHITE, RED,
                                 center_x, center_y + ((button_height*1.5)*2), button_width, button_height,
                                 RED, BTN_INACTIVE_COLOR, menu_font, 'quit')
        
        # Displaying the author text object
        gameDisplay.blit(author, [0, window_height - 35])

        # Displaying logo image
        gameDisplay.blit(header, [660,5])

        # Updating Display
        pg.display.update()

        # Setting frames per second to 60
        clock.tick(60)

# This function will pause the game screen and also provide some relevent output indicating the screen is paused
def pause():
    # Playing sound effect for pausing
    pg.mixer.Sound.play(button_press)
    
    paused = True

    # Outputting informational text about the program being paused
    text = message_to_screen('Paused', BLACK, -30, countdown_font, 0)
    text_1 = message_to_screen('Press P again to continue', BLACK, 35, points_font_2, 0)

    # Updating display
    pg.display.update()

    while paused:
        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    paused = False

                elif event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                    
        # Setting the frames per second to 1 so that tha game actaully freezes
        clock.tick(1)

    # If the game becomes unpaused this will countdown to give the user time to get ready
    pause_countdown()

# This function draws the snake
def snake(size, snakelist, head, body, tail, corner):
    if direction == 'right':
        snake_head = pg.transform.rotate(head, 270)
    if direction == 'left':
        snake_head = pg.transform.rotate(head, 90)
    if direction == 'up':
        snake_head = head
    if direction == 'down':
        snake_head = pg.transform.rotate(head, 180)
    
    gameDisplay.blit(snake_head, (snakelist[-1][0], snakelist[-1][1]))

    if len(snakelist) < 2:
        return
    
    for i in range(1, len(snakelist) - 1):
        prev = snakelist[i - 1]
        curr = snakelist[i]
        next_seg = snakelist[i + 1]

        prev_dx = curr[0] - prev[0]
        prev_dy = curr[1] - prev[1]
        next_dx = next_seg[0] - curr[0]
        next_dy = next_seg[1] - curr[1]

        # Straight vertical body
        if prev_dx == 0 and next_dx == 0:
            snake_body = body

        # Straight horizontal body
        elif prev_dy == 0 and next_dy == 0:
            snake_body = pg.transform.rotate(body, 270)

        # Corner body pieces
        else:
            connections = set()

            # from prev → curr
            if prev[0] < curr[0]:
                connections.add('left')
            elif prev[0] > curr[0]:
                connections.add('right')
            elif prev[1] < curr[1]:
                connections.add('up')
            elif prev[1] > curr[1]:
                connections.add('down')

            # from curr → next
            if next_seg[0] < curr[0]:
                connections.add('left')
            elif next_seg[0] > curr[0]:
                connections.add('right')
            elif next_seg[1] < curr[1]:
                connections.add('up')
            elif next_seg[1] > curr[1]:
                connections.add('down')

            if connections == {'left', 'down'}:
                snake_body = corner

            elif connections == {'right', 'down'}:
                snake_body = pg.transform.rotate(corner, 90)

            elif connections == {'right', 'up'}:
                snake_body = pg.transform.rotate(corner, 180)

            elif connections == {'left', 'up'}:
                snake_body = pg.transform.rotate(corner, 270)

        gameDisplay.blit(snake_body, (curr[0], curr[1]))

    tail_seg = snakelist[0]
    next_seg = snakelist[1]

    dx = next_seg[0] - tail_seg[0]
    dy = next_seg[1] - tail_seg[1]

    if dx > 0:
        snake_tail = pg.transform.rotate(tail, 270)
    elif dx < 0:
        snake_tail = pg.transform.rotate(tail, 90)
    elif dy > 0:
        snake_tail = pg.transform.rotate(tail, 180)
    else:
        snake_tail = tail

    gameDisplay.blit(snake_tail, (tail_seg[0], tail_seg[1]))

# This function will take the value in the 'score' parameter and draw it out to the bottom-left corner of the screen during the game screen
def score(score):
    text = score_font.render('Score: ' + str(score), True, PURPLE)
    gameDisplay.blit(text, [0+20, window_height-56])

# This function renders the font passed through with the color passed through its parameters
# It then returns that and returns it's rectangular area
def text_objects(text, color, fontVar):
    textSurface = fontVar.render(text, True, color)

    return textSurface, textSurface.get_rect()

# This function draws text to a button
    # The 'msg' parameter is the actual message/text you want to draw to the button
    # The 'color' parameter is the color you want that text to nbe displayed in
    # The 'buttonx' parameter is the x co-ordinate location of the button you want to draw the text to
    # The 'buttony' parameter is the y co-ordinate location of the button you want to draw the text to
    # The 'buttonw' parameter is the width of the button you want to draw the text to
    # The 'buttonh' parameter is the height of the button you want to draw the text to
    # The 'fontVar' is the font you want to use for the text and it has a default value
def text_to_button(msg, color, buttonx, buttony, buttonw, buttonh, fontVar=score_font):
    textSurf, textRect = text_objects(msg, color, fontVar)
    textRect.center = ((buttonx + (buttonw/ 2)), buttony + (buttonh / 2))
    gameDisplay.blit(textSurf, textRect)
    
# This is a basic function that allows you to draw text to the screen
    # The 'msg' parameter is the actual message/text you want to draw to the screen
    # The 'color' parameter is the color you want that text to nbe displayed in
    # The 'y_displace' parameter is the ammount of pixels you want the text to be displaced from the center of the screen on the y axis
        # It has a default value of 0 meaning that the text will automatically be placed at the center if you choose not to enter a value
    # The 'x_displace' parameter is the ammount of pixels you want the text to be displaced from the center of the screen on the x axis
        # It has a default value of 0 meaning that the text will automatically be placed at the center if you choose not to enter a value
    # The 'fontVar' is the font you want to use for the text and it also has a default value
def message_to_screen(msg, color, y_displace=0, fontVar=score_font, x_displace=0):
    textSurf, textRect = text_objects(msg, color, fontVar)
    textRect.center = (window_width / 2) + x_displace, (window_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)

# This method provides a countdown just before the game screen loads
def countdown():
    # Changing color of screen to the Background color specified above to erase all text on the screen
    gameDisplay.fill(BG_COLOR)

    # Outputting the number '3' to the screen
    text = message_to_screen('3', BLACK, 0, countdown_font, 0)

    # Updating Display
    pg.display.update()

    # Playing sound effect
    pg.mixer.Sound.play(tick)

    # Pausing screen for one second
    sleep(1)

    # Changing color of screen to the Background color specified above to erase all text on the screen
    gameDisplay.fill(BG_COLOR)

    # Outputting the number '2' to the screen
    text = message_to_screen('2', BLACK, 0, countdown_font, 0)

    # Updating Display
    pg.display.update()

    # Playing sound effect
    pg.mixer.Sound.play(tick)

    # Pausing screen for one second
    sleep(1)

    # Changing color of screen to the Background color specified above to erase all text on the screen
    gameDisplay.fill(BG_COLOR)

    # Outputting the number '1' to the screen
    text = message_to_screen('1', BLACK, 0, countdown_font, 0)

    # Updating Display
    pg.display.update()

    # Playing sound effect
    pg.mixer.Sound.play(tick)

    # Pausing screen for one second
    sleep(1)

    # Changing color of screen to the Background color specified above to erase all text on the screen
    gameDisplay.fill(BG_COLOR)

    # Outputting 'GO' to the screen to let the user know the game has begun
    text = message_to_screen('GO!', BLACK, 0, countdown_font, 0)

    # Updating Display
    pg.display.update()

    # Playing sound effect
    pg.mixer.Sound.play(tock)

    # Pausing screen for half a second
    sleep(0.5)

# This method provides a countdown just after the user unpauses the game
def pause_countdown():
    # Changing color of area specified to the Background color specified above to erase all text in that area
    gameDisplay.fill(BG_COLOR, rect=[window_center_x - 180, window_center_y - 60, 355, 117])

    # Outputting the number '3' to the screen
    text = message_to_screen('3', BLACK, 0, countdown_font, 0)

    # Updating Display
    pg.display.update()

    # Playing sound effect
    pg.mixer.Sound.play(tick)

    # Pausing screen for one second
    sleep(1)
    
    # Changing color of area specified to the Background color specified above to erase all text in that area
    gameDisplay.fill(BG_COLOR, rect=[window_center_x - 180, window_center_y - 60, 355, 117])

    # Outputting the number '2' to the screen
    text = message_to_screen('2', BLACK, 0, countdown_font, 0)

    # Updating Display
    pg.display.update()

    # Playing sound effect
    pg.mixer.Sound.play(tick)

    # Pausing screen for one second
    sleep(1)

    # Changing color of area specified to the Background color specified above to erase all text in that area
    gameDisplay.fill(BG_COLOR, rect=[window_center_x - 180, window_center_y - 60, 355, 117])

    # Outputting the number '1' to the screen
    text = message_to_screen('1', BLACK, 0, countdown_font, 0)

    # Updating Display
    pg.display.update()

    # Playing sound effect
    pg.mixer.Sound.play(tick)

    # Pausing screen for one second
    sleep(1)

    # Changing color of area specified to the Background color specified above to erase all text in that area
    gameDisplay.fill(BG_COLOR, rect=[window_center_x - 180, window_center_y - 60, 355, 117])

    # Outputting 'Resume...' to the screen to get the user ready because the game has been unpaused
    text = message_to_screen('Resume...', BLACK, 0, countdown_font, 0)

    # Updating Display
    pg.display.update()

    # Playing sound effect
    pg.mixer.Sound.play(tock)

    # Pausing screen for half a second
    sleep(0.5)

# Game over screen
def gameOver_screen(cause, score):
    # Getting current game score
    game_score = score

    # Coloring the screen black
    gameDisplay.fill(BLACK)

    # Reseting direction variable for next play
    global direction
    direction = 'right'

    # Getting highscore
    high_score = getHighScore()

    # Saving Highscore
    save_score(high_score, game_score)

    # Outputting 'Game Over' to screen
    message_to_screen('Game Over', BLUE, -300, title_font)

    # Outputting information about the user has lost
    if cause == '1':
        message_to_screen('You ran into yourself!', RED, -200, countdown_font)
    else:
        message_to_screen('You fell of the map!', RED, -200, countdown_font)

    # Outputting the score that the user has lost at
    message_to_screen('Your score was: ' + str(game_score), PURPLE, 0, points_font_2)

    # Event Handling
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_c:
                gameLoop()
            elif event.key == pg.K_m:
                start_screen()
            elif event.key == pg.K_q:
                pg.quit()
                sys.exit()
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
        elif event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Creating a button that will allow you to play the game
    play_again_button = menuButton('Play Again', WHITE, GREEN,
                                   center_x + 355, center_y + 245, control_screen_button_width, control_screen_button_height,
                                   GREEN, BTN_INACTIVE_COLOR_DARK, smaller_menu_font, 'play')

    # Creating a button that will allow you to go back to the main menu
    back_to_start_screen_button = menuButton('Back to Main Menu', WHITE, ORANGE,
                                             center_x - 65, center_y + 245, control_screen_button_width, control_screen_button_height,
                                             ORANGE, BTN_INACTIVE_COLOR_DARK, smaller_menu_font, 'back')

    # Creating a button that will allow to quit the program
    back_to_start_screen_button = menuButton('Quit', WHITE, RED,
                                             window_center_x - control_screen_button_width / 2, center_y + 330, control_screen_button_width, control_screen_button_height,
                                             RED, BTN_INACTIVE_COLOR_DARK, smaller_menu_font, 'quit')

    # Updating Display
    pg.display.update()

# Actual game -Game Screen
def gameLoop():
    # Calling the 'countdown()' function to execute
    countdown()

    # Creating the users score
    actualScore = 0

    # Setting some defaults
    global direction
    direction = 'right'
    next_direction = 'right'
    
    # Loading all sprites from spritesheet
    spritesheet = Spritesheet(SPRITESHEET)

    default_snake_head = spritesheet.get_image(192, 0, 64, 64)
    default_snake_body = spritesheet.get_image(128, 64, 64, 64)
    default_snake_tail = spritesheet.get_image(192, 128, 64, 64)

    snake_corner = spritesheet.get_image(128, 0, 64, 64)

    default_snake_head.set_colorkey(BLACK)
    default_snake_body.set_colorkey(BLACK)
    default_snake_tail.set_colorkey(BLACK)
    snake_corner.set_colorkey(BLACK)

    apple = spritesheet.get_image(0, 192, 64, 64)
    apple.set_colorkey(BLACK)
    
    FPS = 12

    # Setting some more defaults
    gameExit = False
    gameOver_1 = False
    gameOver_2 = False

    # Generating the snake in a random location on the right side of the screen
    head_x = round(rand.randrange(0, window_width/2 - block_size)/float(block_size))*float(block_size)
    head_y = round(rand.randrange(0, window_height - block_size)/float(block_size))*float(block_size)

    # Moving snake right
    head_x_change = block_size
    head_y_change = 0

    # Generating random x-axis location for the apple
    randAppleX = round(rand.randrange(0, window_width - block_size)/float(block_size))*float(block_size)

    # Generating random y-axis location for the apple
    randAppleY = round(rand.randrange(0, window_height - block_size)/float(block_size))*float(block_size)

    # Creating the list of snake segments
    snakeList = []

    # Setting the length of the snake
    snakeLength = 3
    
    while not gameExit:

        while gameOver_1 == True:
            gameOver_screen('1', actualScore)

        while gameOver_2 == True:
            gameOver_screen('2', actualScore)
        
        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameExit = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    pause()
                elif event.key == pg.K_RIGHT and direction != 'left':
                    next_direction = 'right'
                elif event.key == pg.K_LEFT and direction != 'right':
                    next_direction = 'left'
                elif event.key == pg.K_UP and direction != 'down':
                    next_direction = 'up'
                elif event.key == pg.K_DOWN and direction != 'up':
                    next_direction = 'down'
                elif event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

        # Logic Handling:

        # Apply the next valid direction once per frame
        direction = next_direction

        if direction == 'right':
            head_x_change = block_size
            head_y_change = 0
        elif direction == 'left':
            head_x_change = -block_size
            head_y_change = 0
        elif direction == 'up':
            head_x_change = 0
            head_y_change = -block_size
        elif direction == 'down':
            head_x_change = 0
            head_y_change = block_size

        # Moving the snake
        head_x += head_x_change
        head_y += head_y_change

        # If the snake reaches the limits of the window
        if head_x + block_size > window_width or head_x < 0 or head_y + block_size > window_height or head_y < 0:
            gameOver_2 = True

        # Coloring the screen to the background color specified above
        gameDisplay.fill(BG_COLOR)

        # Outputting the apple to the screen
        gameDisplay.blit(apple, (randAppleX, randAppleY))
        
        # Creating the snake segments
        snakeHead = []
        snakeHead.append(head_x)
        snakeHead.append(head_y)
        snakeList.append(snakeHead)

        # THis will stop the snake from growing uncontrollably
        if len(snakeList) > snakeLength:
            del snakeList[0]

        # If the snake touches itself it dies
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver_1 = True
        
        # Drawing the snake object
        snake(block_size, snakeList, default_snake_head, default_snake_body, default_snake_tail, snake_corner)

        # Displaying score
        score(actualScore)
        
        # Updating Display
        pg.display.update()

        # If location of snakes head is equal to location of apple (If snake eats apple)
        if head_x == randAppleX and head_y == randAppleY:
            # Play sound effect
            pg.mixer.Sound.play(eating_apple)

            # Generating new locating for apple
            randAppleX = round(rand.randrange(0, window_width - block_size)/float(block_size))*float(block_size)
            randAppleY = round(rand.randrange(0, window_height - block_size)/float(block_size))*float(block_size)

            # Increasing snake length
            snakeLength += 2

            # Setting score
            actualScore += 10

            # Increasing speed of snake
            FPS += 0.6

        # Setting frames per second to the value in the variable FPS
        clock.tick(FPS)

    # Exit game window
    pg.quit()

    # Exit python shell
    sys.exit()

# Calling main menu
start_screen()
