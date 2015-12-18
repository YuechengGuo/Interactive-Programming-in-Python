# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global init_list, exposed_list, state, turns
    turns = 0
    state = 0
    source_list1 = range(8)
    source_list2 = range(8)
    source_list1.extend(source_list2)
    init_list = source_list1
    random.shuffle(init_list)    
    exposed_list = [False for i in range(len(init_list))]
    label.set_text('Turns = ' + str(turns))
    # print init_list, exposed_list
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, card1_ind, card2_ind, turns
    card_num = pos[0] // card_size[0] # card_num describes which card is selected.
    if not exposed_list[card_num]:
        # exposed_list[card_num] = True
        if state == 0:
            state = 1
            card1_ind = card_num
            exposed_list[card1_ind] = True
        elif state == 1:
            state = 2
            card2_ind = card_num
            exposed_list[card2_ind] = True
        else:
            state = 1
            if init_list[card1_ind] != init_list[card2_ind]:
                exposed_list[card1_ind] = False
                exposed_list[card2_ind] = False
            card1_ind = card_num
            exposed_list[card1_ind] = True
            turns += 1
            label.set_text('Turns = ' + str(turns))
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global card_size
    card_size = [50, 100]
    card_init_pos = [[0, 0], [49, 0], [49, 100], [0, 100]]
    card_pos = [[0, 0], [50, 0], [50, 100], [0, 100]]
    count = range(0, len(init_list))
    for index in count:
        if exposed_list[index]:
            canvas.draw_text(str(init_list[index]), [5 + 50 * index, 80], 85, 'White')
        else:
            card_pos[0][0] = card_init_pos[0][0] + index * card_size[0] 
            card_pos[1][0] = card_init_pos[1][0] + index * card_size[0] 
            card_pos[2][0] = card_init_pos[2][0] + index * card_size[0] 
            card_pos[3][0] = card_init_pos[3][0] + index * card_size[0] 
            canvas.draw_polygon(card_pos, 1, 'Black','Green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
