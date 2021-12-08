"""
Contains different behaviors for locations upon entering/executing/exiting at these locations

"""
import game


class Location:
    def __init__(self, key, adjacent):
        self.key = key
        self.adjacent = adjacent

    def enter(self, g):
        assert isinstance(g, game.Game), "Did not pass game variable into location state function!"

    def execute(self, g):
        assert isinstance(g, game.Game), "Did not pass game variable into location state function!"

    def exit(self, g):
        assert isinstance(g, game.Game), "Did not pass game variable into location state function!"


class House(Location):
    def __init__(self, adjacent):
        super().__init__("house", adjacent)

    def enter(self, g):
        super().enter(g)
        g.messages.append("Entering House")

    def execute(self, g):
        super().execute(g)
        g.messages.append("In House.")

    def exit(self, g):
        super().exit(g)
        g.messages.append("Exiting house.")


class Shop(Location):
    def __init__(self, adjacent):
        super().__init__("shop", adjacent)

    def enter(self, g):
        super().enter(g)
        g.messages.append("Entering shop.")

    def execute(self, g):
        super().execute(g)
        g.messages.append("In shop.")

    def exit(self, g):
        super().exit(g)
        g.messages.append("Exiting shop.")


class Farm(Location):
    def __init__(self, adjacent):
        super().__init__("farm", adjacent)

    def enter(self, g):
        super().enter(g)
        g.messages.append("Entering farm.")

    def execute(self, g):
        super().execute(g)
        g.messages.append("On the farm.")

    def exit(self, g):
        super().execute(g)
        g.messages.append("Exiting the farm.")
