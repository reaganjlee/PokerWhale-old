from cards import *
from players import player1, player2, player3, player4
#from winner_calculator import calc
from collections import Counter

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
    self.street = 'Pre-flop'
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
    if len(self.players_not_out) == 1:
      self.game_end()

    if folded == False:
      self.turn += 1
    if (self.street == 'Pre-flop') and (self.turn == len(self.players_not_out)):
      self.turn = 0
    if (self.street != 'Pre-flop') and (self.turn == len(self.players_not_out)):
      self.next_street()
    if (self.street != 'Done'):
      print('\nThe current turn number is: ' + str(self.turn) + '\n')
      


      print('\ncurrent players turn: ' + self.players_not_out[self.turn].name)

      print('stack size: ' + str(round(self.players_not_out[self.turn].current_stack, 2)))
      print('cards: ' + str(self.players_not_out[self.turn].cards))
      print("player's current stake: " + str(round(self.players_not_out[self.turn].current_stake, 2)))
      print("game's stake: " + str(self.table_stake))
      print("game's current pot size: " + str(round(self.pot, 2)))
      print('special_role: ' + str(self.players_not_out[self.turn].special_role))
      
      while True:
        try:
          players_input = input('what would you like to do? ')
          if (self.players_not_out[self.turn].current_stake == self.table_stake) and (players_input == 'check'):
            break
          elif (players_input == 'check'):
            print('\nYour options are fold, call, raise')

          elif (self.players_not_out[self.turn].current_stake == self.table_stake) and (players_input == 'call'): #When its BB
            print('\nYour options are fold, check, raise')

          elif players_input == 'fold' or players_input == 'call' or players_input == 'raise':
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
      

      if (self.street == 'Pre-flop') and (self.turn == 1): #can't put this up front because BB has to go during pre-flop
        self.next_street()

      else:
        if players_input == 'fold':
          self.next_turn(True)
        else:
          self.next_turn()
    
  def next_street(self):
    print('\n\n we got it!\n\n')
    
    if self.street == 'River':
      self.game_end()
    else:
      if self.street == 'Turn':
        self.street = 'River'
        self.cards.deal(self.card_board)
      if self.street == 'Flop':
        self.street = 'Turn'
        self.cards.deal(self.card_board) 
      if self.street == 'Pre-flop':
        self.street = 'Flop'
        self.cards.deal(self.card_board, 3)  
      

      print('The current street is: ' + str(self.street))
      print(self.card_board)

      self.turn = -1
      self.table_stake = 0
      self.stake_gap = 0 
      self.current_bet = 0 

      for player in self.positioned:
        player.current_stake = 0

    

    self.next_turn()


  def game_end(self): #calculates the winner and gives the pot to the correct player, also uses a smaller function to calculate side-pots 
  
  #so ways to get to this function, you get to the river, or everyone folds i.e. only one player left in players_not_out 
    print('\n\n Game ends!\n\n')
    if len(self.players_not_out) == 1:
      print('When folding down, the winner is: ' + str(self.players_not_out[0]))
    self.street = 'Done'

    
    #for player in self.positioned:
     # if player.current_stack == 0:
      #  if player.special_role == 'BB':
       #   pass

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
      self.cards.deal(player.cards, 2)  

  
  def blinds_in_roles_set(self): 
    self.players_not_out[-1:][0].special_role = 'Btn'

    self.put_money_in_pot(self.small_blind_amt)
    self.table_stake = self.small_blind_amt
    self.players_not_out[self.turn].special_role = 'SB'
    print('\ncurrent game stake is: ' + str(self.table_stake))
    print('small blinds stake is: ' + str(self.players_not_out[self.turn].current_stake))

    print('\n going on to player 2')
    self.turn +=1
    
    #self.positioned[0].current_stack -= self.small_blind_amt 
    #self.pot += self.small_blind_amt  
    
    self.put_money_in_pot(self.big_blind_amt)
    self.table_stake = self.big_blind_amt
    self.players_not_out[self.turn].special_role = 'BB'
    print('\ncurrent game stake is: ' + str(self.table_stake))
    print('big blinds stake is: ' + str(self.players_not_out[self.turn].current_stake))

  def put_money_in_pot(self, amount):
    self.pot += amount
    self.players_not_out[self.turn].current_stack -= amount
    self.players_not_out[self.turn].current_stake += amount





  # Players' actions

  def fold(self):
    print(str(self.players_not_out.pop(self.turn).name) + ' folds')
    print(self.players_not_out)
    '''print('\npositioned should have all the players still ')
    print(self.positioned)'''

  def check(self):
    print(str(self.players_not_out[self.turn]) + ' checks')
  
  def call(self):
    self.put_money_in_pot(self.table_stake - self.players_not_out[self.turn].current_stake)
    

  def raise_by(self, amount):
    if (amount - self.table_stake_gap) < self.stake_gap:
      raise Exception('the re-raise is not large enough')
    
    print(str(self.players_not_out[self.turn]) + ' raises to' + str(amount))
    self.put_money_in_pot(amount)
    self.table_stake = amount 
    





  #calculating the winner 

  def checker(self, player):
    player_nums = self.player_nums(player)

    if_pair = self.if_pair(player_nums)
    print(str(if_pair))

    print('\nseparator flush below\n')
    if_flush = self.if_flush(player1)
    print(str(if_flush))

    print('\nseparator set below\n')
    if_set = self.if_set(player_nums)
    print(str(if_set))

    print('\nseparator quads below\n')
    if_quads = self.if_quads(player_nums)
    print(str(if_quads))

  
  def player_nums(self, player):
    lst = self.card_board.copy()
    for card in player.cards:
      lst.append(card)
    print(str(lst))
    print(lst[0].suit)

    lst_of_nums = []
    for item in lst:
      lst_of_nums.append(item.number)
    print(lst_of_nums)

    #cnt = Counter(lst_of_nums)
    #count_list = [k for k, v in cnt.iteritems() if v > 1]
    #[num for num in lst_of_nums if lst_of_nums.count(num)>1]
    
    __ = []
    for num in lst_of_nums:
      if lst_of_nums.count(num) > 1:
        __.append([num, lst_of_nums.count(num)])
    
    count_lst = []
    for num in __:
      if num not in count_lst:
        count_lst.append(num)

    '''count_lst = []
    for num in lst_of_nums:
      if lst_of_nums.count(num) > 1:
        count_lst.append([num, lst_of_nums.count(num)])'''
        
    print(str(count_lst))
    return count_lst 

    

  def if_pair(self, player_nums):
    #player_nums = self.player_nums(player)
    lst_of_pairs = [item for item in player_nums if item[1] == 2]
    print('\nlst_of_pairs I think works!\n')
    if lst_of_pairs:
      #print('before sorting')
      #print(str(result))
      #print('\nafter sorting:')
      lst_of_pairs.sort(key = lambda item: item[0], reverse = True)

      print(str([True, lst_of_pairs]))
      return [True, lst_of_pairs]

    
  
  def if_set(self, player_nums):
    lst_of_sets = [item for item in player_nums if item[1] == 3]
    print('\n think this works for the if_set function!\n')
    if lst_of_sets:
      lst_of_sets.sort(key = lambda item: item[0], reverse = True) #Pretty sure that there are no two sets possible so this line isn't needed but idk fs and I don't want this to break xd 

      print(str([True, lst_of_sets]))
      return [True, lst_of_sets]
    
  def if_quads(self, player_nums):
    lst_of_quads = [item for item in player_nums if item[1] == 4]
    print('\n think this works for the if_quads function!\n')
    if lst_of_quads:
      lst_of_quads.sort(key = lambda item: item[0], reverse = True) #Pretty sure that there are no two sets possible so this line isn't needed but idk fs and I don't want this to break xd 

      print(str([True, lst_of_quads]))
      return [True, lst_of_quads]
  def highestcombo(self):
    pass 
  
  def if_flush(self, player):
    lst = self.card_board.copy()
    for card in player.cards:
      lst.append(card)
    print(str(lst))
    print(lst[0].suit)

    lst_of_suits = []
    for itm in lst:
      lst_of_suits.append(itm.suit)
    print(lst_of_suits)

    suit_list = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
    for suit in suit_list:
      if lst_of_suits.count(suit) >= 5:
        print(str(suit))
        print('We have a flush!')
        return True 
    print('no flush!')
    return False

    #print('Hearts count: ' + str(lst_of_suits.count('Hearts')))
    #print('Diamonds count: ' + str(lst_of_suits.count('Diamonds')))
    #print('Clubs count: ' + str(lst_of_suits.count('Clubs')))
    #print('Spades count: ' + str(lst_of_suits.count('Spades')))

    #if lst.count(lst.suit):
    

    '''suit_lst = []
    __ = []
    for item in lst_of_suits:
      if lst_of_suits.count(num) > 1:
        __.append([num, lst_of_suits.count(num)])
    
    count_lst = []
    for num in __:
      if num not in count_lst:
        count_lst.append(num)'''


  def if_straight(self):
    pass
  
game = Game(deck, [player1, player2, player3, player4])
#game.cards.shuffle()
#game.cards.deal(game.card_board, 5)

test_card = Card(3, '3', 'Hearts')
test_card.showing = True
game.card_board.append(test_card)

test_card = Card(3, '3', 'Hearts')
test_card.showing = True
game.card_board.append(test_card)

test_card = Card(3, '3', 'Hearts')
test_card.showing = True
game.card_board.append(test_card)

test_card = Card(5, '5', 'Hearts')
test_card.showing = True
game.card_board.append(test_card)

test_card = Card(7, '7', 'Hearts')
test_card.showing = True
game.card_board.append(test_card)
 
print(str(game.card_board))

print('\nThe players cards are: ')
game.deal_cards_all_players()
for player in game.positioned:
  print(str(player.cards))


print('\n')
game.player_nums(player1)

print('\n\nIf there is a pair there should be text')
game.checker(player1)