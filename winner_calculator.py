#from cards import deck 
#from players import player1, player2, player3, player4
from main import game
print('this loaded 1')

game.card_board = []
game.deck.shuffle()
game.deck.deal(game.card_board, 5)
print(str(game.card_board))
print('this loaded')


class win_calculator(object):
  def __init__(self, card_board, players):
    self.card_board = card_board
    self.players = players
  

  # Seeing who won
  def if_pair(self):
    pass
  def highestcombo(self):
    pass 
  
  def if_flush(self):
    pass

  def if_straight(self):
    pass

calc = win_calculator(game.board, game.players)