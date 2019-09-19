

def populateDeck():
    deck = [Card(suit, value) for suit in Card.suits for value in range(1, 14)]

class Card:
    suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
    def __init__(self, suit, value):
        self.value = value
        self.suit = suit
    def __str__ (self):
        return str(self.value) + " of " + self.suit

class PlayerHand:
    bottom_hand = []


populateDeck()