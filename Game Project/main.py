"""
Author: Christopher Yutzy
File Name: main.py
Description: The main file for running my text adventure game.
I used ChatGPT and Gemini to remind me how python works and give
me some ideas on how to do some things. Coding and annotation done by me.
"""

import random
import os
import pandas as pd
import time
from room import Room
from player import Player


file_path = os.path.dirname(__file__)       # import a file containing the rooms and which rooms they lead to
room_csv = pd.read_csv(file_path + r'\Sewer Adventure - Room Assignment.csv')
room_csv.set_index('Name', inplace=True)    # make the room names the index of the file


# declare all of the rooms and their name
road1 = Room("road1")
road2 = Room("road2")
school = Room("school")
it_room = Room("it_room")
history_room = Room("history_room")
music_room = Room("music_room")
science_room = Room("science_room")
park = Room("park")
playground = Room("playground")
forest = Room("forest")
river = Room("river")
stream = Room("stream")
sewer1 = Room("sewer1")
sewer2 = Room("sewer2")
sewer3 = Room("sewer3")
maze1 = Room("maze1")
maze2 = Room("maze2")
maze3 = Room("maze3")
maze4 = Room("maze4")
maze5 = Room("maze5")
maze6 = Room("maze6")
cavern = Room("cavern")
subway = Room("subway")
mineshaft = Room("mineshaft")
roman_ruins = Room("roman_ruins")
dwarven_mine = Room("dwarven_mine")
library = Room("library")
door = Room("door")
fortress = Room("fortress")
national_treasure = Room("national_treasure")
hole = Room("hole")
gutter = Room("gutter")

room_dict = {} 
item_list = []

for room in Room.room_list:  # create a dictionary with the names of rooms and their corresponding Room object
    room_dict.update({room.name:room})

# assign each room object their accessible rooms via cardinal directions
for index, row in room_csv.iterrows():      # iterate over each row in room_csv
    if index in room_dict:                  # use the file to retrieve room connections
        room = room_dict.get(index)
        try:
            room.set_directs(room_dict.get(row['North']),         
                            room_dict.get(row['East']),
                            room_dict.get(row['South']),
                            room_dict.get(row['West']),
                            room_dict.get(row['Up']),
                            room_dict.get(row['Down'])
                            )
            # if the cell isn't nan, set the cell to be the room's item.
            if not pd.isnull(row['Items']):
                room.items.append(row['Items'])
                item_list.append(row['Items'])
            # see if the room is a locked room
            if not pd.isnull(row['Locked']):
                room.locked = True
            # set the npc for the room
            if not pd.isnull(row['NPC']):
                room.npc = row['NPC']
            # set a description for if you have already visited
            if not pd.isnull(row['Description']):
                room.desc = row['Description']
            # have a separate explanation for each room if their first introduction does not work as such
            if not pd.isnull(row['Explanation']):
                Room.explain_room.update({room.name:row['Explanation']})
        except:
            print(f"ERROR: assigning room directions and items to [{index}]")
    else:
        print(f"ERROR: [{index}] not in room_dict")


# start the player at the first room
Player.loc = road1
# declare variables
directions = ('north', 'east', 'south', 'west', 'up', 'down')
rel_directions = ('forward', 'straight', 'right', 'back', 'backward', 'backwards', 'left',)
all_directions = directions + rel_directions
confused_replies = ("What?", "I don't understand that.",
                    "hm?", "I don't understand.")
dog_replies = ("You pet the dog. He really likes that.",
                    "The dog is happy.",
                    "\"bark!\"", "\"boof\"",
                    "*pant* *pant*", "\"barp!\"")
wolf_replies = ("You pet the wolf. He really likes that.",
                    "The wolf is happy.",
                    "\"bark!\"", "\"boof\"",
                    "*pant* *pant*", "\"barp!\"")
# I have the skeleton say random stuff when you approach him
skeleton_remarks = ("I think I forgot my pie in the oven.",
                    "I wonder if I can still grow a beard.",
                    "A talking toaster once gave me life advice about the meaning of toast.")
# magic words, some of which I found online
magic_words = ("abra ca dabra", "abracadabra", "abra cadabra",
               "expelliarmus", "expecto patronum", "sectumsempra",
               "lumos", "accio", "obliviate", "please")
