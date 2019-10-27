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

def test_straight_middle_row():
    correct_score = 4
    all_card_values = list(range(0, NUM_CARD_VALUES - 4))
    for i, bottom_value in enumerate(all_card_values):
        deck = [Card(CLUBS, bottom_value), Card(SPADES, bottom_value+1), Card(HEARTS, bottom_value+2),
                Card(DIAMONDS, bottom_value+3), Card(HEARTS, bottom_value+4) ]
        score, power_range = HandScorer.score_hand(deck, MIDDLE_ROW)

        assert correct_score == score

def test_flush_middle_row():
    correct_score = 8

