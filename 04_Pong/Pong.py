# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
paddle1_acc = 5

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == RIGHT:
        ball_vel =  [(1/60.0) * random.randrange(120, 240), - (1/60.0) * random.randrange(60, 180)]
    elif direction == LEFT:
        ball_vel = [- (1/60.0) * random.randrange(120, 240), - (1/60.0) * random.randrange(60, 180)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_vel, ball_pos  # these are numbers
    global score1, score2  # these are ints
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]        
    # initial scores        
    score1 = 0
    score2 = 0
    
    # initializing the paddles positions
    leftup1 = [0, HEIGHT / 2 - HALF_PAD_HEIGHT]
    rightup1 = [PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT]
    rightdown1 = [PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]
    leftdown1 =  [0, HEIGHT / 2 + HALF_PAD_HEIGHT]
    leftup2 = [WIDTH - PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT]
    rightup2 = [WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT]
    rightdown2 = [WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]
    leftdown2 =  [WIDTH - PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]
    paddle1_pos = [leftup1, rightup1, rightdown1, leftdown1]
    paddle2_pos = [leftup2, rightup2, rightdown2, leftdown2]
    paddle1_vel = 0
    paddle2_vel = paddle1_vel

def recenter_ball():
    # Hold the ball in the center of canvas once scored
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
     
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # update ball
    if (ball_pos[1] >= HEIGHT - BALL_RADIUS) or (ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White") 
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos[0][1] + paddle1_vel >= 0) and (paddle1_pos[3][1] + paddle1_vel<= HEIGHT):
        paddle1_pos[0][1] += paddle1_vel
        paddle1_pos[1][1] += paddle1_vel
        paddle1_pos[2][1] += paddle1_vel
        paddle1_pos[3][1] += paddle1_vel
        
    if (paddle2_pos[0][1] + paddle2_vel >= 0) and (paddle2_pos[3][1] + paddle2_vel<= HEIGHT):
        paddle2_pos[0][1] += paddle2_vel
        paddle2_pos[1][1] += paddle2_vel
        paddle2_pos[2][1] += paddle2_vel
        paddle2_pos[3][1] += paddle2_vel
        
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 1, 'White', 'White')
    canvas.draw_polygon(paddle2_pos, 1, 'White', 'White')
    
    # determine whether paddle and ball collide    
    if (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH):
        if (ball_pos[1] >= paddle1_pos[0][1]) and (ball_pos[1] <= paddle1_pos[3][1]):
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] = 1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score2 += 1
            recenter_ball()
    elif (ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH):
        if (ball_pos[1] >= paddle2_pos[0][1]) and (ball_pos[1] <= paddle2_pos[3][1]):
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] = 1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score1 += 1
            recenter_ball()
    # draw scores
    canvas.draw_text(str(score1) + '-' + str(score2), [WIDTH / 2 - 34, 50], 50, 'White')
    if (score1 == 0) and (score2 == 0):
        canvas.draw_text("Press SPACE to begin", [130, HEIGHT - 50], 30, 'White')
    else:
        canvas.draw_text("Press SPACE to release the ball", [100, HEIGHT - 50], 30, 'White')

def keydown(key):
    global paddle1_vel, paddle2_vel
    # and 
    if key == simplegui.KEY_MAP['w']:
        if (paddle1_pos[0][1] >= 0):
            paddle1_vel = - paddle1_acc
        else:
            paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        if (paddle1_pos[3][1] <= HEIGHT ):
            paddle1_vel = paddle1_acc
        else:
            paddle1_vel = 0    
    elif key == simplegui.KEY_MAP['up']:
        if (paddle2_pos[0][1] >= 0):
            paddle2_vel = - paddle1_acc
        else:
            paddle1_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        if (paddle2_pos[3][1] <= HEIGHT ):
            paddle2_vel = paddle1_acc
        else:
            paddle2_vel = 0
    # use space to release the ball once scored        
    elif key == simplegui.KEY_MAP['space']:
        if ball_vel == [0, 0]:
            if random.randrange(0, 2) == 0:
                spawn_ball(LEFT)
            else:
                spawn_ball(RIGHT)
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        if paddle1_vel < 0:
            paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']: 
        if paddle1_vel > 0:
            paddle1_vel = 0
    if key == simplegui.KEY_MAP['up']:
        if paddle2_vel < 0:
            paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:        
        if paddle2_vel > 0:
            paddle2_vel = 0

def reset():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', reset, 80)


# start frame
new_game()
frame.start()
