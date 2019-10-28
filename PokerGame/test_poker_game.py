from poker_game import HandScorer, Card, Rankings
from poker_game import BOTTOM_ROW, MIDDLE_ROW, TOP_ROW, NUM_CARD_VALUES
CLUBS = 1
SPADES = 2
HEARTS = 3
DIAMONDS = 4

def test_basic():
    assert 1 == 1

def test_double():
    deck = [Card(CLUBS, 2), Card(SPADES, 2)]
    ranking = HandScorer.build_power_range(deck)
    assert ranking[0][0] == Rankings.PAIR.value

def test_three_of_kind():
    deck = [Card(CLUBS, 2), Card(SPADES, 2), Card(SPADES, 2)]
    ranking = HandScorer.build_power_range(deck)
    assert ranking[0][0] == Rankings.THREE_CARD.value

def test_four_of_kind():
    deck = [Card(CLUBS, 2), Card(SPADES, 2), Card(SPADES, 2), Card(SPADES, 2)]
    ranking = HandScorer.build_power_range(deck)
    assert ranking[0][0] == Rankings.FOUR_CARD.value

def test_straight():
    deck = [Card(SPADES, 2), Card(CLUBS, 3), Card(CLUBS, 4),Card(CLUBS, 5), Card(CLUBS, 6)]
    ranking = HandScorer.build_power_range(deck)
    assert ranking[0][0] == Rankings.STRAIGHT.value

def test_flush():
    deck = [Card(CLUBS, 2), Card(CLUBS, 3), Card(CLUBS, 4),Card(CLUBS, 5), Card(CLUBS, 8)]
    ranking = HandScorer.build_power_range(deck)
    assert ranking[0][0] == Rankings.FLUSH.value


def test_straight_flush():
    deck = [Card(CLUBS, 2), Card(CLUBS, 3), Card(CLUBS, 4),Card(CLUBS, 5), Card(CLUBS, 6)]
    ranking = HandScorer.build_power_range(deck)
    assert ranking[0][0] == Rankings.STRAIGHT_FLUSH.value

def test_full_house():
    deck = [Card(CLUBS, 2), Card(SPADES, 2), Card(HEARTS, 2), Card(CLUBS, 3), Card(HEARTS, 3)]
    ranking = HandScorer.build_power_range(deck)
    assert ranking[0][0] == Rankings.FULL_HOUSE.value


'''Test a pair of all values on the top row'''
def test_pair_top_row():
    correct_scores = [0,0,0,0,1,2,3,4,5,6,7,8,9]
    all_card_values = list(range(0,NUM_CARD_VALUES))
    for i, value in enumerate(all_card_values):
        deck = [Card(CLUBS, value), Card(SPADES, value)]
        score, power_range = HandScorer.score_hand(deck, TOP_ROW)
        assert correct_scores[i] == score

'''Test trips of all values on the top row'''
def test_triple_top_row():
    correct_scores = [10,11,12,13,14,15,16,17,18,19,20,21,22]
    all_card_values = list(range(0,NUM_CARD_VALUES))
    for i, value in enumerate(all_card_values):
        deck = [Card(CLUBS, value), Card(SPADES, value), Card(HEARTS, value)]
        score, power_range = HandScorer.score_hand(deck, TOP_ROW)
        assert correct_scores[i] == score

'''Test trips of all values on the middle row'''
def test_triple_middle_row():
    correct_score = 2
    all_card_values = list(range(0, NUM_CARD_VALUES))
    for i, value in enumerate(all_card_values):
        deck = [Card(CLUBS, value), Card(SPADES, value), Card(HEARTS, value)]
        score, power_range = HandScorer.score_hand(deck, MIDDLE_ROW)
        assert correct_score == score

'''Test all possible straights with random suit values'''
def test_straight_middle_row():
    correct_score = 4
    all_card_values = list(range(0, NUM_CARD_VALUES - 4))
    for i, bottom_value in enumerate(all_card_values):
        deck = [Card(CLUBS, bottom_value), Card(SPADES, bottom_value+1), Card(HEARTS, bottom_value+2),
                Card(DIAMONDS, bottom_value+3), Card(HEARTS, bottom_value+4)]
        score, power_range = HandScorer.score_hand(deck, MIDDLE_ROW)
        assert correct_score == score
    # Special Case, Ace Low Straight
    deck = [Card(CLUBS, 12), Card(SPADES, 0), Card(HEARTS, 1),
            Card(DIAMONDS, 2), Card(HEARTS, 3)]
    score, power_range = HandScorer.score_hand(deck, MIDDLE_ROW)
    assert correct_score == score

'''Test flush with different suits and test cases provided for card values'''
def test_flush_middle_row():
    correct_score = 8
    all_suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
    test_cases = [[0,1,2,3,5], [0, 3, 5, 7, 11], [7,9,10,11,12], [0,1,2,11,12]]
    for suit in all_suits:
        for case in test_cases:
            deck = [Card(suit, case[0]), Card(suit, case[1]), Card(suit, case[2]),
                Card(suit, case[3]), Card(suit, case[4])]

            score, power_range = HandScorer.score_hand(deck, MIDDLE_ROW)
            assert correct_score == score

'''Test full house in middle row: Iterate through all possible value for trips and the values for the pair'''
def test_full_house_middle_row():
    correct_score = 12
    all_card_values = list(range(0, NUM_CARD_VALUES))
    for i, triple_value in enumerate(all_card_values):
        pair_values = all_card_values.copy()
        pair_values.remove(triple_value)
        for pair_value in pair_values:
            deck = [Card(CLUBS, triple_value), Card(SPADES, pair_value), Card(HEARTS, triple_value),
                    Card(DIAMONDS, pair_value), Card(HEARTS, triple_value)]
            score, power_range = HandScorer.score_hand(deck, MIDDLE_ROW)
            assert correct_score == score

'''Test Quads + extra card in the middle row'''
def test_quads_middle_row():
    correct_score = 20
    all_card_values = list(range(0, NUM_CARD_VALUES))
    for i, quad_value in enumerate(all_card_values):
        # extra values = values for the 5th card in the hand of quads
        extra_values = all_card_values.copy()
        extra_values.remove(quad_value)
        for extra_value in extra_values:
            deck = [Card(CLUBS, quad_value), Card(SPADES, extra_value), Card(HEARTS, quad_value),
                    Card(DIAMONDS, quad_value), Card(HEARTS, quad_value)]
            score, power_range = HandScorer.score_hand(deck, MIDDLE_ROW)
            assert correct_score == score

# TODO Add Ace Low
def test_straight_flush():
    correct_score = 15
    all_card_values = list(range(0, NUM_CARD_VALUES - 5))
    all_suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
    for i, bottom_value in enumerate(all_card_values):
        for suit in all_suits:
            deck = [Card(suit, bottom_value), Card(suit, bottom_value + 1), Card(suit, bottom_value + 2),
                    Card(suit, bottom_value + 3), Card(suit, bottom_value + 4)]
            score, power_range = HandScorer.score_hand(deck, MIDDLE_ROW)
            print(bottom_value)
            print(score)
            print(power_range)
            assert correct_score == score

test_straight_middle_row()