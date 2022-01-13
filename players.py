class Player(object):
  def __init__(self, name, starting_stack=0):
    self.name = name
    self.cards = []
    self.current_stack = starting_stack
    self.current_stake = 0 
    self.special_role = None #This is needed in the case of when BB leaves the table
    self.all_in = False
  
  def __repr__(self):
    return str(self.name)#"starting stack: " + str(self.starting_stack) + "\ncards: " + str(self.cards)
    

  def clear_cards(self):
    self.cards = []

  def cardcount(self):
    return len(self.cards)

  

player1 = Player('player1', 10.50)
player2 = Player('player2', 20.50)
player3 = Player('player3', 30.50)
player4 = Player('player4', 40.50)