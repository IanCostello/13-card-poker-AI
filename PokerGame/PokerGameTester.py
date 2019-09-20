import PokerGame
import os

def main():
    game = PokerGame.PokerGame()

    while True:
            
        getDeal(game)
        getDeal(game)
        print_game_state(game)

def getDeal(game):
    hand = game.deal()

    print_game_state(game, hand)
    print("Which card do you want to play first?")
    print(f"Cards To Play -- {hand}")
    first_card_num = int(input("Card To Play (1,2,3): "))
    first_card_location = int(input("Row To Play (Bottom = 1, Middle = 2, Top = 3): "))
    first_card = hand.pop(first_card_num - 1)

    print("Which card do you want to play second?")
    print(f"Cards To Play -- {hand}")
    second_card_num = int(input("Card To Play (1,2): "))
    second_card_location = int(input("Row To Play (Bottom = 1, Middle = 2, Top = 3): "))
    second_card = hand.pop(second_card_num - 1)

    print(f"Cards To Play -- {hand}")
    third_card_location = int(input("Row To Play (Bottom = 1, Middle = 2, Top = 3): "))
    third_card = hand.pop(0)

    game.playIntoHand(first_card, first_card_location - 1, second_card, second_card_location - 1, third_card, third_card_location - 1)

def print_game_state(game, hand):
    os.system('cls' if os.name == 'nt' else 'clear')
    game.print_board()


main()