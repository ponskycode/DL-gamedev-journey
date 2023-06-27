import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

# from settings import *


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.level = 1
        self.dungeon_level = 1
        self.global_trigger = False
        self.switch_2d = False
        self.global_event = pg.USEREVENT + 0
        self.sprite_start_pos = []
        self.npc_troll_start_pos = []
        self.npc_gnome_start_pos = []
        self.candle_start_pos = []
        self.portal_pos = []
        self.weapons_pos = []
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self, curr_hp=100, curr_hun=100, kills=0):
        self.map = Map(self)
        self.player = Player(self)
        self.player.kills = kills
        self.player.health = curr_hp
        self.player.hunger = curr_hun
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Tier1Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        # self.static_sprite = SpriteObject(self)
        # self.animated_sprite = AnimatedSprite(self)

    # def next_level(self):
    #     self.dungeon_level += 1
    #     self.map = Map(self)
    #     self.object_handler = ObjectHandler(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        # self.static_sprite.update()
        # self.animated_sprite.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.switch_2d = False
        if self.switch_2d:
            self.draw_2d()
        else:
            self.draw_3d()

    def draw_2d(self):
        self.screen.fill('black')
        self.map.draw()
        self.player.draw()

    def draw_3d(self):
        self.object_renderer.draw()
        self.weapon.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.K_TAB:
                self.switch_2d = not self.switch_2d
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_attack_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