main_intro = "Welcome to the Perfect Sewer Adventure! I will be your guide as you explore this small world.\n" +\
        "You can give me instructions for you to do things, like 'go north' or 'pick up ___'. You can travel cardinal directions,\n" +\
        "up and down, left and right, and other ways. You can not just say the name of a place. You have to say a direction. \n" +\
        "Some information given will be useful, where as other information may be useless. Say 'help' if you need more help. Good luck!" 
user_help = "You can type cardinal directions, up or down, names of items or npcs, relative directions, or pick up or use things.\n" +\
            "If you want me to describe a place again, you can say 'describe' or 'explain'.\n" +\
            "You can also view your inventory typing 'inv' or 'inventory'"

def get_nice_input(output = ''):
    """method for returning a nicely fromatted input"""
    return input(output).lower().strip(' .,!?')


def get_user_action():
    """Gets an input from the user and calls a variety of functions based on the input."""

    while not Player.loc == national_treasure: # end the game when the player is at the national_treasure room

        user_input = get_nice_input()   
        if user_input == '': continue # if the player didn't say anything, then restart the loop
        split_input = user_input.split() # use split to figure out the separate words that the user inputed
        try:
            # move
            if (split_input[0] == 'go' and user_input[3:] in all_directions) or user_input in all_directions:
                move(user_input) # if the player said 'go <direction>' or just '<direction>'
            # use item
            elif split_input[0] == 'use' and split_input[1] in Player.inv:
                use(split_input[1]) # for 'use <item>' or '<item>'
            elif user_input in Player.inv:
                use(user_input)
            # pick up item
            elif (split_input[0] == 'take' and split_input[1] in Player.loc.items):
                pick_up_item(split_input[1])
            elif (split_input[:2] == ['pick','up'] and split_input[2] in Player.loc.items):
                pick_up_item(split_input[2])
            elif user_input in Player.loc.items:
                pick_up_item(user_input)
            # pet dog
            elif user_input in ('pet', 'dog', 'pet dog', 'wolf', 'pet wolf') and Player.dog_tamed:
                random_output(dog_replies)
            elif user_input in ('tap drums', 'tap', 'play', 'drums') and Player.loc == music_room:
                print("You tapped the drums.")
            # describe location
            elif user_input in ('explain', 'describe'):
                Player.loc.intro(True) # use True to say the descriptive intro
            # npc interaction
            elif user_input == Player.loc.npc:
                interact_npc(Player.loc.npc)
            # check inventory
            elif user_input in ('inv','inventory','backpack'):
                if Player.inv:
                    print("Here is what is in your inventory:")
                    for item in Player.inv:
                        print(item)
                else: print("You don't have anything in your inventory.")
            # help player
            elif user_input == 'help' or split_input[0] == 'what':
                print(user_help)
            else:
                random_output(confused_replies)
        except IndexError:
            random_output(confused_replies)
            continue


def move(user_input):
    """Translate the user_input into a cardinal direction or up and down and then put the player there"""

    if user_input[:3] == "go ":
        user_input = (user_input[3:])       # if they said to "go <direction>", just ignore "go "
    if user_input in rel_directions:
        user_input = (Player.get_rel_direction(user_input))   # if they said a relative direction like 'forward', translate it
    room = Player.loc.get_room(user_input)  # retrieve the room object corresponding to the string
    if room == None:                        # if there isn't a room that way they can't go that way
        print(f"You cannot go that way.")   
        return                              
    if room.locked:                         # if the room is a locked room, they can't go that way
        room.intro()
        return
    if user_input not in ('up','down'):     # don't set the player's facing if they went up or down (I can't have them face up or down)
        Player.face(user_input)             # set the relative directions of the player
    Player.loc = room                       # move the player to the room
    Player.loc.intro()                      # play the intro to the room


def random_output(tuple_, end_ = "\n"):
    """Prints a message indicating that the player's input was not understood."""
    randInt = random.randint(0, len(tuple_) - 1)
    print(tuple_[randInt], end = end_)


