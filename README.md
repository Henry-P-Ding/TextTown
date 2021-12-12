# TextTown

TextTown is an interactive text-based RPG set within a medieval town. In the TextTown, the player farms grain by solving 
math equations to upgrade their house to three different tiers. With each tier, the house becomes bigger. When the 
player upgrades their house to tier 3, the game ends.

**IMPORTANT: Please change your terminal window size to 80x48!**

## Project Description
I conceived of this game as a text-input game with different locations the user could visit and perform actions in.
While designing the game, I wanted the player to have some feeling of progression in the game. During this thought
process, I introduced the mechanic of the player being able to upgrade several house tiers through performing some 
action in the game. I also wanted some sort of challenge for the player to upgrade these house tiers. As a result,
I came up with the game mechanic of harvesting and then selling grain by selling math problems. One of the coolest
features of TextTown is the introduction of different locations that the player can explore. As a result, I did not want 
the player to simply stay the farming location continuously farm up grain and then visit the shop at once. Because of
this, I introduced the stamina mechanic which would require the player to return to the house afer farming for a
sufficiently long time.

With the game planned out, I began tackling the task of implementing the code. Because there are several locations in
the game, and the player could only exist in one location at one time, I decided to use a Finite State Machine structure
to organize the different locations, which I had learned about over the summer studying Minecraft code. However, I had
trouble working OOP principles in Python, as most of my knowledge was based in Java. For example, I attempted to make 
all of these classes singletons, a class in which only one dynamic instance could exist. The benefit of using a
Singleton over a static class in my code is that I would be able to pass the single instance in dictionaries or
lists, such as a registry containing all of my game locations. However, I did not know how to specify static variables 
in Python, nor did I know how to create a private constructor method. As a result, I ended up risking potentially
instantiating these Location objects multiple times and simply did not worry about this problem. In the end, I stored
a single instance of all of these location objects in a ``dict`` declared in the ``settings.py`` file. I was still able
to reap some benefits of an OOP approach, as I was able to simply refer to ``enter()`` and ``exit()`` methods when the
player changes locations without specifying which location the player is in.

I also had difficulty in receiving user input in this game. In location screens, the player is presented with potential
options that the player can access. Each of these options corresponds to a specific action the player can take, such as
harvesting grain or going to sleep. The prompt the player for user input, I could either embed ``input()`` functions 
within the methods of each of the Location classes. However, this is problematic for multiple reasons. First,
this practice connects the implementation of the Location classes in the game with the Location class designs. What this
meant in concrete terms was that, if I were to go with this approach, I would have to rewrite methods that prompted the 
player for user input for every single Location class. Even if I was clever about this a created a method for prompting 
user input in the Location super class, I would still have to re-implement user input for other moments in the game when
the player is not a location, such as when the player is prompted to switch locations or to begin the game while on the
title screen. To resolve these issues, I created one ``prompt()`` method that would be run every game loop. This fixes
the issue of having to write multiple input methods into several locations in the code. However, this also
introduced the issue of transferring data of user input from the ``prompt()`` method to each of the Location classes to
then process this input before finally outputting some result of the player's decision associated with that Location. 
In order to accomplish this, I figured out that I could store user inputs in a single string attribute of the main Game
object that would then be passed into every Location method. I was then able to access user input in each of the
Location methods, resolving the issue of processing user input.

In the middle of developing the project and bug testing with Ethan, I realized that I had not pre-processed any of the
user input with ``strip()`` or ``lower()``. Luckily, because of my earlier implementation of user-input with relies on a
single ``prompt()`` method to gather all user input, I was able to fix this issue by adding ``strip()`` and ``lower()`` 
to one line in order to resolve all issues.

## Peer Review Comments
* **Commit:** `4b4d6c7c1a20bf9a467945f155d02fea340b14fd`
* **Peer Reviewer:** Evelyn
* **Feedback:**
I think the images that are printed on top of the code is rlly cool :) I think having to earn money def adds an incentive to the player.
More interesting if there are colors added to the images. Maybe list the price of the house? Also include like how the house is bigger in size after upgrading it.
* **Post Feedback Revisions**
  * Included house price in shop listing.
  * Added recommendation for player to return to the house location in order to see the upgraded house.
--------------------
* **Commit:** `b38f0f22f6616334037f202c1225493bcd770a59`
* **Peer Review:** Ethan
* **Feedback:**
Very good code, a game that i would actully play,
I like the idea of having a game that is not linear until a definite end, this game can go on infinetly which makes it unique.
* **Post Feedback Revisions**
  * Included ``.strip()`` and ``.lower()`` into player input processing.
  * Fixed player soft-lock bug in harvesting mode. See commit ``e751dd6a7ef5ce74d95ac740b1e6a9d8dcf9a4db`` for more details.
## Resources Used in this Project
* https://stackoverflow.com/questions/402504/how-to-determine-a-python-variables-type
    - Used for variable type confirmation in Location class within `locations.py` file. This is to ensure that the g
    argument passed into Location methods are always of the Game type.
* https://docs.python.org/3/library/exceptions.html#bltin-exceptions
    - List of Python exceptions. I referenced this website to determine which exceptions I would use for my `try:` and
    `except:` statements, used in the `prompt()` method of the Game class within the `game.py` file.
* https://www.tutorialspoint.com/python/assertions_in_python.htm
    - I learned how to write assertions in Python. An assertion was used in each of the enter/execute/exit methods of
    the Location class and all child classes. This assertion was used to ensure that the g argument passed into the
    Location methods are always of the Game type.
* https://www.pixilart.com/
    - A free, online pixel art editor I used to generate pixel art that was then converted into ASCII art on
    https://www.ascii-art-generator.org/. 
* https://www.ascii-art-generator.org/
    - A website used to generate ASCII art from image files. ASCII art generated by this website was featured in the
    ASCII images for the title screen and the house/shop/farm locations.
* https://www.geeksforgeeks.org/eval-in-python/
    - I learned about the `eval()` function in Python from this article. The `eval()` function was used to evaluate the
    answer to math questions in the harvesting mode of the Farm location.
* Minecraft Seedfinding Community and https://github.com/Hexeption/MCP-Reborn
    - **While I did not reference any of these resources during the project**, I learned a significant amount of my programming knowledge by reading decompiled Minecraft code through projects 
    such as MCP reborn and talking to programming experts in the Minecraft Seedfinding Community. For example, the code 
    structure resembling that of an FSM (Finite State Machine) is based off my exploration of the FSM used in Ender 
    Dragon code in Minecraft, as well as conservations with other Minecraft seed finders on Discord.
* https://www.youtube.com/watch?v=VO8rTszcW4s
    - **While I did not reference this resource during the project**, I learned about the general ``update()``, ``render()`` and ``input()`` game loop structure from this video years 
    ago sometime in 2016 or 2017.