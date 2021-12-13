"""
A settings file containing the configuration of the game map (with locations on the game map are adjacent to each other).
"""
import locations

# location dict with adjacency list; other locations connected to this location are listed.
# This is separated from 'locations.py' in order to separate location functionality from implementation in game map.
LOCATIONS = {
    "house": locations.House(["shop", "farm"]),
    "shop": locations.Shop(["house", "farm"]),
    "farm": locations.Farm(["house", "shop"])
}
