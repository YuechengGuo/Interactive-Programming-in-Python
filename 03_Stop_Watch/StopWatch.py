# template for "Stopwatch: The Game"
import simplegui

# define global variables
t = 0
position1 = [120, 55]
position2 = [210, 30]
font_size = 24
successful_attempts = 0
total_attempts = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """format wanted --> A:BC.D"""
    if t < 6000:
        D = t % 10
        C = (t // 10) % 10
        B = (t // 100) % 6
        A = (t // 600) % 10
        output = str(A) + ":" + str(B) + str(C) + "." + str(D)
    else:
        output = "Game stopped!"
        position1[0] = 70
    return output

# define event handlers for buttons; "Start", "Stop", "Reset"
def time_start():
    timer.start()
    
def time_stop():
    global total_attempts, successful_attempts, running_status
    if timer.is_running():
        total_attempts += 1
        if (t % 10) == 0:
            successful_attempts += 1
      
    timer.stop()
    
def time_reset():
    global t, successful_attempts, total_attempts
    timer.stop()
    t = 0
    successful_attempts = 0
    total_attempts = 0
    position1[0] = 120

# define event handler for timer with 0.1 sec interval
def time_interval():
    """time increment"""
    global t
    if t < 6000:
        t += 1
    else:
        time_stop()

# define draw handler
def draw(canvas):
    """display watch on the frame """
    canvas.draw_text(str(format(t)), position1, font_size, "White")
    canvas.draw_text("Score:" + str(successful_attempts) + "/" + str(total_attempts), position2, 18, "Red")

# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 100)

# register event handlers
timer = simplegui.create_timer(100, time_interval)
frame.set_draw_handler(draw)
frame.add_button("Start", time_start, 100)
frame.add_button("Stop", time_stop, 100)
frame.add_button("Reset", time_reset)

# start frame
frame.start()

# Please remember to review the grading rubric
