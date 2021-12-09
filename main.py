"""
TextTown is an interactive text-based RPG set within a medieval town.
December 7, 2021
Henry Ding
"""
from game import *


class Player:
    def __init__(self):
        self.location = "house"
        self.stamina = 100
        self.balance = 0
        self.grain = 100
        self.house_tier = 0

    # learned from Choate Programming Union Meeting
    def __str__(self):
        return self.location + " " + str(self.stamina) + " " + str(self.balance)


player = Player()
game = Game(player, "playing")

running = True
while running:
    game.loop()
