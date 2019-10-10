#! usr/local/bin/python3
'''
Created on May 28, 2019

@author:toni
'''
import os
import random as rn # will be used as a means of shuffling the deck
import tkinter as tk


assets_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 
                                             'assets/'))


class Card(object):
    '''
    This class defines a card object
    '''

    def __init__(self, suit, value): # rank, color?
        '''
        Constructor
        '''
        self.suit = suit
        self.value = value
        
    def __repr__(self):
        return ' of '.join((self.value, self.suit))
        # 'member the .join() method takes an iterable argument, therefore
        # we store the values into a tuple
        
    def get_back_file(self, cls):
        cls.back = tk.PhotoImage(file=assets_folder + "/back.png")
        return cls.back    
        
        
class Deck():
    '''Deck object.'''
    def __init__(self):
        self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts",
                      "Diamonds"] for v in ["A", "2", "3", "4", "5", "6",
                      "7", "8", "9", "10", "J", "Q", "K"]]
        # s = suit, v = value
        
    def shuffle(self):
        if len(self.cards) > 1:
            rn.shuffle(self.cards) 
            # guess shuffle does that, look the random docs
    
    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)
        # if we have a deck, we remove the last card from the deck
        # as the self.cards is a list we use pop(); removes last element
        # and returns it
    
        
class Hand():
    '''Hand object'''
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.value = 0
        
    def add_card(self, card):
        self.cards.append(card) 
        
    def calculate_value(self):
        self.value = 0
        has_ace = False
        aces = 0
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    has_ace = True
                    aces += 1
                    self.value += 11
                else:
                    self.value += 10
        if has_ace and self.value > 21:
#             if self.value-10 <= 21:
#                 self.value -= 10
#             else:
#                 self.value -= aces*10
            soft_ace = 0
            while self.value > 21 and soft_ace != aces:
                self.value -= 10
                soft_ace += 1
                
                    
    def get_value(self):
        self.calculate_value()
        return self.value
    
    def display(self):
        if self.dealer:
            print("hidden")
            print(self.cards[1])
        else:
            for card in self.cards:
                print(card)
            print("Value:", self.get_value())
            
            
class Game:
    def __init__(self):
        playing = True
        
        while playing:
            self.deck = Deck()
            self.deck.shuffle()
            
            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer=True)
            
            for i in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())
        
            print('Your hand is:')
            self.player_hand.display()
            print()
            print("Dealer's hand is:")
            self.dealer_hand.display()
            
            game_over = False
            
            while not game_over:
                player_has_blackjack, dealer_has_blackjack =\
                 self.check_for_blackjack()

                if player_has_blackjack or dealer_has_blackjack:
                    game_over = True
                    self.show_blackjack_results(player_has_blackjack, 
                                                dealer_has_blackjack)
                    continue
                
                choice = input("Please choose [Hit(h) / Stick(s)] ").lower()
                while choice not in ["h", "s", "hit", "stick"]:
                    choice = input("Please enter 'hit' or 'stick' (or h/s) ").lower()
                
                if choice in ['hit', 'h']:
                    self.player_hand.add_card(self.deck.deal())
                    print('Your hand:')
                    self.player_hand.display()
                
                    if self.player_is_over():
                        print("You have lost!")
                        game_over = True
                else:
                    self.dealer_hand.dealer = False
                    print()
                    while self.dealer_hand.get_value() < 17:
                        print("Dealer's hand:")
                        self.dealer_hand.display()
                        self.dealer_hand.add_card(self.deck.deal())
                    if self.dealer_hand.get_value() > 21:
                        self.dealer_hand.display()
                        print("You have won! The dealer is over 21.")
                        game_over = True
                        continue
                    print("Dealer's hand:")
                    self.dealer_hand.display()
                    print()
                    print("Final Results")
                    print("Your hand:", self.player_hand.get_value())
                    print("Dealer's hand:", self.dealer_hand.get_value())
                    if self.player_hand.get_value() >\
                     self.dealer_hand.get_value():
                        print("You Win!")
                    elif self.player_hand.get_value() ==\
                     self.dealer_hand.get_value():
                        print("Tie!")
                    else:
                        print("Dealer Wins!")
                    game_over = True
                
            again = input("Play Again? [Y/N] ")
            while again.lower() not in ["y", "n"]:
                again = input("Please enter Y or N ")
            if again.lower() == "n":
                print("Thanks for playing!")
                playing = False
            else:
                game_over = False
    
    
    def check_for_blackjack(self):
            player = False
            dealer = False
            if self.player_hand.get_value() == 21 and\
             len(self.player_hand.cards) == 2:
                player = True
            if self.dealer_hand.get_value() == 21 and\
             len(self.dealer_hand.cards) == 2:
                dealer = True
            return player, dealer
        
        
    def show_blackjack_results(self, player_has_blackjack,
                           dealer_has_blackjack):
        if player_has_blackjack and dealer_has_blackjack:
            print("Both players have blackjack! Draw!")
        elif player_has_blackjack:
            print("You have blackjack! You win!")
        elif dealer_has_blackjack:
            print("Dealer's hand:")
            self.dealer_hand.dealer = False
            self.dealer_hand.display()
            print("Dealer has blackjack! Dealer wins!")
            
            
    def player_is_over(self):
        return self.player_hand.get_value() > 21
            
        
def main():
    game = Game()


if __name__ == '__main__':
    main()