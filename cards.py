import random

class Card(object):
    def __init__(self, number, name, suit):
        self.number = number
        self.suit = suit
        self.name = name 
        self.showing = False
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
    
  def deal(self, location, numofcards=2):
    #given_hand = []
    for num in range(numofcards):
      location.cards.append(self.cards.pop(0))
    for i in location.cards:
      i.showing = True 
    return location

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

    