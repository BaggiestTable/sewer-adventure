"""
Author: Christopher Yutzy
File Name: player.py
Description: This file defines functions
and methods for the player.
"""

class Player:

    directions = ('north', 'east', 'south', 'west')
    forward = 'north'
    right = 'east'
    back = 'south'
    left = 'west'
    inv = []
    dog_tamed = False
    loc = None
    magic = False
    notebook_note = None
   
    def get_rel_direction(direction):
        """Returns a cardinal direction when given a relative direction"""
        rel_dir_map = {
            'forward':Player.forward,
            'straight':Player.forward,
            'right':Player.right,
            'back':Player.back,
            'backward':Player.back,
            'backwards':Player.back,
            'left':Player.left
        }
        return rel_dir_map.get(direction)

    def face(direction):
        """Sets the relative directions that the player is facing by iterating through a dictionary"""
        index = Player.directions.index(direction)

        Player.forward = Player.iterate_direction(index)
        Player.right = Player.iterate_direction(index + 1)
        Player.back = Player.iterate_direction(index + 2)
        Player.left = Player.iterate_direction(index + 3)
        return Player.forward, Player.right, Player.back, Player.left

    def iterate_direction(index):
        """Recieves an index for the directions tuple 
        and iterates through each one restarting at the end of the cardinal direcitons."""
        if index > 3:
                index -= 4
        return Player.directions[index]

    def get_direction(user_input):
        dir_map = {
            'north': Player.loc.north,
            'east': Player.loc.east,
            'south': Player.loc.south,
            'west': Player.loc.west,
            'up': Player.loc.up,
            'down': Player.loc.down
        }
        if user_input in dir_map:
            return dir_map.get(user_input)
        else: print("ERROR: INVALID DIRECTION FOR get_direction")