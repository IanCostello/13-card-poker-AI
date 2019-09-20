import random, math
from termcolor import colored, cprint
from enum import Enum

#DEFINE
NUM_CARD_VALUES = 13
RANDOM_SEED = None #None For No Seed

class PokerGame:
    '''Used to run a game of 13 card poker 
    
    Card values assigned based on number (2 card-0 ... 10-8, J-9, Q-10, K-11, A-12)   
    Probably will need to modify to support an opponent eventually 
    '''

    def __init__(self):
        # Init seed for consistent testing
        random.seed(RANDOM_SEED)

        # Currently on board -- all 0s if empty
        self.player_board = [] 

        # Append Board Sizes
        for i in range(3):
            self.player_board.append([])

        # Init deck
        self.deck = []
        for i in range(52):
            self.deck.append(Card(i))
        random.shuffle(self.deck)

    # hand num corresponds to bottom, mid, or top
    def playIntoHand(self, first_card, first_hand_num, second_card, second_hand_num, third_card, third_hand_num):
        self.player_board[first_hand_num].append(first_card)
        self.player_board[second_hand_num].append(second_card)
        self.player_board[third_hand_num].append(third_card)

    def deal(self):
        ''' Deals cards to the player '''
        player_hand = self.deck[:3]
        self.deck = self.deck[3:]

        return player_hand

    # def play_hand(self, board_after_play, )

    def self_score(self):
        return score_board(self.player_board)

    # def score_board(board):
    
    def print_board(self):
        ''' Prints the current player board state '''

        print(f"TOP    ROW {self.player_board[2]}")
        print(f"MIDDLE ROW {self.player_board[1]}")
        print(f"BOTTOM ROW {self.player_board[0]}")

    def score_hand(self):
        ''' Returns the total score of entire player hand

        [UNIMPLEMENTED]
        '''
        scorer = HandScorer(self.player_board[first_hand_num])

        # Check for straight
        has_straight = True

    class Card:
        suit_names = ["Clubs", "Spades", "Hearts", "Diamonds"]
        card_names = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
        short_card_names = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        short_suit_names = ["C", "S", "H", "D"]

        def __init__(self, value):
            self.value = value - NUM_CARD_VALUES*math.floor(value / NUM_CARD_VALUES)
            self.suit = math.floor(value / NUM_CARD_VALUES)

        def __str__(self):
            return f"{self.short_card_names[self.value]}{self.short_suit_names[self.suit]}"

        def __repr__(self):
            return self.__str__()

    class HandScorer:
        def __init__(self, hand):
            self.hand = hand
            self.value_range = [0] * NUM_CARD_VALUES

            for card in hand:
                if card.value not in self.value_range:
                    self.value_range[card.value] = 0

                self.value_range[card.value] = self.value_range[card.value] + 1

        def hasPair(self):
            for i in range(NUM_CARD_VALUES):
                if (self.value_range[i] == 2):
                    return True
            return False

        def hasTwoPair(self):
            numDoubles = 0
            for i in range(NUM_CARD_VALUES):
                if (self.value_range[i] == 2):
                    return numDoubles
            return numDoubles == 2

        def hasThreeOfKind(self):
            for i in range(NUM_CARD_VALUES):
                if (self.value_range[i] == 3):
                    return True
            return False

        def hasStraight(self):
            for i in range(NUM_CARD_VALUES-5):
                for j in range(5):
                    if (self.value_range[i+j] != 1):
                        break
                    elif j == 5:
                        return True

            return False

        def hasFlush(self):
            for i in range(1, len(self.hand)):
                if self.hand[i].suit != self.hand[i-1].suit:
                    return False
            return True

        def hasFullHouse(self):
            return self.hasPair() and self.hasTriple()

        def hasFourOfKind(self):
            for i in range(NUM_CARD_VALUES):
                if (self.value_range[i] == 4):
                    return True
            return False

        def hasStraightFlush(self):
            return self.hasStraight() + self.hasFlush()
    def set_player_deck(self, deck):
        ''' Sets the deck to a given hand for testing '''
        self.deck = deck;