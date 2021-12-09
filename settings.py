import locations

# location dict with adjacency list; other locations connected to this location are listed.
# This is separated from 'locations.py' in order to separate location functionality from implementation in game map.
LOCATIONS = {
    "house": locations.House(["shop", "farm"]),
    "shop": locations.Shop(["house"]),
    "farm": locations.Farm(["house"])
}

# possible game states
STATES = [
    "changing",
    "playing"
]
