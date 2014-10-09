import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 6
GAME_HEIGHT = 6

#### Put class definitions here ####
class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acuired a gem! You have %d items!" %(len(player.inventory)))

class EnemyBug(GameElement):
    IMAGE = "EnemyBug"
    SOLID = False

    def interact(self, player):
        #hurt the player.
        player.health -= 1
        GAME_BOARD.draw_msg("Ow! Your strength is at %r." % player.health)


class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Princess"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
        self.health = 5

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
                board_restrict = [-1, 6, 6]

                # if next_x < 0 or next_x >= GAME_WIDTH or next_y < 0 or next_y >= GAME_HEIGHT:
                #     self.board.draw_msg("I can't go that way! I'll fall off.")
                #     self.board.del_el(self.x, self.y)
                #     self.board.set_el(self.x, self.y, self)

                existing_el = self.board.get_el(next_x, next_y)

                if next_x or next_y in board_restrict:
                    self.board.draw_msg("AHH! There is something in my way.")
                    out_of_bounds = True

                if existing_el:
                    existing_el.interact(self)

                if existing_el and existing_el.SOLID:
                    self.board.draw_msg("AHH! There is something in my way.")

                elif existing_el is None or not existing_el.SOLID or not out_of_bounds:
                    self.board.del_el(self.x, self.y)
                    self.board.set_el(next_x, next_y, self)
                    

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
        (2,1),
        (1,2),
        (3,2),
        (2,3)
    ]

    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0],pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(2,2, player)
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

    gem_positions = [
        (3,1),
        (0,3)
    ]

    gems = []

    for pos in gem_positions:  
        gem = Gem()
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0],pos[1],gem)
        gems.append(gem)
