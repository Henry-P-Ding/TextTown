# TODO: add explanations for all classes/files
# TODO: comment out all code
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
                                                                                
'''
        self.player = player
        self.state = state
        self.messages = []
        self.prompts = []
        self.inputs = ""
        self.day_count = 1
        self.boot_up_counter = 0

    def invalid_input_message(self):
        self.messages.append("Not a valid input.")

    # returns string with options of available locations to travel to
    def list_available_locations(self):
        adjacent_locations = settings.LOCATIONS[self.player.location].adjacent
        location_listing = "Where would you like to go?"
        for i in range(0, len(adjacent_locations)):
            location_listing += "\n(" + str(i) + ") " + adjacent_locations[i]
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
            settings.LOCATIONS[self.player.location].execute(self)

            # formats the contents of player's inventory
            self.messages.append(self.display_player_inventory())
        elif self.state == "booting":
            if self.boot_up_counter < 48:
                self.messages.append("\n" * (47 - self.boot_up_counter) + (36 * "-" + "LOADING" + 37 * "-" + "\n") + \
                                     "\n" * self.boot_up_counter)
                self.boot_up_counter += 1
            else:
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

        # display messages sequentially
        for message in self.messages:
            print(message)
        if self.state == "booting":
            time.sleep(0.01)

    # prompts user for inputs
    def prompt(self):
        self.messages = []
        if self.state != "booting":
            # asks user for a valid input for a new location to travel to
            print("-" * 80)
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

        # processes inputs
        elif self.state == "changing":
            adjacent_locations = settings.LOCATIONS[self.player.location].adjacent
            try:
                new_location = adjacent_locations[int(self.inputs)]
                settings.LOCATIONS[self.player.location].exit(self)
                settings.LOCATIONS[new_location].enter(self)
                self.player.location = new_location
                self.state = "playing"
            except ValueError:
                self.invalid_input_message()
            except IndexError:
                self.messages.append("Not a valid location.")
        elif self.state == "playing":
            if isinstance(settings.LOCATIONS[self.player.location], locations.Farm) and \
                    settings.LOCATIONS[self.player.location].question_mode != 0:
                return
            try:
                action_index = int(self.inputs)
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