def use(item):
    """use the item that the player said"""

    def use_notebook():
        """define the use cases for the notebook"""
        def notebook_read():
            """let the player read what is written in the notebook"""
            if Player.notebook_note:
                print("The notebook reads:\"" + Player.notebook_note + "\"")
            else:
                print("There is nothing written in the notebook.")

        def notebook_write():
            """let the player write down a string"""
            Player.notebook_note = input("What will you write down?\n")
            print("\"" + Player.notebook_note + "\" successfully written down.")

        # loop makes sure the player says write or read or asks them to repeat again
        print("Would you like to write or read in the notebook?")
        while True:
            user_input = get_nice_input()
            if user_input == 'write':
                notebook_write()
                break
            if user_input == 'read':
                notebook_read()
                break
            if user_input == 'stop':
                break
            print("Please type 'write' or 'read'.")
            
    def use_shovel():
        """if the player is on the playground, dig a hole to the cavern"""
        if Player.loc == playground:
            playground.down = cavern
            cavern.up = playground
            Player.inv.remove('shovel')
            print("""You dug a hole in the sand. It appears that there is a large area underneath the playground,\nbut it's hard to see where it goes. The shovel unfortunately broke.""")
            # fix room intros in case player goes backwards through maze
            sewer1.new = False # If the player goes backwards the description of the room doesn't make sense. The visited description works. I don't have the time to fix this properly.
            Room.new_room_intro.update({'maze3':'You are in a maze.'}) # this makes more sense
        else:
            print("You can't use that here.")

    def use_bone():
        """if the current location has the wolf, tame the wolf."""
        if Player.loc.npc == 'wolf':
            print("Congratulations! You give the bone to the wolf. He really likes it.")
            print("The wolf is now your pet dog. Please refer to him as 'dog' now.")
            Player.loc.npc = None
            Player.dog_tamed = True
        else:
            print("I don't know what you would do with that.")
        
    def use_key():
        """if the player is at the stream, use the key to unlock the gutter I guess"""
        if Player.loc == stream:
            print("The key works in the lock of the gutter.\nYou might be able to fit through the hole, but I don't know why you would go down there.")
            stream.down = sewer1
            sewer1.up = stream
        elif Player.loc == sewer1:
            print("The key unlocked the gutter. You can crawl up the ladder and get out now.")
            stream.down = sewer1
            sewer1.up = stream
        else:
            print("You can't use that here")
        

    # dictionary because each item has a different function
    use_item_dict = {
    'notebook':use_notebook,
    'shovel':use_shovel,
    'bone':use_bone,
    'key':use_key
    }

    if use_item_dict.get(item):
        use_item_dict.get(item)()
    else:
        print("You can't use that here.")


def pick_up_item(item):
    """put the item in the player's inventory and remove it from the room."""
    print(f"You picked up the {item}.")
    Player.inv.append(item)
    Player.loc.items.remove(item) # remove item from current room

    # if the player is magic, make the stick a wand
    if item == 'stick' and Player.magic:
        print("Your magic turned the stick into a wand!")
        Player.inv.append('wand')
        Player.inv.remove('stick')


