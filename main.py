"""
TextTown is an interactive text-based RPG set within a medieval town.
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

'''
Peer Review Comments
--------------------
Commit: 4b4d6c7c1a20bf9a467945f155d02fea340b14fd
Peer Reviewer: Evelyn
Feedback:
I think the images that are printed on top of the code is rlly cool :) I think having to earn money def adds an incentive to the player.
More interesting if there are colors added to the images. Maybe list the price of the house? Also include like how the house is bigger in size after upgrading it.
--------------------
Commit: b38f0f22f6616334037f202c1225493bcd770a59
Peer Review: Ethan
Feedback: 
Very good code, a game that i would actully play,
I like the idea of having a game that is not linear until a definite end, this game can go on infinetly which makes it unique.
'''