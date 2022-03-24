#! usr/local/bin/python3
'''
Created on May 28, 2019

@author:toni
'''
import os
import random as rn
import tkinter as tk

assets_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'assets/Cards/Classic/'))


class Card():
    """This class defines a card object."""

    def __init__(self, suit, value):  # rank, color?
        """
        Constructor
        """
        self.suit = suit
        self.value = value
        self.img = tk.PhotoImage(file=assets_folder + '/' + self.suit
                                 + self.value + ".png")

    def __repr__(self):
        # 'member the .join() method takes an iterable argument, therefore we
        # store the values into a tuple.
        return ' of '.join((self.value, self.suit))

    def get_file(self):
        return self.img

    # Class methods don't require an instance of the class to work.
    @classmethod
    def get_back_file(cls):
        cls.back = tk.PhotoImage(file=assets_folder + "/back.png")
        return cls.back


class Deck():
    """Deck object."""

    def __init__(self):
        # s = suit, v = value
        self.cards = [Card(s, v) for s in ["s", "c", "h",
                      "d"] for v in ["01", "02", "03", "04", "05", "06",
                      "07", "08", "09", "10", "11", "12", "13"]]
#                    [Card(s, v) for s in ["Spades", "Clubs", "Hearts",
#                    "Diamonds"] for v in ["A", "2", "3", "4", "5", "6",
#                    "7", "8", "9", "10", "J", "Q", "K"]]

    def shuffle(self):
        if len(self.cards) > 1:
            rn.shuffle(self.cards)

    def deal(self):
        # If we have a deck, we remove the last card from the deck. As the
        # self.cards object is a list we use pop() to remove the last element
        # and return it. If there are no cards left, we return None.
        if len(self.cards) > 1:
            return self.cards.pop(0)
        return None


class Hand():
    """Hand object."""

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
            soft_ace = 0
            while self.value > 21 and soft_ace != aces:
                self.value -= 10
                soft_ace += 1

    def get_value(self):
        self.calculate_value()
        return self.value


class GameState:

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand = Hand()
        self.dealer_hand = Hand(dealer=True)

        for i in range(2):
            self.player_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())

        self.has_winner = ''

    def player_is_over(self):
        return self.player_hand.get_value() > 21

    def someone_has_blackjack(self):
        player = False
        dealer = False
        if (self.player_hand.get_value() == 21 and
                len(self.player_hand.cards) == 2):
            player = True
        if (self.dealer_hand.get_value() == 21 and
                len(self.dealer_hand.cards) == 2):
            dealer = True

        if player and dealer:
            return 'dp'
        if player:
            return 'p'
        if dealer:
            return 'd'

        return False

    def hit(self):
        self.player_hand.add_card(self.deck.deal())
        if self.someone_has_blackjack() == 'p':
            self.has_winner = 'p'
        if self.player_is_over():
            self.has_winner = 'd'

        return self.has_winner

    def get_table_state(self):
        blackjack = False
        winner = self.has_winner
        if not winner:
            winner = self.someone_has_blackjack()
            if winner:
                blackjack = True
        table_state = {
            'player_cards': self.player_hand.cards,
            'dealer_cards': self.dealer_hand.cards,
            'has_winner': winner,
            'blackjack': blackjack,
        }

        return table_state

    def calculate_final_state(self):
        player_hand_value = self.player_hand.get_value()
        dealer_hand_value = self.dealer_hand.get_value()

        if player_hand_value == dealer_hand_value:
            winner = 'dp'
        elif player_hand_value > dealer_hand_value:
            winner = 'p'
        else:
            winner = 'd'

        table_state = {
            'player_cards': self.player_hand.cards,
            'dealer_cards': self.dealer_hand.cards,
            'has_winner': winner,
        }

        return table_state

    def player_score_as_text(self):
        return "Score: " + str(self.player_hand.get_value())


