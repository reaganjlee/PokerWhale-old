import random

class Card(object):
    def __init__(self, number, name, suit):
        self.number = number
        self.suit = suit
        self.name = name 
        self.showing = False
        
        #self.player_nums = []
    def __repr__(self):
        suit_symbols = {
          "Hearts": '♥',
          "Spades": '♠',
          "Clubs": '♣',
          "Diamonds": '♦'
        }
        if self.showing:
          return str(self.name) + suit_symbols[self.suit]#str(self.suit)
        return "Card"

class Deck(object):
  def shuffle(self, times=1):
      random.shuffle(self.cards)
      print('shuffled')
    
  def deal(self, location, numofcards=1):
    #given_hand = []
    for num in range(numofcards):
      location.append(self.cards.pop(0))
    for i in location:
      i.showing = True 
    return location
  
  #def deal_specific(self, location, specific_card):
  #  location.append(Card(values[name], name, suit))
  # you can just a new object, have a string that says like Ace of Hearts and use that to make a new object then delete the old object from the deck, though its too much work for rn 

class StandardDeck(Deck):
    def __init__(self):
      self.cards = []
      suits = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
      values = {
          "2": 2,
          "3": 3,
          "4": 4,
          "5": 5,
          "6": 6,
          "7": 7,
          "8": 8,
          "9": 9,
          "10": 10,
          "J": 11,
          "Q": 12,
          "K": 13,
          "A": 14}

      for name in values:
          for suit in suits:
              self.cards.append(Card(values[name], name, suit))
    
    def __repr__(self):
      return "standard deck of cards with {0} remaining".format(len(self.cards))

deck = StandardDeck()

    