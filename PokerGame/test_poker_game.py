from poker_game import HandScorer, Card, Rankings
from poker_game import BOTTOM_ROW, MIDDLE_ROW, TOP_ROW, NUM_CARD_VALUES
CLUBS = 0
SPADES = 1
HEARTS = 2
DIAMONDS = 3

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

'''Test all possible straight flushes in the middle row'''
def test_straight_flush_middle_row():
    correct_score = 30
    all_card_values = list(range(0, NUM_CARD_VALUES - 5))
    all_suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
    for i, bottom_value in enumerate(all_card_values):
        for suit in all_suits:
            deck = [Card(suit, bottom_value), Card(suit, bottom_value + 1), Card(suit, bottom_value + 2),
                    Card(suit, bottom_value + 3), Card(suit, bottom_value + 4)]
            score, power_range = HandScorer.score_hand(deck, MIDDLE_ROW)

            assert correct_score == score

    # Special Case, Ace Low Straight
    for suit in all_suits:
            deck = [Card(suit, 12), Card(suit, 0), Card(suit, 1),
                    Card(suit, 2), Card(suit, 3)]
            score, power_range = HandScorer.score_hand(deck, MIDDLE_ROW)

            assert correct_score == score

'''Test all possible royal flushes in the middle row'''
def test_royal_flush_middle_row():
    correct_score = 50
    all_suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
    for suit in all_suits:
        deck = [Card(suit, 8), Card(suit, 9), Card(suit, 10),
                Card(suit, 11), Card(suit, 12)]
        score, power_range = HandScorer.score_hand(deck, MIDDLE_ROW)

        assert score == correct_score


'''BOTTOM ROW'''

'''Test trips of all values on the bottom row'''
def test_triple_bottom_row():
    correct_score = 0
    all_card_values = list(range(0, NUM_CARD_VALUES))
    for i, value in enumerate(all_card_values):
        deck = [Card(CLUBS, value), Card(SPADES, value), Card(HEARTS, value)]
        score, power_range = HandScorer.score_hand(deck, BOTTOM_ROW)
        assert correct_score == score

'''Test all possible straights with random suit values'''
def test_straight_bottom_row():
    correct_score = 2
    all_card_values = list(range(0, NUM_CARD_VALUES - 4))
    for i, bottom_value in enumerate(all_card_values):
        deck = [Card(CLUBS, bottom_value), Card(SPADES, bottom_value+1), Card(HEARTS, bottom_value+2),
                Card(DIAMONDS, bottom_value+3), Card(HEARTS, bottom_value+4)]
        score, power_range = HandScorer.score_hand(deck, BOTTOM_ROW)
        assert correct_score == score
    # Special Case, Ace Low Straight
    deck = [Card(CLUBS, 12), Card(SPADES, 0), Card(HEARTS, 1),
            Card(DIAMONDS, 2), Card(HEARTS, 3)]
    score, power_range = HandScorer.score_hand(deck, BOTTOM_ROW)
    assert correct_score == score

'''Test flush with different suits and test cases provided for card values'''
def test_flush_bottom_row():
    correct_score = 4
    all_suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
    test_cases = [[0,1,2,3,5], [0, 3, 5, 7, 11], [7,9,10,11,12], [0,1,2,11,12]]
    for suit in all_suits:
        for case in test_cases:
            deck = [Card(suit, case[0]), Card(suit, case[1]), Card(suit, case[2]),
                Card(suit, case[3]), Card(suit, case[4])]

            score, power_range = HandScorer.score_hand(deck, BOTTOM_ROW)
            assert correct_score == score

'''Test full house in middle row: Iterate through all possible value for trips and the values for the pair'''
def test_full_house_bottom_row():
    correct_score = 6
    all_card_values = list(range(0, NUM_CARD_VALUES))
    for i, triple_value in enumerate(all_card_values):
        pair_values = all_card_values.copy()
        pair_values.remove(triple_value)
        for pair_value in pair_values:
            deck = [Card(CLUBS, triple_value), Card(SPADES, pair_value), Card(HEARTS, triple_value),
                    Card(DIAMONDS, pair_value), Card(HEARTS, triple_value)]
            score, power_range = HandScorer.score_hand(deck, BOTTOM_ROW)
            assert correct_score == score

'''Test Quads + extra card in the bottom row'''
def test_quads_bottom_row():
    correct_score = 10
    all_card_values = list(range(0, NUM_CARD_VALUES))
    for i, quad_value in enumerate(all_card_values):
        # extra values = values for the 5th card in the hand of quads
        extra_values = all_card_values.copy()
        extra_values.remove(quad_value)
        for extra_value in extra_values:
            deck = [Card(CLUBS, quad_value), Card(SPADES, extra_value), Card(HEARTS, quad_value),
                    Card(DIAMONDS, quad_value), Card(HEARTS, quad_value)]
            score, power_range = HandScorer.score_hand(deck, BOTTOM_ROW)
            assert correct_score == score

'''Test all possible straight flushes in the bottom row'''
def test_straight_flush_bottom_row():
    correct_score = 15
    all_card_values = list(range(0, NUM_CARD_VALUES - 5))
    all_suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
    for i, bottom_value in enumerate(all_card_values):
        for suit in all_suits:
            deck = [Card(suit, bottom_value), Card(suit, bottom_value + 1), Card(suit, bottom_value + 2),
                    Card(suit, bottom_value + 3), Card(suit, bottom_value + 4)]
            score, power_range = HandScorer.score_hand(deck, BOTTOM_ROW)

            assert correct_score == score

    # Special Case, Ace Low Straight
    for suit in all_suits:
            deck = [Card(suit, 12), Card(suit, 0), Card(suit, 1),
                    Card(suit, 2), Card(suit, 3)]
            score, power_range = HandScorer.score_hand(deck, BOTTOM_ROW)

            assert correct_score == score

'''Test all possible royal flushes in the bottom row'''
def test_royal_flush_bottom_row():
    correct_score = 25
    all_suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
    for suit in all_suits:
        deck = [Card(suit, 8), Card(suit, 9), Card(suit, 10),
                Card(suit, 11), Card(suit, 12)]
        score, power_range = HandScorer.score_hand(deck, BOTTOM_ROW)

        assert score == correct_score

'''Test compare power rankings function'''

'''Compare decks of different hands (pair vs. straight)'''
def test_compare_power_rankings_general():
    '''High Card, Pair, Trips'''
    deck_high_card = [Card(HEARTS, 0), Card(SPADES, 1), Card(CLUBS, 3),
                Card(SPADES, 5), Card(HEARTS, 9)]
    deck_pair = [Card(HEARTS, 0), Card(SPADES, 0), Card(CLUBS, 3),
                Card(SPADES, 5), Card(HEARTS, 9)]
    deck_trips = [Card(HEARTS, 0), Card(SPADES, 0), Card(CLUBS, 0),
                Card(SPADES, 5), Card(HEARTS, 9)]
    deck_straight = [Card(HEARTS, 0), Card(SPADES, 1), Card(CLUBS, 2),
                Card(SPADES, 3), Card(HEARTS, 4)]
    deck_flush = [Card(HEARTS, 0), Card(HEARTS, 3), Card(HEARTS, 5),
                     Card(HEARTS, 7), Card(HEARTS, 10)]
    deck_full_house = [Card(HEARTS, 0), Card(SPADES, 0), Card(CLUBS, 0),
                Card(SPADES, 1), Card(HEARTS, 1)]
    deck_quads = [Card(HEARTS, 0), Card(SPADES, 0), Card(CLUBS, 0),
                Card(SPADES, 0), Card(HEARTS, 1)]
    deck_straight_flush = [Card(HEARTS, 0), Card(HEARTS, 1), Card(HEARTS, 2),
                Card(HEARTS, 3), Card(HEARTS, 4)]
    deck_royal_flush = [Card(HEARTS, 8), Card(HEARTS, 9), Card(HEARTS, 10),
                Card(HEARTS, 11), Card(HEARTS, 12)]
    ordered_deck_by_rank = [deck_high_card, deck_pair, deck_trips, deck_straight, deck_flush, deck_full_house,
                            deck_quads, deck_straight_flush, deck_royal_flush]

    for i, deck in enumerate(ordered_deck_by_rank[1:]):
        deck_A = deck
        score_A, power_range_A = HandScorer.score_hand(deck_A, BOTTOM_ROW)

        deck_B = ordered_deck_by_rank[i]
        score_B, power_range_B = HandScorer.score_hand(deck_B, BOTTOM_ROW)

        assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 1
        assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == -1
        assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0
        assert HandScorer.compare_power_rankings(power_range_B, power_range_B) == 0

def test_compare_power_rankings_pair():
    # higher pair comparison
    all_card_values = list(range(1, NUM_CARD_VALUES))
    for i, value in enumerate(all_card_values):
        deck_A = [Card(CLUBS, value), Card(SPADES, value)]
        score_A, power_range_A = HandScorer.score_hand(deck_A, TOP_ROW)

        deck_B = [Card(CLUBS, value-1), Card(SPADES, value-1)]
        score_B, power_range_B = HandScorer.score_hand(deck_B, TOP_ROW)
        assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 1
        assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == -1
        assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0
        assert HandScorer.compare_power_rankings(power_range_B, power_range_B) == 0

def test_compare_power_rankings_high_card():
    all_card_values = list(range(2, NUM_CARD_VALUES))
    for i, value in enumerate(all_card_values):
        deck_A = [Card(CLUBS, value), Card(SPADES, value-1)]
        score_A, power_range_A = HandScorer.score_hand(deck_A, TOP_ROW)

        deck_B = [Card(CLUBS, value-1), Card(SPADES, value-2)]
        score_B, power_range_B = HandScorer.score_hand(deck_B, TOP_ROW)
        assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 1
        assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == -1
        assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0
        assert HandScorer.compare_power_rankings(power_range_B, power_range_B) == 0


def test_compare_power_rankings_trips():
    all_card_values = list(range(1, NUM_CARD_VALUES))
    for i, value in enumerate(all_card_values):
        deck_A = [Card(CLUBS, value), Card(SPADES, value), Card(HEARTS, value)]
        score_A, power_range_A = HandScorer.score_hand(deck_A, TOP_ROW)

        deck_B = [Card(CLUBS, value - 1), Card(SPADES, value - 1), Card(HEARTS, value-1)]
        score_B, power_range_B = HandScorer.score_hand(deck_B, TOP_ROW)
        assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 1
        assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == -1
        assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0
        assert HandScorer.compare_power_rankings(power_range_B, power_range_B) == 0



def test_compare_power_rankings_straight():
    all_card_values = list(range(1, NUM_CARD_VALUES - 4))
    for i, bottom_value in enumerate(all_card_values):
        deck_A = [Card(CLUBS, bottom_value), Card(SPADES, bottom_value + 1), Card(HEARTS, bottom_value + 2),
                Card(DIAMONDS, bottom_value + 3), Card(HEARTS, bottom_value + 4)]
        score_A, power_range_A = HandScorer.score_hand(deck_A, BOTTOM_ROW)
        deck_B = [Card(CLUBS, bottom_value-1), Card(SPADES, bottom_value), Card(HEARTS, bottom_value + 1),
                 Card(DIAMONDS, bottom_value + 2), Card(HEARTS, bottom_value + 3)]
        score_B, power_range_B = HandScorer.score_hand(deck_B, BOTTOM_ROW)

        assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 1
        assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == -1
        assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0
        assert HandScorer.compare_power_rankings(power_range_B, power_range_B) == 0

    # Ace low vs higher straight
    deck_A = [Card(CLUBS, 11), Card(HEARTS, 10), Card(CLUBS, 9),
              Card(HEARTS, 8), Card(DIAMONDS, 7)]
    score_A, power_range_A = HandScorer.score_hand(deck_A, BOTTOM_ROW)

    deck_B = [Card(CLUBS, 12), Card(HEARTS, 0), Card(CLUBS, 1),
              Card(HEARTS, 2), Card(DIAMONDS, 3)]
    score_B, power_range_B = HandScorer.score_hand(deck_B, BOTTOM_ROW)
    assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 1
    assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == -1
    assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0


