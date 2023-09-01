#https://github.com/Johannes1803/Text-based-adventure-game/blob/master/rpg/room.py
class Room:

    def __init__(self, room_name):
        self.name = room_name
        self.description = None
        self.linked_rooms = {}
        self.character = None
        self.item = None

    def set_description(self, room_description):
        """Sets the description of the room as a string"""
        self.description = room_description

    def get_description(self):
        """Returns a string containing the description of the room"""
        return self.description

    def set_name(self, name):
        """ Sets the name of the room as a string"""
        self.name = name

    def get_name(self):
        """Returns a string containing the name of the room"""
        return self.name

    def describe(self):
        """Prints a string describung the room to the console"""
        print(self.description)

    def link_room(self, room_to_link, direction):
        """Links the room the other room given as input in the specified direction, """
        self.linked_rooms[direction] = room_to_link
        # print(self.name + " linked rooms :" + repr(self.linked_rooms))

    def get_details(self):
        """Returns a string describing the linked rooms and their directions"""
        self.describe()
        for direction in self.linked_rooms:
            room = self.linked_rooms[direction]
            print("The " + room.get_name() + " is " + direction)

    def move(self, direction):
        """Returns the room in the given direction, or returns the current room if there is no such room"""
        if direction in self.linked_rooms:
            return self.linked_rooms[direction]
        else:
            print("You cant go that way")
            return self

    def set_character(self, character):
        """Sets the Character object in the room"""
        self.character = character

    def get_character(self):
        """Returns the character object in the room"""
        return self.character

    def set_item(self, item):
        """Sets the item object in the room"""
        self.item = item

    def get_item(self):
        """Returns the item object in the room"""
        return self.item

class Character():

    # Create a character
    def __init__(self, char_name, char_description):
        self.name = char_name
        self.description = char_description
        self.conversation = None

    # Describe this character
    def describe(self):
        """Prints a string describing the character to the console"""
        print(self.name + " is here!")
        print(self.description)

    # Set what this character will say when talked to
    def set_conversation(self, conversation):
        """Sets the conversation attribute of the character to the given string"""
        self.conversation = conversation

    # Talk to this character
    def talk(self):
        """Prints the conversation string of the character to the console"""
        if self.conversation is not None:
            print("[" + self.name + " says]: " + self.conversation)
        else:
            print(self.name + " doesn't want to talk to you")

    # Fight with this character
    def fight(self, combat_item):
        """Returns True and prints string about fight message to console"""
        print(self.name + " doesn't want to fight with you")
        return True


class Enemy(Character):
    dead_enemies: int = 0

    def __init__(self, char_name, char_description):
        super().__init__(char_name, char_description)
        self.weakness = None

    def set_weakness(self, weakness):
        """Sets a string containing the weekness of the enemy"""
        self.weakness = weakness

    def get_weakness(self):
        """Returns a string containing the weekness of the enemy"""
        return self.weakness

    def fight(self, combat_item):
        """Returns a boolean, True if you won the fight, false otherwise"""
        if combat_item == self.weakness:
            print("You fend " + self.name + " off with the " + combat_item)
            Enemy.dead_enemies += 1
            print(Enemy.dead_enemies)
            return True
        else:
            print(self.name + " crushes you, puny adventurer")
            return False

    def get_dead_enemies(self):
        """Returns an int reflecting the number of dead enemies"""
        return self.dead_enemies


class Friend(Character):
    def __init__(self, char_name, char_description):
        super().__init__(char_name, char_description)
        self.hugReady = True

    def hug(self):
        """Returns a boolean, True if Character wants to be hugged, False otherwise"""
        if self.hugReady:
            print(self.name + " hugs you!")
            return True
        else:
            print(self.name + " does not hug you!")
            return False


class Item():
    def __init__(self, name):
        self.name = name
        self.description = None

    def set_name(self, name):
        """Sets the name attribute of the item to the given String"""
        self.name = name

    def get_name(self):
        """returns a string containing the name of the item"""
        return self.name

    def set_description(self, description):
        """Sets the description attribute of the item to the given String"""
        self.description = description

    def get_description(self):
        """Returns a string containing the description of the item"""
        return self.description

    def describe(self):
        """Prints a string describing the item to the console"""
        print(self.get_name())
        print(self.get_description())


# number of enemies to defeat before victory
to_be_killed = 2

# Define the map

# define rooms
kitchen = Room("Kitchen")
kitchen.set_description("A dank and dirty room buzzing with flies.")

ballroom = Room("Ballroom")
ballroom.set_description("Where we chill, yo!")

dining_hall = Room("Dining hall")
dining_hall.set_description("The room where we eat delicious meals!")

kitchen.link_room(dining_hall, "south")
ballroom.link_room(dining_hall, "east")
dining_hall.link_room(kitchen, "north")
dining_hall.link_room(ballroom, "west")

current_room = kitchen

# add items
sword = Item("sword")
sword.set_name("excalibur")
# sword.get_name()
sword.set_description("sword of King Arthur")
# sword.get_description()
# put sword in kitchen
kitchen.set_item(sword)

cucumber = Item("Cucumber")
cucumber.set_name("cucumber")
cucumber.set_description("A delicious vegetable!")
dining_hall.set_item(cucumber)
# add a character
dave = Enemy("Dave", "A smelly zombie")
dave.set_conversation("Oink Oink")
dave.set_weakness("excalibur")

# put character dave in dining hall
dining_hall.set_character(dave)
# Add a new enemy
pete = Enemy("Pete", "a nasty wizard")
pete.set_conversation("Hokus Pokus")
pete.set_weakness("cucumber")
ballroom.set_character(pete)

# Add a new character
catrina = Friend("Catrina", "a friendly skeleton")
catrina.set_conversation("Hello there.")
kitchen.set_character(catrina)

dead = False
backpack = []

# the game loop
while not dead:
    print("\n")
    # describe state of room you are in
    current_room.get_details()
    inhabitant = current_room.get_character()
    if inhabitant is not None:
        inhabitant.describe()
    item = current_room.get_item()
    if item is not None:
        item.describe()
        backpack.append(item.get_name())
        current_room.set_item(None)
    # listen to user input
    command = input("> ")
    if command in ["north", "south", "east", "west"]:
        # Move in the given direction
        current_room = current_room.move(command)
    elif command == "talk":
        # talk to current inhabitant -check whether there is one
        if inhabitant is not None:
            inhabitant.talk()
    elif command == "fight":
        # fight with inhabitant if there is one
        if inhabitant is not None:
            print("What will you fight with?")
            fight_with = input()
            # do you have the item you want to fight with in your bag?
            if fight_with in backpack:
                # Fight won?
                won_fight = inhabitant.fight(fight_with)
                if not won_fight:
                    dead = True  # You die. Game over
                else:
                    try:
                      if inhabitant.get_dead_enemies() >= to_be_killed:
                          print("You win")  # you killed enough enemies to win the game
                          dead = True
                    except:
                      pass
                    current_room.set_character(None)
            else:
                print("This item is not in your backpack")
        else:
            print("There is no one here to fight with!")

    elif command == "hug":
        if inhabitant is not None:
            if isinstance(inhabitant, Enemy):
                print("bad Idea")
            elif isinstance(inhabitant, Friend):
                inhabitant.hug()