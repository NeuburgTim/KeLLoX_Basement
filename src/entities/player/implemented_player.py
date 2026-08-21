class Character:

    def __init__(self, name, max_hp, attack, defense, level=1, xp=0):
        self.name = name
        self.level = level
        self.xp = xp
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defense = defense

    def is_alive(self):
        return self.current_hp > 0

    def heal(self, amount):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def take_damage(self, amount):
        self.current_hp = max(0, self.current_hp - amount)

    def gain_xp(self, amount):
        self.xp += amount
