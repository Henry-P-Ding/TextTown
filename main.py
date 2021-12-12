"""
TextTown is an interactive text-based RPG set within a medieval town. Find more detailed information about TextTown
as well as peer review/resources used in this project within the README.
December 7, 2021,
Henry Ding
"""
from game import *

# A player container class with associated attributes of a player.
class Player:
    def __init__(self):
        self.location = "house"
        self.stamina = 100
        # Wealth of the player in dollars.
        self.balance = 0
        self.grain = 0
        # The tier of the player's house, which affects how the player house is rendered at the house location.
        self.house_tier = 0

player = Player()
# Instantiate a new game class in "booting" mode.
game = Game(player, "booting")

running = True
while running:
    game.loop()

# omh
