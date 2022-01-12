from cards import deck
from players import player1, player2, player3, player4

class Game(object):
  def __init__(self, cards, players, small_blind_amt=.10, big_blind_amt=.20):
    self.cards = cards
    self.pot = 0
    self.table_stake = 0
    self.stake_gap = 0 
    self.card_board = []
    self.players = players.copy() # Just the list of players
    self.small_blind_amt = small_blind_amt
    self.big_blind_amt = big_blind_amt

    self.current_bet = 0 
    self.street = 'pre-flop'
    self.turn = 0

    self.positioned = players.copy() #list of players in order of position
    self.players_not_out = players.copy()
    #There can also be vars for SB/BB/Dealer name but don't think it's needed

    self.last_hand_BB_bust = False

    self.last_aggro_player = None #only needed on rivers 
    

  def __repr__(self):
    return 'We have a game!' + '\nBlinds are '+ str(self.small_blind_amt) +'/' + str(self.big_blind_amt) + '\nWith a ' + str(self.cards) + '\nand ' + str(len(self.players)) + ' players'
    #+ str(self.players)

  def start(self):
    print('game restarting')

    self.players_not_out = self.positioned.copy()

    #clear cards/roles from all players
    for player in self.players:
      player.clear_cards()
      player.special_role = None
    print('players cards/roles removed')
    

    self.cards.__init__()
    print('cards reset')

    self.cards.shuffle()
    self.deal_cards_all_players()
    self.blinds_in_roles_set()
    print('The blinds have been put in, UTG starts')
    self.next_turn()

    #current_street()

    '''for player in self.positioned: 
      print(player.cards)
    print('just for some testing/debugging^')'''

  def current_street(self):
    pass #Pre-flop 

  def next_turn(self, folded=False):
    if folded == False:
      self.turn += 1
    if self.turn == len(self.players_not_out):
      self.turn = 0
    print('\ncurrent players turn: ' + self.players_not_out[self.turn].name)

    print('stack size: ' + str(round(self.players_not_out[self.turn].current_stack, 2)))
    print('cards: ' + str(self.players_not_out[self.turn].cards))
    print("player's current stake: " + str(round(self.players_not_out[self.turn].current_stake, 2)))
    print("game's stake: " + str(self.table_stake))
    print('special_role: ' + str(self.players_not_out[self.turn].special_role))
    
    while True:
      try:
        players_input = input('what would you like to do? ')
        if (self.players_not_out[self.turn].current_stake == self.table_stake) and (players_input == 'check'):
          break
        #need to add in the other option when BB can check preflop 
        if players_input == 'fold' or players_input == 'call' or players_input == 'raise':
          break
        else:
          print('\nYour options are fold, check, call, raise')
      except:
        continue

    if players_input == 'fold':
      self.fold()
    if players_input == 'check':
      self.check()
    if players_input == 'call':
      self.call()
    if players_input == 'raise':
      raise_amt = input('What would you like to raise it to? ')
      self.raise_by(raise_amt)
    
    print('we have some input!')
    
  def next_street(self):
    pass

  def game_end(self):
    for player in self.positioned:
      if player.current_stack == 0:
        if player.special_role == 'BB':
          pass

  def change_pos_order(self, busted_special_role=None):

    self.positioned[0].special_role = None
    self.positioned[1].special_role = None
    self.positioned[-1:][0].special_role = None

    self.positioned = self.positioned[-1:] + self.positioned[:1]

    if busted_special_role != None:
      if busted_special_role == 'BB': #Special case of if BB busts
        self.positioned[0].special_role = 'BB'
        self.positioned[-1:][0].special_role = 'Btn'
        self.last_hand_BB_bust = True
      if busted_special_role == 'SB':
        self.positioned[0].special_role = 'SB'
        self.positioned[1].special_role = 'BB'
    elif self.last_hand_BB_bust:
      self.positioned[0].special_role = 'SB'
      self.positioned[1].special_role = 'BB'
      self.last_hand_BB_bust = False

    else:
      self.positioned[-1:][0].special_role = 'Btn'
      self.positioned[0].special_role = 'SB'
      self.positioned[1].special_role = 'BB'

  def deal_cards_all_players(self):
    for player in self.positioned:
      self.cards.deal(player)  

  
  def blinds_in_roles_set(self): 
    self.players_not_out[-1:][0].special_role = 'Btn'

    self.put_money_in_pot(self.small_blind_amt)
    self.players_not_out[self.turn].special_role = 'SB'
    print('\ncurrent game stake is: ' + str(self.table_stake))
    print('small blinds stake is: ' + str(self.players_not_out[self.turn].current_stake))

    print('\n going on to player 2')
    self.turn +=1
    
    #self.positioned[0].current_stack -= self.small_blind_amt 
    #self.pot += self.small_blind_amt  
    
    self.put_money_in_pot(self.big_blind_amt)
    self.players_not_out[self.turn].special_role = 'BB'
    print('\ncurrent game stake is: ' + str(self.table_stake))
    print('big blinds stake is: ' + str(self.players_not_out[self.turn].current_stake))

  def put_money_in_pot(self, amount):
    self.pot += amount
    self.table_stake = amount 
    self.players_not_out[self.turn].current_stack -= amount
    self.players_not_out[self.turn].current_stake += amount





  # Players' actions

  def fold(self):
    print(str(self.players_not_out.pop(self.turn).name) + ' folds')
    print(self.players_not_out)
    '''print('\npositioned should have all the players still ')
    print(self.positioned)'''
    self.next_turn()

  def check(self):
    print(str(self.players_not_out[self.turn]) + ' checks')
    self.next_turn()
  
  def call(self):
    self.put_money_in_pot(self.table_stake - self.players_not_out[self.turn].current_stake)
    self.next_turn()
    

  def raise_by(self, amount):
    if (amount - self.table_stake_gap) < self.stake_gap:
      raise Exception('the re-raise is not large enough')
    
    print(str(self.players_not_out[self.turn]) + ' raises to' + str(amount))
    self.put_money_in_pot(amount)
    self.next_turn()
    





  # Seeing who won 

  def highestcombo(self):
    pass 
  
  def if_flush(self):
    pass

  def if_straight(self):
    pass
  
game = Game(deck, [player1, player2, player3, player4])
