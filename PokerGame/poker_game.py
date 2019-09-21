import random, math
from termcolor import colored, cprint
from enum import Enum

#CONSTANTS
NUM_CARD_VALUES = 13
RANDOM_SEED = None #None For No Seed
BOTTOM_ROW = 0
MIDDLE_ROW = 1
TOP_ROW = 2

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
    def playIntoHand(self, first_card, first_hand_num, second_card, second_hand_num):
        self.player_board[first_hand_num].append(first_card)
        self.player_board[second_hand_num].append(second_card)

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
        print(f"TOP    ROW {self.player_board[TOP_ROW]}  Hand Score {HandScorer.score_hand(self.player_board[TOP_ROW], 2)[0]}")
        print(f"MIDDLE ROW {self.player_board[MIDDLE_ROW]}  Hand Score {HandScorer.score_hand(self.player_board[MIDDLE_ROW], 1)[0]}")
        print(f"BOTTOM ROW {self.player_board[BOTTOM_ROW]}   Hand Score {HandScorer.score_hand(self.player_board[BOTTOM_ROW], 0)[0]}")

    def eval_board(self):
        bottom_hand, bottom_score = HandScorer.score_hand(self.player_board[BOTTOM_ROW], BOTTOM_ROW)
        middle_hand, middle_score = HandScorer.score_hand(self.player_board[BOTTOM_ROW], BOTTOM_ROW)
        top_hand, top_score = HandScorer.score_hand(self.player_board[BOTTOM_ROW], BOTTOM_ROW)



class Card:
    suit_names = ["Clubs", "Spades", "Hearts", "Diamonds"]
    card_names = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
    short_card_names = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    short_suit_names = ["C", "S", "H", "D"]

    # Either pass suit, value or just 0-51 for easier generation of a deck
    def __init__(self, suit, value=-1):
        if value == -1:
            self.suit = math.floor(suit / NUM_CARD_VALUES)
            self.value = suit - NUM_CARD_VALUES*math.floor(suit / NUM_CARD_VALUES)
        else:
            self.suit = suit
            self.value = value

    def __str__(self):
        return f"{self.short_card_names[self.value]}{self.short_suit_names[self.suit]}"

    def __repr__(self):
        return self.__str__()

class Rankings(Enum):
        HIGH_CARD = 0
        PAIR = 1
        THREE_CARD = 2
        STRAIGHT = 3
        FLUSH = 4
        FULL_HOUSE = 5
        FOUR_CARD = 6
        STRAIGHT_FLUSH = 7

class HandScorer: 
    BOTTOM_ROW_SCORING = {
        Rankings.STRAIGHT_FLUSH.value: 15,
        Rankings.FOUR_CARD.value: 10,
        Rankings.FULL_HOUSE.value: 6,
        Rankings.FLUSH.value: 4,
        Rankings.STRAIGHT.value: 2,
        Rankings.THREE_CARD.value: 0,
        Rankings.PAIR.value: 0,
        Rankings.HIGH_CARD.value: 0
    }

    MIDDLE_ROW_SCORING = {
        Rankings.STRAIGHT_FLUSH.value: 30,
        Rankings.FOUR_CARD.value: 20,
        Rankings.FULL_HOUSE.value: 12,
        Rankings.FLUSH.value: 8,
        Rankings.STRAIGHT.value: 4,
        Rankings.THREE_CARD.value: 2,
        Rankings.PAIR.value: 0,
        Rankings.HIGH_CARD.value: 0
    }

    # A pair of 5s is worth 0 points
    TOP_ROW_ZERO_PAIR = 3

    def score_hand(hand, row):
        power_range = HandScorer.build_power_range(hand)

        score = 0
        ## TODO NEED to handle full house

        if row == BOTTOM_ROW:
            for item in power_range:
                score += HandScorer.BOTTOM_ROW_SCORING[item[0]]
        elif row == MIDDLE_ROW:
            for item in power_range:
                score += HandScorer.MIDDLE_ROW_SCORING[item[0]]
        else:
            for item in power_range:
                if item[0] == Rankings.PAIR.value:
                    #Pair of sixes worth 1, then 1 point for every subsequent increase 
                    score += max(item[1]-HandScorer.TOP_ROW_ZERO_PAIR, 0)
                elif item[0] == Rankings.THREE_CARD.value:
                    # TRIP 2s -> 10, then 1 point for every subsequent increase
                    score += 10 + item[1]

        return score, power_range

    def build_power_range(hand):
        '''Scores a single poker hand (3 or 5 cards)
        Builds a range from best hand to worst, with type of pair

        Returns a list in the format (CARD_RANKING, HIGH VALUE CARD)
        [(1, 12), (1, 0), (0, 4)] -> represents pair of aces, pair of twos, and a highcard 6
        [(2, 4), (1, 2)] -> represents triple threes, pair of fours (E.G full house)

        '''

        # Build map of num_cards for each value
        value_range = [0] * NUM_CARD_VALUES

        for card in hand:
            value_range[card.value] += 1

        
        # Build power range
        power_range = []
        power_range = power_range + HandScorer.four_of_kind_rankings(value_range)

        straight_flush_rankings = []
        straight_flush_rankings = straight_flush_rankings + HandScorer.straight_rankings(value_range)
        straight_flush_rankings = straight_flush_rankings + HandScorer.flush_rankings(hand)

        # Special case if straight flush
        if len(straight_flush_rankings) > 5:
            for i in range(5):
                power_range.append((Rankings.STRAIGHT_FLUSH.value, straight_flush_rankings[i][1]))
        else:
            power_range = power_range + straight_flush_rankings

        if power_range == []:
            power_range = power_range + HandScorer.three_of_kind_rankings(value_range)
            power_range = power_range + HandScorer.pair_rankings(value_range)
            power_range = power_range + HandScorer.high_card_rankings(value_range)

        return sorted(power_range)[::-1] 

    def high_card_rankings(value_range):
        power_range = []

        for card_num in range(NUM_CARD_VALUES):
            if (value_range[card_num] == 1):
                value_range[card_num] = 0
                power_range.append((Rankings.HIGH_CARD.value, card_num))

        return power_range

    def pair_rankings(value_range):
        power_range = []

        for card_num in range(NUM_CARD_VALUES):
            if (value_range[card_num] == 2):
                value_range[card_num] = 0
                power_range.append((Rankings.PAIR.value, card_num))

        return power_range

    def three_of_kind_rankings(value_range):
        for card_num in range(NUM_CARD_VALUES):
            if (value_range[card_num] == 3):
                value_range[card_num] = 0
                return [(Rankings.THREE_CARD.value, card_num)]

        return []

    def straight_rankings(value_range):
        for card_num in range(NUM_CARD_VALUES-5):
            for j in range(5):
                if (value_range[card_num+j] != 1):
                    break
                elif j == 4:
                    return [(Rankings.STRAIGHT.value, card_num + 4)]

        return []

    def flush_rankings(hand):
        if len(hand) < 5:
            return []

        power_range = []
        power_range.append((Rankings.FLUSH.value, hand[0].value))
        for i in range(1, len(hand)):
            if hand[i].suit != hand[i-1].suit:
                return []
            else:
                power_range.append((Rankings.FLUSH.value, hand[i].value))

        return power_range

    def four_of_kind_rankings(value_range):
        for card_num in range(NUM_CARD_VALUES):
            if (value_range[card_num] == 4):
                return [(Rankings.FOUR_CARD.value, card_num)]

        return []