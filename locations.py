"""
Contains different behaviors for locations upon entering/executing/exiting at these locations, as well as different actions
affecting the game the player can perform while present in these locations.
"""
import game
import random as rand


# formats an ASCII image by placing "-" bars above and below
def format_image(image):
    return "-" * 80 + "\n" + image + "\n" + "-" * 80


# A location parent class
class Location:
    def __init__(self, key, adjacent):
        # the string key associated with the location instance; different locations will have different string keys
        self.key = key
        # list containing string keys of adjacent locations
        self.adjacent = adjacent
        # list containing different ASCII images that could be rendered at each location.
        self.images = []
        # list containing location methods that can be accessed and executed during prompt() step of game loop.
        # This list corresponds to the different actions the player can perform at each location.
        self.actions = []

    # Behavior when the player enters a location. Ensures a game variable is passed into the method.
    def enter(self, g):
        assert isinstance(g, game.Game), "Did not pass game variable into location state function!"

    # Behavior when the player is currently playing at a location. Ensures a game variable is passed into the method.
    def execute(self, g):
        assert isinstance(g, game.Game), "Did not pass game variable into location state function!"

    # Behavior when the player exits a location. Ensures a game variable is passed into the method.
    def exit(self, g):
        assert isinstance(g, game.Game), "Did not pass game variable into location state function!"


# House location, where the player can sleep and regain stamina, as well as see their upgraded house.
class House(Location):
    def __init__(self, adjacent):
        super().__init__("house", adjacent)
        # ASCII images associated with the house
        self.images = ['''
                                                                                
                           ((    ((    ((((    ((    ((    ((((((  ((((((((     
                           @@    @@  @@    @@  @@    @@  @@        @@           
                           @@@@@@@@  @@    @@  @@    @@    @@@@    @@@@@@       
                           @@    @@  @@    @@  @@    @@        @@  @@           
       ###@@@@             **    **    ****      ****    ******    ********     
.........@@@@@..................................................................
         @@@@@                                                                  
  &                         &    .     &                                .       
     ,           %                                ,            ,                ''',
                       '''
                                                                                                      
                           ((    ((    ((((    ((    ((    ((((((  ((((((((     
                           @@    @@  @@    @@  @@    @@  @@        @@           
       ((@@@@@@@((         @@@@@@@@  @@    @@  @@    @@    @@@@    @@@@@@       
       @@@@@@@@@@@         @@    @@  @@    @@  @@    @@        @@  @@           
       @@@@@@@@@@@         **    **    ****      ****    ******    ********     
.......@@@@@@@@@@@..............................................................
       ***********                                                              
  &                         &    .     &                                .       
     ,           %                                ,            ,                ''',
                       '''
                                                                                                      
           (@(             ((    ((    ((((    ((    ((    ((((((  ((((((((     
        @@@@@@@@@          @@    @@  @@    @@  @@    @@  @@        @@           
    (@@@@@@@@@@@@@@@(      @@@@@@@@  @@    @@  @@    @@    @@@@    @@@@@@       
    @@@@@@@@@@@@@@@@@      @@    @@  @@    @@  @@    @@        @@  @@           
    @@@@@@@@@@@@@@@@@      **    **    ****      ****    ******    ********     
....@@@@@@@@@@@@@@@@@...........................................................
    @@@@@@@@@@@@@@@@@                                                           
  &                         &    .     &                                .       
     ,           %                                ,            ,                '''
                       ]
        self.actions = [self.restore_stamina, self.leave]

    def enter(self, g):
        super().enter(g)
        g.messages.append("Entering the house.")

    def execute(self, g):
        super().execute(g)
        g.messages.insert(0, format_image(self.images[g.player.house_tier]))
        available_actions = "\nWhat would you like to do?"
        # counter is enumerated into the text graphics to show increasing numbers that correspond to user input. For
        # example, the first action has a (0) in front of the action.
        counter = 0
        # sleeping option
        available_actions += "\n(" + str(counter) + ") Sleep"
        counter += 1
        # leaving the house option
        available_actions += "\n(" + str(counter) + ") Leave the house."
        g.messages.append(available_actions)

    def exit(self, g):
        super().exit(g)
        g.messages.append("Exiting the house.")

    # the following 2 methods are stored in the self.actions list to be accessed in the game prompt() ste
    def restore_stamina(self, g):
        g.player.stamina = 100
        g.messages.append("Zzzz.... After a night's rest, you feel energized and ready to work!\nStamina is full.")

    def leave(self, g):
        g.state = "changing"