def interact_npc(npc):
    """interact with the npcs"""
    def wolf_interaction():
        """interact with the dog"""
        random_output(wolf_replies)
        print("This wolf seems to be hungry.")
        if 'bone' in Player.inv:
            print("maybe you could give it your bone?")

    def dwarf_interaction():
        """If you have nitrobid, the dwarf will turn it into explosives to fight the skeleton with."""
        if 'nitrobid' in Player.inv:
            print("The dwarf extracted the nitroglycerin from your nitrobid without asking.")
            print("He gave you some of the explosives he made with it.")
            Player.inv.remove('nitrobid')
            Player.inv.append('explosives')
        else:
            print("The dwarf seemed interested in you until he found out you didn't have anything of value for him.")

    def wizard_interaction():
        """Interact with the wizard."""
        print("The wizard knows many things. However, he does not know why you would interrupt him in his studies.")
        print("Maybe if you can prove you are a wizard, he will do something for you.")
        print("Wizard: \"Are you a wizard?\"")
        print("1. n-no\n2. no")
        while True:
            user_input = get_nice_input()
            if user_input == '1' or user_input == '2' or user_input == 'no':
                break
            else:
                print("Please type one of the answers above.")
        print("Wizard: \"Then why do you bother me?\"")
        print("1. I want to become a wizard\n2. Sorry. I will leave you alone.")
        while True:
            user_input = get_nice_input()
            if user_input == '2':
                print("The wizard returns to his studies.")
                return
            if user_input == '1':
                break
            else:
                print("Please type one of the answers above.")
        user_input = get_nice_input("Wizard: \"In order to become a wizard, you must say the magic word(s)\"\n")
        if user_input not in magic_words:
            print("Wizard: \"I'm sorry, but you must not be a wizard. Goodbye.\"")
            return
        print("Wizard: \"You surely must be a wizard!")
        if 'stick' in Player.inv:
            print("Wizard: \"Here, it seems your wand is lacking.\"")
            print("Your stick was turned into a magic wand!")
            Player.inv.append('wand')
            Player.inv.remove('stick')
        print("You now feel some magic essence flowing in you. The wizard dissapeared.")
        Player.magic = True
        library.npc = None

    def skeleton_interaction():
        """have a "boss" fight with the skeleton."""

        def defeat_skeleton():
            """When you defeat the skeleton the door to the fortress unlocks.d"""
            time.sleep(4)
            print("The curse of the skeleton was released from the large door.")
            roman_ruins.npc = None
            cavern.south = fortress
            Room.new_room_intro.update({'cavern':"You are now in a cavern. To the north is a subway, to the east is the maze, to the south is a fortress, and to the west is a mineshaft."})
            cavern.new = True

        # Create a list containing only the items you can use if they are in the player's inventory
        items = [item for item in ['keytar', 'dog', 'explosives', 'stick', 'wand'] if item in Player.inv]

        # The player can use the dog if they have it
        if Player.dog_tamed:
            items.append('dog')

        # If the player doesn't have any items to fight the skeleton, don't let him be fought.
        if not items:
            print("I wouldn't approach the skeleton if I were you. You don't have anything to fight him with!")
            return

        print("*Boss music starts playing*")
        time.sleep(3)
        print(f"Skeleton: \"", end = "")
        random_output(skeleton_remarks, '')
        print("\"")
        time.sleep(4)
        print("The skeleton obviously wants to fight you. What will you do?")

        # Print each item that the player can use to tell the player what they can do.
        for count, item in enumerate(items, start=1):
            print(f"{count}. Use {item}")
        use_item = 0        # index for items list
        while True:
            user_input = input()
            if not user_input.isdigit():
                print("Please type one of the numbers that I stated above.")
                continue
            user_input = int(user_input) # turn the input into an integer to compare with <=
            if user_input <= len(items) and user_input > 0:
                use_item = items[user_input - 1] # use the item in the place on the list that the user specified
                break
            else:
                print("Please type one of the numbers that I stated above.")

        if use_item == 'dog':
            print("Your dog goes up and paws at the skeleton. he seems to be wanting some pets.")
            time.sleep(6)
            print("Your dog decides to grab one of the skeleton's bones and bring it back to you.")
            time.sleep(6)
            print("The skeleton falls apart and is defeated!")
        elif use_item == 'keytar':
            print("You play a major scale which clashes with the boss music!")
            time.sleep(6)
            print("The skeleton doesn't like it and is defeated!")
        elif use_item == 'explosives':
            print("You toss the explosives at the skeleton.")
            time.sleep(4)
            print("KABOOMSHSHKLLSKSHSSHSHSHhhhh") # explosion noise
            time.sleep(1)
            print("*clik*") # bones landing on the ground
            time.sleep(1)
            print("*lcunc*")
            time.sleep(1)
            print("The skeleton is defeated!")
        elif use_item == 'wand':
            print("You use a spell and turn the skeleton into rocks.")
            print("The skeleton has been defeated!")
        elif use_item == 'stick':
            print("nyeh")
            print("You threw the stick at the skeleton. He didn't seem to notice.")
            Player.inv.remove('stick')
            Player.loc.items.append('stick')
            time.sleep(4)
            Player.loc.intro(True)
            return
        defeat_skeleton()
        Player.loc.intro(True)

    npc_interaction_dict = {
        'wolf':wolf_interaction,
        'skeleton':skeleton_interaction,
        'dwarf':dwarf_interaction,
        'wizard':wizard_interaction
    }

    npc_interaction_dict.get(npc)()


def main():
    print()
    print(main_intro)
    print()
    Player.loc.intro()
    get_user_action()

if __name__ == "__main__":
    main()
