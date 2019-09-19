import PokerGame

game = PokerGame.PokerGame()

for i in range(3):
    hand = game.deal()
    game.playIntoHand(hand[0], 0, hand[1], 1)
game.print_board()


print(hand)