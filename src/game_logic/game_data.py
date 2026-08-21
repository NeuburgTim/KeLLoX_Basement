"""
party, gold, inventory. One GameData instance is created in
GameApp and handed to every screen through app.game_data.
"""


class GameData:

    def __init__(self):
        self.party = []       # list[Character]
        self.gold = 0
        self.inventory = {}   # item name -> quantity

    def add_gold(self, amount):
        self.gold = max(0, self.gold + amount)

    def add_item(self, item_name, quantity=1):
        self.inventory[item_name] = self.inventory.get(item_name, 0) + quantity

    def remove_item(self, item_name, quantity=1):
        if self.inventory.get(item_name, 0) < quantity:
            raise ValueError(f"Not enough '{item_name}' in inventory")
        self.inventory[item_name] -= quantity
        if self.inventory[item_name] == 0:
            del self.inventory[item_name]

    def get_living_party(self):
        return [character for character in self.party if character.is_alive()]
