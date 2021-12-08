"""
Contains different behaviors for locations upon entering/executing/exiting at these locations

"""
import game

class Location:
    def __init__(self, key, adjacent):
        self.key = key
        self.adjacent = adjacent

    def enter(self, messages):
        pass

    def execute(self, messages):
        pass

    def exit(self, messages):
        pass


class House(Location):
    def __init__(self, adjacent):
        super().__init__("house", adjacent)

    def enter(self, messages):
        messages.append("Entering House")

    def execute(self, messages):
        messages.append("In House.")

    def exit(self, messages):
        messages.append("Exiting house.")


class Shop(Location):
    def __init__(self, adjacent):
        super().__init__("shop", adjacent)

    def enter(self, messages):
        messages.append("Entering shop.")

    def execute(self, messages):
        messages.append("In shop.")

    def exit(self, messages):
        messages.append("Exiting shop.")


class Farm(Location):
    def __init__(self, adjacent):
        super().__init__("farm", adjacent)

    def enter(self, messages):
        messages.append("Entering farm.")

    def execute(self, messages):
        messages.append("On the farm.")

    def exit(self, messages):
        messages.append("Exiting the farm.")
