# TODO: add explanations for all classes/files
# TODO: comment out all code
import settings
import os

class Game:
    def __init__(self, player, state):
        self.player = player
        self.state = state
        self.messages = []
        self.prompts = []
        self.inputs = ""

    # returns string with options of available locations to travel to
    def list_available_locations(self):
        adjacent_locations = settings.LOCATIONS[self.player.location].adjacent
        location_listing = "Available locations: "
        for i in range(0, len(adjacent_locations)):
            location_listing += "\n(" + str(i) + ") " + adjacent_locations[i]
        return location_listing

    # update logic for game loop
    def update(self):
        self.prompts = []
        if self.state == "changing":
            # list player states at the top of the window
            self.messages.append("Current location: " + self.player.location + ".")

            # lists out options of available locations to travel to
            self.messages.append(self.list_available_locations())
        elif self.state == "playing":
            self.messages.append("Current location: " + self.player.location + ".")
            settings.LOCATIONS[self.player.location].execute(self)

    # renders messages from update and prompt steps
    def render(self):
        # Terminal clearing code adapted from user 'poke' on StackOverflow here:
        # https://stackoverflow.com/questions/2084508/clear-terminal-in-python
        os.system('cls' if os.name == 'nt' else 'clear')

        # diplace messages sequentially
        for message in self.messages:
            print(message)

    # prompts user for inputs
    def prompt(self):
        self.messages = []
        # asks user for a valid input for a new location to travel to
        for prompt in self.prompts:
            print(prompt)
        self.inputs = input(">> ")

        # processes inputs
        if self.state == "changing":
            adjacent_locations = settings.LOCATIONS[self.player.location].adjacent
            try:
                new_location = adjacent_locations[int(self.inputs)]
                settings.LOCATIONS[self.player.location].exit(self)
                settings.LOCATIONS[new_location].enter(self)
                self.player.location = new_location
                self.state = "playing"
            except ValueError:
                self.messages.append("Not a valid input.")
            except IndexError:
                self.messages.append("Not a valid location.")
        elif self.state == "playing":
            if self.inputs == "y":
                self.state = "changing"

    # main game loop. render is called twice, first to render new calculated game states from update(), then to render
    # new content from prompt() logic.
    def loop(self):
        self.update()
        self.render()
        self.prompt()
        self.render()
