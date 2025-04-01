"""
Author: Christopher Yutzy
File Name: room.py
Description: This file defines attributes, functions,
and methods for the rooms in the game.
"""

class Room:

    # dictionary with the descriptions of the rooms
    new_room_intro = {
        "road1":"You find yourself at the end of a road; to the north of you is a school, to the east of you is a river, and to the west is a park.",
        "road2":"You are on a road; to the east of you is a forest.",
        "school":"You are now in a school building. There is a room to the east, north, and west of you.",
        "it_room":"You entered a room full of computers.",
        "history_room":"You are in a room with some books and timeline plots on the walls. A marking on the wall says \"left, straight, right\"",
        "science_room":"You are in a room with many pictures of disgusting things.",
        "music_room":"You entered a room full of instruments. You feel an urge to tap the drums and other percussion instruments.",
        "park":"You are in a park with nice green grass. To the north of you is a playground.",
        "forest":"You are now in a forest. It is hard to tell what is around you.",
        "playground":"You are on a playground. The sand and rocks get into your shoes.",
        "river":"You are in the bend of a river. The river gets thinner as it heads north, and a forest is to the south.\nI don't know why you got in, but your shoes are soaking wet now.",
        "stream":"You are by a stream. To the south, it turns into a river. To the north, a tall wall of brush.\nThe stream heads down a gutter nearby.",
        "sewer1":"You- You dropped into the sewer. I guess since your shoes were already wet the rest of your clothes don't matter anyway.\nThe sewer heads north.",
        "sewer2":"You head down the sewer. You stop to take a break.",
        "sewer3":"You are in the sewer. There is a door on the west side of the wall here.",
        "maze1":"You are inside a maze. There is a door to the east.",
        "maze2":"You are still in the maze.",
        "maze3":"You are inside a maze. You can see a light to the west.",
        "maze4":"You are still in the maze.",
        "maze5":"You are still in the maze.",
        "maze6":"You are still in the maze.",
        "cavern":"You are now in a cavern. To the east is the maze, to the south is a door, and to the west is a mineshaft.",
        "subway":"You are in a subway tunnel. To the south is a cavern.",
        "mineshaft":"The mineshaft continues west to more mines. To the north are some ruins, to the east is the cavern, and to the south is a library.",
        "roman_ruins":"These ruins look like they are of Roman origin. They must be ancient from when the Romans conquered Kansas.",
        "dwarven_mine":"You have reached the dwarven mines. You can return east if you don't want to stay.",
        "library":"There are many books in this library. To the north is the mineshaft.",
        "door":"A large door with a skeleton emblem on it. It seems to be held closed by a mysterious force.\nWho knows what is on the other side?",
        "fortress":"You enter the fortress. This place looks scary. You can see something shiny to the south.",
        "national_treasure":"Congratulations! You found the national treasure! You beat the game.",
        "hole":"There is ground in the way of you going down. If only you could move it out of the way.",
        "gutter":"This manhole has a lock for no reason."
    }
    # if the player wants an explanation of the room, they get the first introduction. Some don't make sense so I have a separate assignment in main for that.
    # make a separate dictionary for explanations
    explain_room = {key: value for key, value in new_room_intro.items()}
    # make descriptions for items
    item_desc_dict = {
        'notebook':"There is a notebook on the ground.",
        'shovel':"A shovel is underneath the slide.",
        'bone':"There is a bone on the ground that fell from a display.",
        'stick':"There is a stick on the ground.",
        'key':"Someone seems to have left a key here.",
        'nitrobid':"There's some nitrobid on a counter.",
        'keytar':"A keytar is lying agianst the wall in the corner."
    }
    # descriptions for when an npc is in the room
    npc_desc = {
        'wolf':"There is a wolf here.",
        'skeleton':"There is a skeleton here. He seems dangerous.",
        'dwarf':"There is a dwarf miner here.",
        'wizard':"There is a wizard here reading a book."
    }
    room_list = []



# initiates object and assigns directions and items to itself
    def __init__(self, name):
        """Initiate object and assign attributes to itself."""
        self.name = name
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.up = None
        self.down = None
        self.items = []
        self.locked = False     # I used separate locked rooms for locked areas. I reassign the directions to a different room once the area is unlocked.
        self.new = True
        self.npc = None
        self.desc = None
        Room.room_list.append(self)

    def __str__(self):
        """Return the name of the object."""
        return (self.name)

    def set_directs(self, north = None, east = None, south = None, west = None, up = None, down = None):
        """Set what rooms certain directions lead to."""
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.up = up
        self.down = down

    def get_room(self, direction):
        """Give the cooresponding room in the direction specified by the given string."""
        directions = {
            'north':self.north,
            'east':self.east,
            'south':self.south,
            'west':self.west,
            'up':self.up,
            'down':self.down
        }
        return directions.get(direction)

    def intro(self, explain = False):
        """Print the description of the location by finding the value in the desc_dict"""
        # If the player hasn't visited this location yet, then it is new.
        if self.new: 
            print(self.new_room_intro.get(self.name))
            if not self.locked:
                self.new = False
        # If the player asked for a description of the locaiton, give it.
        elif explain: 
            print(self.explain_room.get(self.name))
        else:
            print(self.desc)
        # If the room has items, print the items.
        if self.items: 
            for item in self.items:
                desc = Room.item_desc_dict.get(item)
                # If there isn't a description, send an error.
                if desc == None:
                    print("ERROR: NO ITEM DESCRIPTION")
                else:
                    print(desc, end = '')
            print()
        # If there is an npc, say that there is an npc.
        if self.npc: 
            if Room.npc_desc.get(self.npc) == None:
                print(f"no npc_desc for {self.npc}")
                return
            print(Room.npc_desc.get(self.npc))