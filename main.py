import random

class Card(object):
    def __init__(self, value, name, suit):
        self.value = value
        self.suit = suit
        self.name = name 
        self.showing = False
    def __repr__(self):
        if self.showing:
          return str(self.name) + " of " + str(self.suit)
        return "Card"

class Deck(object):
  def shuffle(self, times=1):
      random.shuffle(self.cards)
      print('shuffled')
    
  def deal(self, numofcards=2):
    given_hand = []
    for num in range(numofcards):
      given_hand.append(self.cards.pop(0))
    for i in given_hand:
      i.showing = True 
    return given_hand

class StandardDeck(Deck):
    def __init__(self):
      self.cards = []
      suits = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
      values = {
          "Two": 2,
          "Three": 3,
          "Four": 4,
          "Five": 5,
          "Six": 6,
          "Seven": 7,
          "Eight": 8,
          "Nine": 9,
          "Ten": 10,
          "Jack": 11,
          "Queen": 12,
          "King": 13,
          "Ace": 14}

      for name in values:
          for suit in suits:
              self.cards.append(Card(values[name], name, suit))
    
    def __repr__(self):
      return "standard deck of cards with {0} remaining".format(len(self.cards))

    