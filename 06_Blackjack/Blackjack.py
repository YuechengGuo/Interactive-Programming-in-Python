# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
padding = 20
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        self.cardinhand = ""
        for i in self.hand:
            self.cardinhand += " " + str(i)
        return "Hand contains" + self.cardinhand

    def add_card(self, card):
        # add a card object to a hand
        self.hand.extend([card])

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        aces = False
        for i in self.hand:            
            value += VALUES[i.get_rank()]
            if (i.get_rank() == 'A'):
                aces = True
        if (value + 10 <= 21) and (aces):
            value += 10
        return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i in self.hand:
            i.draw(canvas, pos)
            pos[0] += padding + CARD_SIZE[0]
            
        

    
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for i in SUITS:
            self.deck.extend([Card(i, j) for j in RANKS])
           

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck) # use random.shuffle()

    def deal_card(self):
        # deal a card object from the deck
        self.dealtcard = self.deck[-1]
        self.deck.pop(-1)
        return self.dealtcard
    
    def __str__(self):
        # return a string representing the deck
        self.cardindeck = ""
        for i in self.deck:
            self.cardindeck += " " + str(i)
        return "Deck contains" + self.cardindeck



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hands, dealer_hands, score, give_up
    give_up = False
    if in_play:
        score -= 1
        give_up = True
    else:
        outcome = 'Hit or Stand?'
    deck = Deck()
    deck.shuffle()
    player_hands = Hand()
    dealer_hands = Hand()
    for i in range(2):
        player_hands.add_card(deck.deal_card())
        dealer_hands.add_card(deck.deal_card())
        in_play = True
#    print deck
#    print player_hands
#    print dealer_hands

def hit():
    global score, in_play, outcome, give_up
    # if the hand is in play, hit the player
    if in_play:
        give_up = False
        outcome = ''
        player_hands.add_card(deck.deal_card())
        # if busted, assign a message to outcome, update in_play and score
        if player_hands.get_value() > 21:
            outcome = 'You have busted! New deal?'
            score -= 1
            in_play = False
        else:
            outcome = 'Hit or Stand?'

def stand():
    global score, in_play, outcome, give_up
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        give_up = False
        outcome = ''
        while dealer_hands.get_value() < 17:
            dealer_hands.add_card(deck.deal_card())
        if dealer_hands.get_value() > 21:
            outcome = 'Dealer has busted! Wanna more?'
            score += 1
        else:
            # assign a message to outcome, update in_play and score
            if player_hands.get_value() > dealer_hands.get_value():
                # player wins
                score += 1
                outcome = 'You win! Wanna more?'
            else:
                # dealer wins
                score -= 1
                outcome = 'You lose. New deal?'
    in_play = False
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    dealer_pos = [20, 150]
    player_pos = [20, 450]

    player_hands.draw(canvas, player_pos)
    dealer_hands.draw(canvas, dealer_pos)
    canvas.draw_text('Black Jack', [220 ,75], 40, 'Black', 'serif')
    canvas.draw_text(outcome, [60, 340], 35, 'White')
    canvas.draw_text('SCORE: ' + str(score), [430, 120], 30, 'White')
    if give_up:
        canvas.draw_text('You gave up the last round. Wanna more?', [15, 285], 32, 'White')
    if in_play:
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [20 + CARD_CENTER[0], 150 + CARD_CENTER[1]], CARD_SIZE)
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric
