from poker_game import HandScorer, Card, Rankings

CLUBS = 1
SPADES = 2

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



