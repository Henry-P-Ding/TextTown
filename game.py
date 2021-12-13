"""
The main game file with a Game class containing general functionality for updating the game state, rendering graphics,
and processing user inputs. The game class also contains useful data to be transferred to different classes such as the
current game state, the player object associated with the game, "messages" to be rendered, player inputs, etc. Other
functionality associated with specific locations are located in the locations.py file.
"""
import locations
import settings
import os
import time

class Game:
    def __init__(self, player, state):
        self.TITLE = '''
                                                                                
  @@@@@@@@@@@@@@@   @@@@@@@@@@@@   @@@      @@@   @@@@@@@@@@@@@@@               
        @@@         @@@            @@@      @@@         @@@                     
        @@@         @@@//////      (((//////(((         @@@                     
        @@@         @@@@@@@@@         @@@@@@            @@@                     
        @@@         @@@            @@@      @@@         @@@                     
        @@@         @@@@@@@@@@@@   @@@      @@@         @@@                     
                                                                                
             @@@@@@@@@@@@@@@      @@@@@@      @@@         @@@   @@@      @@@    
                   @@@         @@@      @@@   @@@         @@@   @@@@@@   @@@    
                   @@@         @@@      @@@   @@@   %%%   @@@   @@@,,,%%%@@@    
                   @@@         @@@      @@@   @@@,,,%%%,,,@@@   @@@   %%%@@@    
                   @@@         @@@      @@@   @@@@@@   @@@@@@   @@@      @@@    
                   @@@            @@@@@@      @@@         @@@   @@@      @@@    
                                                                                
Upgrade your house to the highest tier!
'''
        self.player = player
        '''
        The game "state", what the game is trying to accomplish during the current game loop iteration.
        The possible game states are: 
            "title": The title screen.
            "playing": When the player is performing actions at a location 
            "changing": When the player is asked to change locations.
            "booting": The loading screen animation
        '''
        self.state = state
        # list containing strings to be rendered in the render() step at the top of the terminal
        self.messages = []
        # list containing strings to be rendered in the prompt() step that ask the player questions
        self.prompts = []
        # string containing all user input characters
        self.inputs = ""
        # a day counter to track game progression
        self.day_count = 1
        # a counter used to animate the loading animation
        self.boot_up_counter = 0

    def invalid_input_message(self):
        self.messages.append("Not a valid input.")

    # returns string with options of available locations to travel to
    def list_available_locations(self):
        adjacent_locations = settings.LOCATIONS[self.player.location].adjacent
        location_listing = "Where would you like to go?"
        for i in range(0, len(adjacent_locations)):
            location_listing += "\n(" + str(i + 1) + ") " + adjacent_locations[i]
        return location_listing

    def display_player_inventory(self):
        inventory = "\n" + "-" * 80 + "\nPLAYER INVENTORY:"
        inventory += "\nStamina: " + str(self.player.stamina)
        inventory += "\nGrain: " + str(self.player.grain)
        inventory += "\nBalance: " + str(self.player.balance) + "\n"
        return inventory

    # update logic for game loop
    def update(self):
        if self.state == "changing":
            # lists out options of available locations to travel to
            self.messages.append(self.list_available_locations())
        elif self.state == "playing":
            self.day_count += 1
            self.messages.append("\nDay: " + str(self.day_count))
            # When the game is "playing" while the player is in a certain location, the location contains code to be
            # executed in its execute() method.
            settings.LOCATIONS[self.player.location].execute(self)
            # adds the contents of player's inventory to rendered list.
            self.messages.append(self.display_player_inventory())
        elif self.state == "booting":
            # 48 corresponds to the height of the terminal window. The loading bar moves from the bottom of the terminal
            # to the top during the "booting" game state.
            if self.boot_up_counter < 48:
                self.messages.append("\n" * (47 - self.boot_up_counter) + (36 * "-" + "LOADING" + 37 * "-" + "\n") + \
                                     "\n" * self.boot_up_counter)
                self.boot_up_counter += 1
            else:
                # once booting is completed, the game state is changed to the "title" state.
                self.state = "title"
                self.messages.append(self.TITLE)
                self.prompts.append("Start the game? [yes] or [no]")
        elif self.state == "title":
            self.prompts.append("Start the game? [yes] or [no]")

    # renders messages from update and prompt steps
    def render(self):
        # Terminal clearing code adapted from user 'poke' on StackOverflow here:
        # https://stackoverflow.com/questions/2084508/clear-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')

        # display messages sequentially line by line. Different entries in the self.messages list are displayed on
        # separate lines.
        for message in self.messages:
            print(message)

        # visual delay in "booting" screen to create animation
        if self.state == "booting":
            time.sleep(0.01)

    # prompts user for inputs
    def prompt(self):
        # clears messages list since all messages had just been redendered.
        self.messages = []
        if self.state != "booting":
            print("-" * 80)
            # prints prompts (questions) that indicate what type of user input is expected. Used in the harvest math mode.
            for prompt in self.prompts:
                print(prompt)
            self.inputs = input(">> ").lower().strip()
            self.prompts = []

        if self.state == "title":
            if self.inputs == "yes":
                self.state = "playing"
            elif self.inputs == "no":
                self.messages.append(self.TITLE)
                self.messages.append("Hmm... I think you should start the game.")
            else:
                self.messages.append(self.TITLE)
                self.invalid_input_message()

        elif self.state == "changing":
            # Locations that the player can travel to based on the player's current location
            adjacent_locations = settings.LOCATIONS[self.player.location].adjacent
            try:
                new_location = adjacent_locations[int(self.inputs) - 1]
                # settings.LOCATIONS location class is accessed by a dictionary entry
                # exit() code associated with class when location is exited by the player.
                settings.LOCATIONS[self.player.location].exit(self)
                # enter() code associated with class when a new location is entered by the player.
                settings.LOCATIONS[new_location].enter(self)
                self.player.location = new_location
                # After the player changes location, the game state is changed to be "playing" at that new location.
                self.state = "playing"
            except ValueError:
                self.invalid_input_message()
            except IndexError:
                self.messages.append("Not a valid location.")
        elif self.state == "playing":
            # If the player is in harvest mode, the input is not processed in this prompt() method but is processed
            # within the Farm location class itself.
            if isinstance(settings.LOCATIONS[self.player.location], locations.Farm) and \
                    settings.LOCATIONS[self.player.location].question_mode != 0:
                return
            try:
                # Accesses .actions attribute in each Location containing list of actions that the player can perofrm at
                # a location. Player input selects these actions.
                action_index = int(self.inputs) - 1
                settings.LOCATIONS[self.player.location].actions[action_index](self)
            except ValueError:
                self.invalid_input_message()
            except IndexError:
                self.messages.append("Not a valid option.")

    # main game loop. render is called twice, first to render new calculated game states from update(), then to render
    # new content from prompt() logic.
    def loop(self):
        self.update()
        self.render()
        self.prompt()
        self.render()
