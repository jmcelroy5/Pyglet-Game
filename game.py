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

#### Put class definitions here ####
class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acuired a gem! You have %d items!" %(len(player.inventory)))

class EnemyBug(GameElement):
    IMAGE = "EnemyBugR"
    SOLID = True
    ENEMY = True
    direction = 1

    def interact(self, player):
        GAME_BOARD.change_health(-1)
        GAME_BOARD.draw_msg("Ow! Your strength is at %r." % GAME_BOARD.player_health)

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

        existing_el = self.board.get_el(next_x, self.y)

        if hasattr(existing_el,"GIRL"):
            existing_el.board.del_el(existing_el.x, existing_el.y)
            existing_el.board.set_el(1,1, existing_el)
            GAME_BOARD.player_health -= 1
 
        self.board.del_el(self.x, self.y)
        self.board.set_el(next_x, self.y, self)

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Tree(GameElement):
    IMAGE = "ShortTree"
    SOLID = True

class Wall(GameElement):
    IMAGE = "StoneBlock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Princess"
    SOLID = True
    GIRL = True
    
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
        self.health = GAME_BOARD.player_health

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

        self.board.draw_msg("[%s] moves %s." %(self.IMAGE, direction) )

        if direction:
            next_location = self.next_pos(direction)
            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]

                if 0 <= next_x < GAME_WIDTH and 0 <= next_y < GAME_HEIGHT: 

                    existing_el = self.board.get_el(next_x, next_y)

                    if existing_el:
                        existing_el.interact(self)

                    if hasattr(existing_el, "ENEMY"):
                        self.board.draw_msg("OW! Dang that hurt.")
                        self.board.del_el(self.x, self.y)
                        self.board.set_el(1, 1, self)

                    if existing_el and existing_el.SOLID:
                        self.board.draw_msg("AHH! There is something in my way.")

                    elif existing_el is None or not existing_el.SOLID:
                        self.board.del_el(self.x, self.y)
                        self.board.set_el(next_x, next_y, self)
                else:
                    self.board.draw_msg("You can't go that way!")
                    

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    wall_positions = [
        (2,0),
        (2,1),
        (2,2),
        (2,3),
        (3,3),
        (4,3),
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

    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(1,1,player)
    print player

    bug_positions = [
        (0,5)
    ]

    bugs = []

    for pos in bug_positions:
        bug = EnemyBug()
        GAME_BOARD.register(bug)
        GAME_BOARD.set_el(pos[0],pos[1], bug)
        bugs.append(bug)

    # gem_positions = [
    #     (3,1),
    #     (0,3)
    # ]

    # gems = []

    # for pos in gem_positions:  
    #     gem = Gem()
    #     GAME_BOARD.register(gem)
    #     GAME_BOARD.set_el(pos[0],pos[1],gem)
    #     gems.append(gem)

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
