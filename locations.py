"""
Contains different behaviors for locations upon entering/executing/exiting at these locations
"""
import game
import random as rand


def format_image(image):
    return "-" * 80 + "\n" + image + "\n" + "-" * 80


class Location:
    def __init__(self, key, adjacent):
        self.key = key
        self.adjacent = adjacent
        self.images = []
        self.actions = []

    def enter(self, g):
        assert isinstance(g, game.Game), "Did not pass game variable into location state function!"

    def execute(self, g):
        assert isinstance(g, game.Game), "Did not pass game variable into location state function!"

    def exit(self, g):
        assert isinstance(g, game.Game), "Did not pass game variable into location state function!"


class House(Location):

    def __init__(self, adjacent):
        super().__init__("house", adjacent)
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
        counter = 0
        available_actions += "\n(" + str(counter) + ") Sleep"
        counter += 1
        available_actions += "\n(" + str(counter) + ") Leave the house."
        g.messages.append(available_actions)

    def exit(self, g):
        super().exit(g)
        g.messages.append("Exiting the house.")

    def restore_stamina(self, g):
        g.player.stamina = 100
        g.messages.append("Zzzz.... After a night's rest, you feel energized and ready to work!")

    def leave(self, g):
        g.state = "changing"


class Shop(Location):
    def __init__(self, adjacent):
        super().__init__("shop", adjacent)
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
        self.HOUSE_PRICES = [10, 20]
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
        available_actions += "\n(" + str(counter) + ") Sell " + str(self.grain_bundle_size) + " grain for " + \
                             str(self.grain_cost) + " dollars."
        counter += 1
        available_actions += "\n(" + str(counter) + ") Upgrade my house."
        counter += 1
        available_actions += "\n(" + str(counter) + ") Leave the shop."
        g.messages.append(available_actions)

    def exit(self, g):
        super().exit(g)
        g.messages.append("Exiting the shop.")

    def sell_grain(self, g):
        if g.player.grain >= self.grain_bundle_size:
            g.player.grain -= self.grain_bundle_size
            g.player.balance += self.grain_cost
            g.messages.append("You sold " + str(g.player.grain) + " grain.")
            g.messages.append("You received " + str(g.player.balance) + " dollars.")
        elif g.player.grain < self.grain_bundle_size:
            g.messages.append("Oops! You don't have enough grain to sell. Come back later.")

    def upgrade_house(self, g):
        if g.player.house_tier < 2:
            price = self.HOUSE_PRICES[g.player.house_tier - 1]
            if g.player.balance >= price:
                g.player.house_tier += 1
                g.player.balance -= price
                g.messages.append(
                    "Congratulations on the new house! Your house is now tier " + str(g.player.house_tier + 1) + ".")
            elif g.player.balance < price:
                g.messages.append("Oops! It's too expensive to upgrade your house. Come back later.")
        else:
            g.messages.append("Your house is already max tier!")

    def leave(self, g):
        g.state = "changing"


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
        self.harvest_yield = 3 + rand.randint(-1, 1)
        self.stamina_drain = 15 + rand.randint(-5, 5)
        self.question_mode = 0
        self.question = ""

    def enter(self, g):
        super().enter(g)
        g.messages.append("Entering the farm.")

    def execute(self, g):
        super().execute(g)
        if self.question_mode == 0:
            g.messages.insert(0, format_image(self.images[0]))
            available_actions = "\nWhat would you like to do?"
            counter = 0
            self.harvest_yield = 3 + rand.randint(-1, 1)
            self.stamina_drain = 15 + rand.randint(-5, 5)
            available_actions += "\n(" + str(counter) + ") harvest grain."
            counter += 1
            available_actions += "\n(" + str(counter) + ") leave."
            g.messages.append(available_actions)
        else:
            g.messages.insert(0, "\nYou farm grain with the sheer power of your math ability.\n" + 80 * "-")

            try:
                answer = int(g.inputs)
                if answer == int(eval(self.question)):
                    g.messages.append("That is correct!")
                    g.player.stamina -= self.stamina_drain
                    g.player.grain += self.harvest_yield
                    g.messages.append("You harvested " + str(self.harvest_yield) + " grain while losing " + \
                                      str(self.stamina_drain) + " stamina.")
                    g.messages.append("Press enter to go back to the farm.")
                    self.question_mode = 0
                    return
                else:
                    if self.question_mode == 2:
                        g.messages.append("That is incorrect!")
                        g.messages.append("Press enter to go back to the farm.")
                        self.question_mode = 0
                        return
                self.question_mode = 2
            except ValueError:
                g.messages.append("Not a valid input. Wrong.")

    def exit(self, g):
        super().execute(g)
        g.messages.append("Exiting the farm.")

    def harvest(self, g):
        if g.player.stamina >= self.stamina_drain:
            n, m = rand.randint(1, 10), rand.randint(1, 10)
            self.question = str(n) + " * " + str(m)
            g.prompts.append("What is " + self.question + "?")
            self.question_mode = 1
        else:
            g.messages.append("You ran out of stamina! Go back to your house to restore your energy.")

    def leave(self, g):
        g.state = "changing"
