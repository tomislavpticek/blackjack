import assets
import random
import art
from replit import clear

def generate_pool_of_cards (deck_of_cards, number_of_decks):

  pool_of_cards = []
  
  for deck_number in range(0, number_of_decks):
    tmp_deck = deck_of_cards.copy()
    for card in range(0, len(tmp_deck)):
      pool_of_cards.append(tmp_deck.pop(random.randint(0,len(tmp_deck)-1)))

  return pool_of_cards

def deal_card (pool_of_cards):
  return pool_of_cards.pop()

def place_bet(players):
  bet = 0
  while bet <= 0 or bet > players["player1"]["money"]:
    bet = int(input("Place your  bet: "))
    if(bet <= 0):
      print("Bet too small, try again.")
    elif(bet > player1["money"]):
      print("You dont have enough funds for a bet this size")
  players["player1"]["bet"] += bet    
  players["player1"]["money"] -= bet

      
def start_game(players, pool_of_cards):

  clear()
  print (art.logo)
  
  print(f"Available money: {players['player1']['money']}\n")

  place_bet(players)
  
  for player in players:
    players[player]["cards"] = []
  
  for player in players:
    for cards in range(0, 2):
      players[player]["cards"].append(deal_card(pool_of_cards))

def calculate_hand_size(player):
  count = 0

  for card in player["cards"]:
    if(card["name"] != "CA" and card["name"] != "DA" and card["name"] != "HA" and card["name"] != "SA"):
      count += card["value"]
      #print(f"Card: {card}")
      #print(f"Regular card count: {count}")

  for card in player["cards"]:
    if(card["name"] == "CA" or card["name"] == "DA" or card["name"] == "HA" or card["name"] == "SA"):
      if(count+11 > 21):
        count += 1
      else:
        count += 11
     #print(f"Card: {card}")
     #print(f"Speclial card count: {count}")
  
  return count

pool_of_cards = generate_pool_of_cards(assets.alt_deck_of_cards, 6)

def reset_screen(players, reveal_dealers_hand):

  clear()
  print (art.logo)
  
  print(f"Available money: {players['player1']['money']}\n")

  print(f"Bet: {players['player1']['bet']}\n")

  if(reveal_dealers_hand):
    for player in players:
      if(player == "dealer"):
        print("Dealer: ", end="")
        for card in players[player]["cards"]:
          print (f"[{card['name']}] ", end="")
        print("\n")
  else:
    print("Dealer: ", end="")
    print(f"[{players['dealer']['cards'][0]['name']}] X\n")
  
  for player in players:
    if(player != "dealer"):
      print("Guest: ", end="")
      for card in players[player]["cards"]:
        print (f"[{card['name']}] ", end="")
      print("\n")
   
      
player1 = {
  "cards": [],
  "money": 300,
  "bet": 0
}

dealer = {
  "cards": [],
  "money": 300000000000,
  "bet": 0
}

players = {"dealer": dealer, "player1": player1}

while True:

  start_game(players=players, pool_of_cards=pool_of_cards)
  
  
  while True:
  
    reset_screen(players, False)
    
    action = input("Hit (h) or stand (s): ")
  
    if (action == "h"):
      players["player1"]["cards"].append(deal_card(pool_of_cards))
  
  
      if(calculate_hand_size(players["player1"]) > 21):
        players["player1"]["bet"] = 0
        reset_screen(players, True)
  
        print("Over 21, You lose.")
        break
      
  
    elif(action == "s"):
  
      
  
      #print(f"{players['dealer']['cards'][0]['name']}, {players['dealer']['cards'][1]['name']}")
      while (calculate_hand_size(players["dealer"]) <= 16):
        players["dealer"]["cards"].append(deal_card(pool_of_cards))
        
  
      if(calculate_hand_size(players["dealer"]) > 21):
        players["player1"]["money"] += players["player1"]["bet"]*2
        players["player1"]["bet"] = 0
        reset_screen(players, True)
        print(f"Dealers {calculate_hand_size(players['dealer'])} vs your {calculate_hand_size(players['player1'])}")
        print("You win.")
        break
      
      elif(calculate_hand_size(players["dealer"]) > calculate_hand_size(players["player1"])):
        players["player1"]["bet"] = 0
        reset_screen(players, True)
        print(f"Dealers {calculate_hand_size(players['dealer'])} vs your {calculate_hand_size(players['player1'])}")
        print("Dealer wins.")
        break
  
      elif(calculate_hand_size(players["dealer"]) < calculate_hand_size(players["player1"])):
        players["player1"]["money"] += players["player1"]["bet"]*2
        players["player1"]["bet"] = 0
        reset_screen(players, True)
        print(f"Dealers {calculate_hand_size(players['dealer'])} vs your {calculate_hand_size(players['player1'])}")
        print("You win.")
        break
  
      elif(calculate_hand_size(players["dealer"]) == calculate_hand_size(players["player1"])):
        players["player1"]["money"] += players["player1"]["bet"]
        players["player1"]["bet"] = 0
        reset_screen(players, True)
        print(f"Dealers {calculate_hand_size(players['dealer'])} vs your {calculate_hand_size(players['player1'])}")
        print("Draw.")
        break
  
  cont = input("Continue n/y: ")
  
  if(cont=="n"):
    print("Thank you for playing, goodbye.")
    break
  else:
    if players["player1"]["money"] == 0:
      print("Insufficient funds to keep playing, please deposit more funds in the account.\nUntil then, goodbye.")
      break