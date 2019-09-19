class HandScorer:
    def __init__(self, hand, row_num):
        self.hand = hand
        self.value_range = [0] * NUM_CARD_VALUES

        for card in hand:
            if card.value not in self.value_range:
                self.value_range[card.value] = 0

            self.value_range[card.value] = self.value_range[card.value] + 1

    def score(self):
        '''Returns the hand strength and point total
        
        R
        
        Returns:
            hand_strength -- the ranking of a hand (lower is better)
        '''
        if self.row_num == 2:

        else:
            # Score
            score_multiplier = self.row_num + 2 
            if hasStraightFlush():
                return 0, 25 * 2 

    def hasPair(self):
        for i in range(NUM_CARD_VALUES):
            if (value_range[i] == 2):
                return True
        return False

    def hasTwoPair(self):
        numDoubles = 0
        for i in range(NUM_CARD_VALUES):
            if (value_range[i] == 2):
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
        for i in range(1, len(hand)):
            if hand[i].suit != hand[i-1].suit:
                return False
        return True

    def hasFullHouse(self):
        return hasPair() and hasTriple() 

    def hasFourOfKind(self):
        for i in range(NUM_CARD_VALUES):
            if (self.value_range[i] == 4):
                return True
        return False

    def hasStraightFlush(self):
        return hasStraight() + hasFlush()