def test_compare_power_rankings_flush():
    all_suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
    test_cases = [[0, 1, 2, 3, 5], [0, 3, 5, 7, 11], [7, 9, 2, 11, 12], [0, 1, 10, 11, 12]]
    for suit in all_suits:
        for i in range(1,len(test_cases)):
            deck_A = [Card(suit, test_cases[i][0]), Card(suit, test_cases[i][1]), Card(suit, test_cases[i][2]),
                    Card(suit, test_cases[i][3]), Card(suit, test_cases[i][4])]
            score_A, power_range_A = HandScorer.score_hand(deck_A, BOTTOM_ROW)

            deck_B = [Card(suit, test_cases[i-1][0]), Card(suit, test_cases[i-1][1]), Card(suit, test_cases[i-1][2]),
                      Card(suit, test_cases[i-1][3]), Card(suit, test_cases[i-1][4])]
            score_B, power_range_B = HandScorer.score_hand(deck_B, BOTTOM_ROW)

            assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 1
            assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == -1
            assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0
            assert HandScorer.compare_power_rankings(power_range_B, power_range_B) == 0


def test_compare_power_rankings_full_house():
    '''Same pair value, different triple value'''
    all_card_values = list(range(1, NUM_CARD_VALUES))
    for i, triple_value_A in enumerate(all_card_values):
        for j in range(0, i):
            triple_value_B = all_card_values[j]
            pair_values = all_card_values.copy()
            pair_values.remove(triple_value_A)
            pair_values.remove(triple_value_B)
            for pair_value in pair_values:
                deck_A = [Card(CLUBS, triple_value_A), Card(SPADES, pair_value), Card(HEARTS, triple_value_A),
                        Card(DIAMONDS, pair_value), Card(HEARTS, triple_value_A)]
                score_A, power_range_A = HandScorer.score_hand(deck_A, BOTTOM_ROW)

                deck_B = [Card(CLUBS, triple_value_B), Card(SPADES, pair_value), Card(HEARTS, triple_value_B),
                          Card(DIAMONDS, pair_value), Card(HEARTS, triple_value_B)]
                score_B, power_range_B = HandScorer.score_hand(deck_B, BOTTOM_ROW)
                assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 1
                assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == -1
                assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0
                assert HandScorer.compare_power_rankings(power_range_B, power_range_B) == 0
    '''Same triple value, different pair value'''
    all_card_values = list(range(1, NUM_CARD_VALUES))
    for i, pair_value_A in enumerate(all_card_values):
        for j in range(0, i):
            pair_value_B = all_card_values[j]
            triple_values = all_card_values.copy()
            triple_values.remove(pair_value_A)
            triple_values.remove(pair_value_B)
            for triple_value in triple_values:
                deck_A = [Card(CLUBS, triple_value), Card(SPADES, pair_value_A), Card(HEARTS, triple_value),
                          Card(DIAMONDS, pair_value_A), Card(HEARTS, triple_value)]
                score_A, power_range_A = HandScorer.score_hand(deck_A, BOTTOM_ROW)

                deck_B = [Card(CLUBS, triple_value), Card(SPADES, pair_value_B), Card(HEARTS, triple_value),
                          Card(DIAMONDS, pair_value_B), Card(HEARTS, triple_value)]
                score_B, power_range_B = HandScorer.score_hand(deck_B, BOTTOM_ROW)
                assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 1
                assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == -1
                assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0
                assert HandScorer.compare_power_rankings(power_range_B, power_range_B) == 0


