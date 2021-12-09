"""
Contains different behaviors for locations upon entering/executing/exiting at these locations

"""
import game


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
        self.actions = [self.restore_stamina, self.leave_house]

    def enter(self, g):
        super().enter(g)
        g.messages.append("Entering House")

    def execute(self, g):
        super().execute(g)
        g.messages.insert(0, format_image(self.images[g.player.house_tier]))
        available_actions = "What would you like to do?"
        counter = 0
        available_actions += "\n(" + str(counter) + ") Sleep"
        counter += 1
        g.location_actions.append(self.restore_stamina)
        available_actions += "\n(" + str(counter) + ") Leave the house."
        g.messages.append(available_actions)

    def exit(self, g):
        super().exit(g)
        g.messages.append("Exiting house.")

    def restore_stamina(self, g):
        g.player.stamina = 100
        g.messages.append("Zzzz.... After a night's rest, you feel energized and ready to work!")

    def leave_house(self, g):
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

    def enter(self, g):
        super().enter(g)
        g.messages.append("Entering shop.")

    def execute(self, g):
        super().execute(g)
        g.messages.insert(0, format_image(self.images[0]))

    def exit(self, g):
        super().exit(g)
        g.messages.append("Exiting shop.")


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

    def enter(self, g):
        super().enter(g)
        g.messages.append("Entering farm.")

    def execute(self, g):
        super().execute(g)
        g.messages.insert(0, format_image(self.images[0]))

    def exit(self, g):
        super().execute(g)
        g.messages.append("Exiting the farm.")