class GameScreen(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Blackjack")
        self.geometry("800x640")
        self.resizable(False, False)

        self.CARD_ORIGINAL_POSITION = 100
        self.CARD_WIDTH_OFFSET = 100

        self.PLAYER_CARD_HEIGHT = 300
        self.DEALER_CARD_HEIGHT = 100

        self.PLAYER_SCORE_TEXT_COORDS = (400, 450)
        self.WINNER_TEXT_COORDS = (400, 250)

        self.game_state = GameState()
        self.game_screen = tk.Canvas(self, bg="white", width=800, height=500)

        self.bottom_frame = tk.Frame(self, width=800, height=140, bg="red")
        # Force the size of the frame widget, otherwise the size will adjust
        # to account for other widgets on the frame (frame child widgets).
        self.bottom_frame.pack_propagate(0)

        self.hit_button = tk.Button(self.bottom_frame, text='Hit', width=25,
                                    command=self.hit)
        self.stick_button = tk.Button(self.bottom_frame, text='Stick',
                                      width=25, command=self.stick)

        self.play_again_button = tk.Button(self.bottom_frame,
                                           text='Play Again', width=25,
                                           command=self.play_again)
        self.quit_button = tk.Button(self.bottom_frame, text='Quit', width=25,
                                     command=self.destroy)

        self.hit_button.pack(side=tk.LEFT, padx=(100, 200))
        self.stick_button.pack(side=tk.LEFT)

        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.game_screen.pack(side=tk.LEFT, anchor=tk.N)

        self.display_table()

    def display_table(self, hide_dealer=True, table_state=None):
        if not table_state:
            table_state = self.game_state.get_table_state()

        player_card_images = [card.get_file() for card in
                              table_state['player_cards']]
        dealer_card_images = [card.get_file() for card in
                              table_state['dealer_cards']]
        if hide_dealer and not table_state['blackjack']:
            dealer_card_images[0] = Card.get_back_file()

        self.game_screen.delete('all')
        self.tabletop_image = tk.PhotoImage(file=assets_folder
                                            + '/tabletop.png')

        self.game_screen.create_image((400, 250), image=self.tabletop_image)

        for card_number, card_image in enumerate(player_card_images):
            self.game_screen.create_image(
                (self.CARD_ORIGINAL_POSITION + self.CARD_WIDTH_OFFSET *
                 card_number, self.PLAYER_CARD_HEIGHT),
                image=card_image.subsample(1, 1))

        for card_number, card_image in enumerate(dealer_card_images):
            self.game_screen.create_image(
                (self.CARD_ORIGINAL_POSITION + self.CARD_WIDTH_OFFSET *
                 card_number, self.DEALER_CARD_HEIGHT),
                image=card_image.subsample(1, 1))

        self.game_screen.create_text(
            self.PLAYER_SCORE_TEXT_COORDS,
            text=self.game_state.player_score_as_text(),
            font=(None, 20))

        if table_state['has_winner']:
            if table_state['has_winner'] == 'p':
                self.game_screen.create_text(
                    self.WINNER_TEXT_COORDS,
                    text="YOU WIN!", font=(None, 50))
            elif table_state['has_winner'] == 'dp':
                self.game_screen.create_text(
                    self.WINNER_TEXT_COORDS,
                    text="TIE!", font=(None, 50))
            else:
                self.game_screen.create_text(
                    self.WINNER_TEXT_COORDS,
                    text="DEALER WINS!", font=(None, 50))

            self.show_play_again_options()

    def show_play_again_options(self):
        self.hit_button.pack_forget()
        self.stick_button.pack_forget()

        self.play_again_button.pack(side=tk.LEFT, padx=(100, 200))
        self.quit_button.pack(side=tk.LEFT)

    def show_gameplay_buttons(self):
        self.play_again_button.pack_forget()
        self.quit_button.pack_forget()

        self.hit_button.pack(side=tk.LEFT, padx=(100, 200))
        self.stick_button.pack(side=tk.LEFT)

    def play_again(self):
        self.show_gameplay_buttons()
        self.game_state = GameState()
        self.display_table()

    def hit(self):
        self.game_state.hit()
        self.display_table()

    def stick(self):
        table_state = self.game_state.calculate_final_state()
        self.display_table(False, table_state)


def main():
    gs = GameScreen()
    gs.mainloop()


if __name__ == '__main__':
    main()