def test_compare_power_rankings_quads():
    all_card_values = list(range(1, NUM_CARD_VALUES))
    all_locs = [BOTTOM_ROW, MIDDLE_ROW]
    for loc in all_locs:
        for i, quad_value in enumerate(all_card_values):
            # extra values = values for the 5th card in the hand of quads
            extra_values = all_card_values.copy()
            extra_values.remove(quad_value)
            extra_values.remove(all_card_values[i-1])
            for extra_value in extra_values:
                deck_A = [Card(CLUBS, quad_value), Card(SPADES, extra_value), Card(HEARTS, quad_value),
                        Card(DIAMONDS, quad_value), Card(HEARTS, quad_value)]
                score_A, power_range_A = HandScorer.score_hand(deck_A, loc)

                deck_B = [Card(CLUBS, quad_value-1), Card(SPADES, extra_value), Card(HEARTS, quad_value-1),
                        Card(DIAMONDS, quad_value-1), Card(HEARTS, quad_value-1)]

                score_B, power_range_B = HandScorer.score_hand(deck_B, loc)
                assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 1
                assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == -1
                assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0
                assert HandScorer.compare_power_rankings(power_range_B, power_range_B) == 0


def test_compare_power_rankings_straight_flush():
    all_card_values = list(range(1, NUM_CARD_VALUES - 5))
    all_suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
    all_locs = [BOTTOM_ROW, MIDDLE_ROW]
    for loc in all_locs:
        for i, bottom_value in enumerate(all_card_values):
            for suit in all_suits:
                deck_A = [Card(suit, bottom_value), Card(suit, bottom_value + 1), Card(suit, bottom_value + 2),
                        Card(suit, bottom_value + 3), Card(suit, bottom_value + 4)]
                score_A, power_range_A = HandScorer.score_hand(deck_A, loc)

                deck_B = [Card(suit, bottom_value-1), Card(suit, bottom_value), Card(suit, bottom_value + 1),
                          Card(suit, bottom_value + 2), Card(suit, bottom_value + 3)]
                score_B, power_range_B = HandScorer.score_hand(deck_B, loc)

                assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 1
                assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == -1
                assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0
                assert HandScorer.compare_power_rankings(power_range_B, power_range_B) == 0

        # Special Case, Ace Low Straight
        for suit in all_suits:
            deck_A = [Card(suit, 11), Card(suit, 10), Card(suit, 9),
                    Card(suit, 8), Card(suit, 7)]
            score_A, power_range_A = HandScorer.score_hand(deck_A, loc)

            deck_B = [Card(suit, 12), Card(suit, 0), Card(suit, 1),
                    Card(suit, 2), Card(suit, 3)]
            score_B, power_range_B = HandScorer.score_hand(deck_B, loc)
            assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 1
            assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == -1
            assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0
            assert HandScorer.compare_power_rankings(power_range_B, power_range_B) == 0

def test_compare_power_rankings_royal_flush():
    all_suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
    all_locs = [BOTTOM_ROW, MIDDLE_ROW]
    for loc in all_locs:
        for i in range(1,4):
            deck_A = [Card(all_suits[i], 12), Card(all_suits[i], 11), Card(all_suits[i], 10),
                    Card(all_suits[i], 9), Card(all_suits[i], 8)]
            score_A, power_range_A = HandScorer.score_hand(deck_A, loc)

            deck_B = [Card(all_suits[i-1], 12), Card(all_suits[i-1], 11), Card(all_suits[i-1], 10),
                    Card(all_suits[i-1], 9), Card(all_suits[i-1], 8)]
            score_B, power_range_B = HandScorer.score_hand(deck_B, loc)

            assert HandScorer.compare_power_rankings(power_range_A, power_range_B) == 0
            assert HandScorer.compare_power_rankings(power_range_B, power_range_A) == 0
            assert HandScorer.compare_power_rankings(power_range_A, power_range_A) == 0
            assert HandScorer.compare_power_rankings(power_range_B, power_range_B) == 0



test_straight_flush_bottom_row()
test_compare_power_rankings_straight()
test_compare_power_rankings_quads()
test_compare_power_rankings_full_house()
test_compare_power_rankings_flush()
test_compare_power_rankings_general()
test_compare_power_rankings_trips()
test_compare_power_rankings_high_card()
test_compare_power_rankings_pair()
test_compare_power_rankings_straight_flush()
test_compare_power_rankings_royal_flush()

#TODO Implement different row comparisons