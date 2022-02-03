class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
    
    def play(self, current_gamedeck_color, current_gamedeck_number):
        print(f"Your cards are:")
        for index, card in enumerate(self.deck):
            if index == 0: 
                print(f"{index + 1} {card}", end=", ")
            elif index == len(self.deck) - 1:
                print(f"{index + 1} {card}")
            else:
                print(f"{index + 1} {card}", end=", ")
        print("What card do you want to play? If none of your cards are playable type P to pick up a card!")
        while True:
            response = input("> ")
            try:
                response = int(response)
                response -= 1
                chosen_card = self.deck[response]
            except ValueError as e:
                if response == "P":
                    self.take_card() 
                else:
                    continue 
            if not response <= len(self.deck) - 1:
               print("Not a valid card")
               continue
            elif chosen_card[0] == "black":  # Black cards can be played regardless 
                print(f"Played {chosen_card}")
                return response, chosen_card
            elif current_gamedeck_color is None and current_gamedeck_number is None:
                print(f"Played {chosen_card}")
                return response, chosen_card 
            elif chosen_card[0] != current_gamedeck_color and chosen_card[1] != current_gamedeck_number:  # Check if card has the same number or color as current played card
                print("The card you chose is not playable!")
            else:
                print(f"Played {chosen_card}")
                return response, chosen_card
                
    def take_card(self, deck):
        self.deck.append(deck.pop())
    
    def remove_card(self, index):
        card = self.deck.pop(index)
        return card 
    
    def __repr__(self):
        return self.name 
 