"""
TextTown is an interactive text-based RPG set within a medieval town.
December 7, 2021
Henry Ding
"""
from game import *

class Player:
    def __init__(self, location, stamina, balance):
        self.location = location
        self.stamina = stamina
        self.balance = balance

    # learned from Choate Programming Union Meeting
    def __str__(self):
        return self.location + " " + str(self.stamina) + " " + str(self.balance)


player = Player("house", 0.0, 0)
game = Game(player, "playing")

running = True
while running:
    game.loop()