# Shop location, where the player can buy/sell goods and upgrade their house.
class Shop(Location):
    def __init__(self, adjacent):
        super().__init__("shop", adjacent)
        # ASCII images associated with the shop
        self.images = [
            '''
                                                                                
     @@@@@@@@@@@@@@@@@@@       ((((((      ((    ((        ((((        ((((((   
     @@               @@     @@            @@    @@      @@    @@      @@    @@ 
     @@               @@       @@@@        @@@@@@@@      @@    @@      @@@@@@   
     @@               @@           @@      @@    @@      @@    @@      @@       
     @@               @@     ******        **    **        ****        **       
.....@@@@@@@@@@@@@@@@@@@........................................................
     @@@@@@@@@@@@@@@@@@@                                                        
  &                         &    .     &                                .       
     ,           %                                ,            ,                '''
        ]
        self.actions = [self.sell_grain, self.upgrade_house, self.leave]
        # list of house upgrade prices
        self.HOUSE_PRICES = [10, 20]
        # randomizes amount of grain the player can sell at once and the profit the player can gain by selling grain.
        self.grain_bundle_size = 5 + rand.randint(-1, 1)
        self.grain_cost = 5 + rand.randint(-1, 1)

    def enter(self, g):
        super().enter(g)
        g.messages.append("Entering the shop.")

    def execute(self, g):
        super().execute(g)
        g.messages.insert(0, format_image(self.images[0]))
        available_actions = "\nWhat would you like to do?"
        counter = 0
        self.grain_bundle_size = 5 + rand.randint(-1, 1)
        self.grain_cost = 5 + rand.randint(-1, 1)
        # selling grain option
        available_actions += "\n(" + str(counter) + ") Sell " + str(self.grain_bundle_size) + " grain for " + \
                             str(self.grain_cost) + " dollars."
        counter += 1
        # upgrading house option
        available_actions += "\n(" + str(counter) + ") Upgrade my house for " + \
                             str(self.HOUSE_PRICES[g.player.house_tier]) + " dollars ."
        counter += 1
        # leaving shop option
        available_actions += "\n(" + str(counter) + ") Leave the shop."
        g.messages.append(available_actions)

    def exit(self, g):
        super().exit(g)
        g.messages.append("Exiting the shop.")

    # the following 3 methods are actions the user can perform.
    def sell_grain(self, g):
        # only sell the player grain if they have enough grain to sell
        if g.player.grain >= self.grain_bundle_size:
            g.player.grain -= self.grain_bundle_size
            g.player.balance += self.grain_cost
            g.messages.append("You sold " + str(g.player.grain) + " grain.")
            g.messages.append("You received " + str(g.player.balance) + " dollars.")
        elif g.player.grain < self.grain_bundle_size:
            g.messages.append("Oops! You don't have enough grain to sell. Come back later.")

    def upgrade_house(self, g):
        if g.player.house_tier < 2:
            # the price of upgrading the house to the next tier
            price = self.HOUSE_PRICES[g.player.house_tier - 1]
            if g.player.balance >= price:
                g.player.house_tier += 1
                g.player.balance -= price
                g.messages.append(
                    "Congratulations on the new house! Your house is now tier " + str(g.player.house_tier + 1) +
                    ".\nReturn to your house to see your new, larger house. ")
                # the highest house tier possible
                if g.player.house_tier == 2:
                    g.messages.append("Congratulations! Your house has reached the max tier, tier" +
                                      str(g.player.house_tier + 1) + ". You have completed the game, but feel free to "
                                                                     "grind out more money!")
            elif g.player.balance < price:
                g.messages.append("Oops! It's too expensive to upgrade your house. Come back later.")
        else:
            g.messages.append("Your house is already max tier!")

    def leave(self, g):
        g.state = "changing"


