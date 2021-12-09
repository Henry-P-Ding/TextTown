"""
TextTown is an interactive text-based RPG set within a medieval town. Find more detailed information about TextTown
as well as peer review/resources used in this project within the README.
December 7, 2021,
Henry Ding
"""
from game import *


class Player:
    def __init__(self):
        self.location = "house"
        self.stamina = 100
        self.balance = 0
        self.grain = 0
        self.house_tier = 0


player = Player()
game = Game(player, "booting")

running = True
while running:
    game.loop()

# omh
