import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 8
GAME_HEIGHT = 6

### PARENT CLASSES (inherit from GameElement class) ###

class Character(GameElement):

    def __init__(self):
        self.inventory = []
        self.health = GAME_BOARD.player_health
        self.SOLID = True

class Enemy(GameElement):
    """Game board elements that harm player"""

    SOLID = True

    def interact(self, player):
        GAME_BOARD.change_health(-1)
        GAME_BOARD.draw_msg("OUCH! That hurt. Your strength is at %r." % GAME_BOARD.player_health)

    def check_for_character(self, next_x, next_y):
        existing_el = self.board.get_el(next_x, next_y)

        if isinstance(existing_el, Character):
            existing_el.board.del_el(existing_el.x, existing_el.y)
            existing_el.board.set_el(1,1, existing_el)
            GAME_BOARD.change_health(-1)
            GAME_BOARD.draw_msg("OUCH! That hurt. Your strength is at %r." % GAME_BOARD.player_health)
 
        self.board.del_el(self.x, self.y)
        self.board.set_el(next_x, self.y, self)

class Barrier(GameElement):
    """Game board elements that block player movement"""
    SOLID = True

    def interact(self, player):
        self.board.draw_msg("There is something in my way.")

class Reward(GameElement):
    """Elements that increase player life"""
    
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a %s! You have %d items!" %(self.reward_type, len(player.inventory)))

class Inventory(GameElement):
    """Elements that player acquires for later use"""

    SOLID = False


### SUB CLASSES ###

class Gem(Reward):
    IMAGE = "OrangeGem"
    reward_type = "gem"

class EnemyBug(Enemy):
    IMAGE = "EnemyBugR"
    direction = 1

    def update(self, dt):

        next_x = self.x + self.direction

        if next_x < 0:
            self.change_image("EnemyBugR")
            self.direction *=- 1
            next_x = self.x
        if next_x >= self.board.width:
            self.change_image("EnemyBugL")
            self.direction *=- 1
            next_x = self.x

        self.check_for_character(next_x, self.y)

class Rock(Barrier):
    IMAGE = "Rock"
    SOLID = True

class Tree(Barrier):
    IMAGE = "ShortTree"
    SOLID = True

class Wall(Barrier):
    IMAGE = "StoneBlock"
    SOLID = True

class Key(Inventory):
    IMAGE = "Key"
    SOLID = False

    def interact(self, player):
        GAME_BOARD.draw_msg("You have the key! Go find the treasure chest.")
        player.hasKey = True

class Treasure(GameElement):
    IMAGE = "Chest"
    SOLID = True

    def interact(self,player):
        if player.hasKey == True:
            self.change_image("OpenChest")
            self.board.del_el(self.x,self.y,self)
            win_gem = Gem()
            GAME_BOARD.register(win_gem)
            self.board.set_el(3,2,win_gem)


class Player1(Character): 
    IMAGE = "Princess"
    hasKey = False
        
    def next_pos(self, direction):

        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

    def keyboard_handler(self, symbol, modifier):
        direction = None
        if symbol == key.UP:
            direction = "up"
        elif symbol == key.DOWN:
            direction = "down"
        elif symbol == key.RIGHT:
            direction = "right"
        elif symbol == key.LEFT:
            direction = "left"

        self.board.draw_msg("%s moves %s." %(self.IMAGE, direction))

        if direction:
            next_location = self.next_pos(direction)
            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]

                if 0 <= next_x < GAME_WIDTH and 0 <= next_y < GAME_HEIGHT: 

                    existing_el = self.board.get_el(next_x, next_y)

                    if existing_el:
                        existing_el.interact(self)

                    if isinstance(existing_el, Enemy):
                        self.board.del_el(self.x, self.y)
                        self.board.set_el(1, 1, self)

                    elif existing_el is None or not existing_el.SOLID:
                        self.board.del_el(self.x, self.y)
                        self.board.set_el(next_x, next_y, self)
                else:
                    self.board.draw_msg("You can't go that way!")   # out of bounds

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    wall_positions = [
        (2,0),
        (2,1),
        (2,2),
        (2,3),
        (2,4),
        (3,4),
        (4,4),
        (5,2),
        (5,3),
        (5,4),
    ]

    walls = []

    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0],pos[1], wall)
        walls.append(wall)

    #rocks[-1].SOLID = False

    player = Player1()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(1,2,player)

    bug_positions = [
        (0,5)
    ]

    bugs = []

    for pos in bug_positions:
        bug = EnemyBug()
        GAME_BOARD.register(bug)
        GAME_BOARD.set_el(pos[0],pos[1], bug)
        bugs.append(bug)

    chest = Treasure()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(3,1, chest)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(7,4, key)

    # gem_positions = [
    #     (0,0)
    # ]

    gems = []

    # for pos in gem_positions:  
    win_gem = Gem()
    GAME_BOARD.register(win_gem)
    # gems.append(win_gem)

    tree_positions = [
        (3,0),
        (4,0),
        (5,0),
        (6,0),
        (7,0),
    ]

    trees = []

    for pos in tree_positions:  
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0],pos[1],tree)
        trees.append(tree)