# At the Farm, the player can get grain by solving multiplication problems.
class Farm(Location):
    def __init__(self, adjacent):
        super().__init__("farm", adjacent)
        self.images = [
            '''
            @                                                                   
        (@@@@@@@(        ((((((((        ((((        ((((((        ((      ((   
     @@@@@@@@@@@@@@@     @@            @@    @@      @@    @@      @@@@  @@@@   
  //@@@@@@@@@@@@@@@@//   @@@@@@        @@@@@@@@      @@@@@@        @@  @@  @@   
    @@@@@@@@@@@@@@@@     @@            @@    @@      @@  @@        @@      @@   
    @@@@@@@@@@@@@@@@     **            **    **      **    **      **      **   
..@.@@@@@@@@@@@@@@@@........@...................................................
  @ @@@@@@@@@@@@@@@@  @     @          #      #      @                      #   
  &  @      @    @    @     &    @     &          .       @    @    @   @       
     ,      ,    @                                ,            ,    ,           '''
        ]
        self.actions = [self.harvest, self.leave]
        # randomizes amount of grain the player gets per math problem and amount of stamina solving the problem drains.
        self.harvest_yield = 3 + rand.randint(-1, 1)
        self.stamina_drain = 15 + rand.randint(-5, 5)
        '''
        counter used to denote question_modes during the harvest math mode, each corresponding to a different iteration
        of the game loop.
            0 - the player is not in harvest mode
            1 - the player has entered harvest mode, the game now expects user input from the player that is the answer to
            the math problem
            2 - the player has inputted the answer to the math problem, the game now evaluates the validity of the answer.
        '''
        self.question_mode = 0
        self.question = ""

    def enter(self, g):
        super().enter(g)
        g.messages.append("Entering the farm.")

    def execute(self, g):
        super().execute(g)
        # the player is not in harvest mode
        if self.question_mode == 0:
            g.messages.insert(0, format_image(self.images[0]))
            available_actions = "\nWhat would you like to do?"
            counter = 0
            # re-randomizes harvest yield.
            self.harvest_yield = 3 + rand.randint(-1, 1)
            self.stamina_drain = 15 + rand.randint(-5, 5)
            available_actions += "\n(" + str(counter) + ") Harvest grain."
            counter += 1
            available_actions += "\n(" + str(counter) + ") Leave the farm."
            g.messages.append(available_actions)
        else:
            # The player is in harvest mode
            g.messages.insert(0, "\nYou farm grain with the sheer power of your math ability.\n" + 80 * "-")

            try:
                answer = int(g.inputs)
                # if the player has inputted an answer (question_mode 2) and the answer is the correct
                if self.question_mode == 2 and answer == int(eval(self.question)):
                    g.messages.append("That is correct!")
                    g.player.stamina -= self.stamina_drain
                    g.player.grain += self.harvest_yield
                    g.messages.append("You harvested " + str(self.harvest_yield) + " grain while losing " + \
                                      str(self.stamina_drain) + " stamina.")
                    g.messages.append("Press enter to go back to the farm.")
                    self.question_mode = 0
                    return
                else:
                    # if the player input is expected, and the answer was incorrect, the user is notified that the answer
                    # is incorrected
                    if self.question_mode == 2:
                        g.messages.append("That is incorrect!\nPress enter to go back to the farm.")
                        self.question_mode = 0
                        return
                self.question_mode = 2
            except ValueError:
                g.messages.append("Not a valid input. Wrong.\nPress enter to go back to the farm.")
                self.question_mode = 0

    def exit(self, g):
        super().execute(g)
        g.messages.append("Exiting the farm.")

    def harvest(self, g):
        if g.player.stamina >= self.stamina_drain:
            # randomizes factors in multiplication problem
            n, m = rand.randint(1, 10), rand.randint(1, 10)
            self.question = str(n) + " * " + str(m)
            g.prompts.append("What is " + self.question + "?")
            self.question_mode = 1
        else:
            g.messages.append("You ran out of stamina! Go back to your house to restore your energy.")

    def leave(self, g):
        g.state = "changing"
