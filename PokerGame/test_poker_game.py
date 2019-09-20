from HandScorer import HandScorer
from PokerGame import Card

def test_basic():
    assert 1 == 1

def test_double():
    Deck = [Card(Card.Suits.Clubs, 2), Card(Card.Suits.Spades, 2)]
    scorer = HandScorer(Deck)
    assert scorer.hasPair()
