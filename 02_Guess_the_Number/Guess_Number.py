# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import random
import simplegui
import math

# game initialization:
number_range = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, counter
    counter = math.ceil(math.log(number_range - 0 + 1, 2))
    secret_number = random.randrange(0, number_range)
    print "Game begins! Your guess range should be [0, "+ str(number_range) + ")" 
    print("Input your guess:")

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global number_range
    number_range = 100
    print ""
    new_game()
def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global number_range
    number_range = 1000
    print ""
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global counter
    counter -= 1
    player_guess = float(guess)
    print "Guess was", player_guess
    if (player_guess > secret_number) and (counter):
        print "Lower! Number of remaining guesses is ", counter
    elif (player_guess < secret_number) and (counter):
        print "Higher! Number of remaining guesses is ", counter
    elif (player_guess == secret_number) and (counter >= 0):
        print "Correct"
        print ""
        new_game()
    else:
        print "You lose!"
        print "The number is", secret_number
        print ""
        new_game()
    
# create frame
frame = simplegui.create_frame("Guess the number", 100, 200)

# register event handlers for control elements and start frame
frame.add_button("Number Range [0, 100)", range100, 100)
frame.add_button("Number Range [0, 1000)", range1000, 100)
frame.add_input("Guess the number:", input_guess, 100)
frame.start()

# call new_game 
new_game()

# always remember to check your completed program against the grading rubric
