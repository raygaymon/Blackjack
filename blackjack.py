from random import shuffle

VALUES = {"2" : 2, "3": 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7, "8" : 8, "9" : 9, "10" : 10, "Jack" : 10, "Queen" : 10, "King" : 10, "Ace" : 11}
SUITS = ("Diamond", "Clubs", "Hearts", "Spades")
RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace")

class Card():

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = VALUES[rank]

    def __str__(self):
        return (f"{self.rank} of {self.suit}")

class Deck(Card):

    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                c = Card(r, s)
                self.deck.append(c)
        
        shuffle(self.deck)
    
    def __str__ (self):
        return (f"Deck now has {len(self.deck)} cards")

    def deal(self):
        return self.deck.pop()

class Player():

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.value = 0
        self.bet = 0
        self.budget = 10000
        self.have_ace = False

    # to return players' hand values
    def hand_value(self):
        res = 0
        for c in self.hand:
            res += c.value
        self.value = res
    
    def __str__(self):
        return (f"Player {self.name} has a total value of {self.value()}")

    def take_card(self, c):
        self.hand.append(c)

    # to place bets
    def place_bet(self):
        bet = 0
        while True:
            try:
                bet = int(input(f"How much do you want to bet {self.name}: "))
            except ValueError:
                print("Please only enter valid numbers. ")
            except SyntaxError:
                print("Please enter something. ")
            else:
                if bet > self.budget:
                    print(f"You can't afford that bet {self.name}. You only have ${self.budget}.")
                else:
                    print(f"Bet of ${bet} successfully placed.")
                    self.bet = bet
                    self.budget -= bet
                    break
    
    def display_hand(self):
        print(f"{self.name}'s hand has: ")
        for c in self.hand:
            print(c)

def deal_cards(players, deck):

    for i in range(2):
        for p in players:
            c = deck.deal()
            if c.rank == "Ace":
                p.have_ace = True
            p.take_card(c)
    
    for p in players:
        p.hand_value()

def get_players():
    players = []

    name = "-"

    while name != "done":

        if name != "-":
            p = Player(name.capitalize())
            players.append(p)

        name = input(f"Please enter your name player {len(players) + 1} (Enter 'done' when all players have entered their names): ")
    
    # add dealer into list of players since dealer also needs to take cards in deal() function
    dealer = Player("dealer")
    players.append(dealer)
    
    return players

def hit (player, deck):

    action = ""

    # check for blackjack or double ace here
    if player.value >= 21:
        print(f"Yay {player.name} got a blackjack! You win ${player.bet * 2}")
        player.budget += player.bet * 3
        player.bet = 0
        return

    while len(player.hand) < 5:

        player.display_hand()

        # check if the player has gone over and if they have an ace - if they have an ace then they can change it into a 1
        if player.value > 21 and not player.have_ace:
            print(f"You went over 21 at {player.value}. Let's hope the dealer goes over too.")
            break
        elif player.have_ace and player.value > 21:
            player.value -= 10
            player.have_ace = False
        
        action = input(f"{player.name}, do you want to take another card? Current value of hand: {player.value} (y/n) : ").upper()

        if action != 'Y' and action != 'N':
            print("Please only enter y or n.")
        elif action == 'Y':
            c = deck.deal()
            if c.rank == "Ace":
                player.have_ace = True
            player.take_card(c)
            player.hand_value()
            print(f"You got the {c}.")
        else:
            print("Next player.")
            break
    
    if len(player.hand) == 5:
        print(f"{player.name} has reached the hand size limit of 5. Current value: {player.value}")
        
def check_win(dealer, players):

    d = dealer.value
    for p in players:

        # skip blackjacked players
        if p.bet == 0 or p.name == 'dealer':
            continue

        # check for over 21 situations - separated over 21 situations and under 21 situations to prevent potential issues

        # dealer and player go over
        if p.value > 21 and d > 21:
            p.budget += p.bet
            print(f"Dealer also went over 21. {p.name} gets back their bet of ${p.bet}")
            p.bet = 0

        # dealer over player under
        elif d > 21 and p.value < 21:
            p.budget += p.bet * 2
            print(f"Congratulations {p.name} for winning. You win ${p.bet * 2}")
            p.bet = 0
        
        # player over dealer under
        elif d < 21 and p.value > 21:
            p.bet = 0
            print(f"Sorry for your loss {p.name}. Better luck next round.")
            
        # both are under
        else:
            if d == p.value:
                p.budget += p.bet 
                print(f"{p.name} had a draw. You get back your bet of ${p.bet}")
                p.bet = 0
                
            elif d < p.value:
                p.budget += p.bet * 2
                print(f"Congratulations {p.name} for winning. You win ${p.bet * 2}")
                p.bet = 0
                
            else:
                p.bet = 0
                print(f"Sorry for your loss {p.name}. Better luck next round.")
            

def game():

    # take in players
    players = get_players()

    # to allow players to keep going
    keep_playing = True

    while keep_playing:
        # create deck
        deck = Deck()

        # get player bets
        for p in players:
            if p.name == 'dealer':
                continue
            p.place_bet()

        # since dealer is added last when getting players in get_players() function, dealer will always be the last player
        deal_cards(players, deck)

        # pop dealer out of player list to avoid checking if dealer won against dealer
        dealer = players[-1]

        # show one face up for casino rules
        print(f"Dealer has a {dealer.hand[0]} face up. ")

        # dealing cards to players
        for p in players:
            if p.name == 'dealer':
                continue
            hit(p, deck)
            
        
        print(f"Dealer's turn now.")
        dealer.display_hand()
        
        # make sure dealer's hand value is > 17 - casino rules..?
        while dealer.value < 17 and len(dealer.hand) < 5:
            c = deck.deal()

            # check if dealer got ace from draw after not getting ace
            if c.rank == "Ace":
                dealer.have_ace = True

            dealer.take_card(c)
            dealer.hand_value()

            # only minus 10 once - using ace_deducted to check for deduction
            if dealer.value > 21 and dealer.have_ace:
                dealer.value -= 10
                dealer.have_ace = False
            
            dealer.display_hand()
            print(f"Dealer's hand value is now: {dealer.value}")
        
        check_win(dealer, players)

        # to check if players want to keep playing
        while True:
            still_play = input("Do you want to keep playing? (Y/N): ").upper()

            if still_play != "Y" and still_play != "N":
                print("Please input Y or N only")

            elif still_play == "N":
                keep_playing = False
                print("Gambling is bad for you. Bye bye.")
                break
            else:
                print("Alright we keep going.")
                for p in players:
                    p.hand.clear()
                break
        

if __name__ == "__main__":
    print("Welcome to Blackjack, where dreams go to die.")
    game()
    

