from sprite_object import *
from npc import *
from items import *


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.item_list = []
        self.npc_sprite_path = 'DimensionalLabirynth/resources/sprites/npc/'
        self.static_sprite_path = 'DimensionalLabirynth/resources/sprites/static_sprites/'
        self.anim_sprite_path = 'DimensionalLabirynth/resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}
        add_item = self.add_item

        # sprite map
        # add_sprite(SpriteObject(game))
        # add_sprite(AnimatedSprite(game))
        # add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        # add_sprite(AnimatedSprite(game, pos=(2.5, 2.5)))
        # add_sprite(AnimatedSprite(game, pos=(3.5, 3.5)))
        # add_sprite(AnimatedSprite(game, pos=(4.7, 4.9)))

        # npc map
        # add_npc(TrollNPC(game, pos=(tmp[0], tmp[1])))
        # [print(tmp[0], tmp[1]) for tmp in self.game.npc_troll_start_pos]
        tmp_list = set(self.game.candle_start_pos)
        for i in tmp_list:
            add_sprite(AnimatedSprite(game, pos=i))

        tmp_list = set(self.game.npc_troll_start_pos)
        for i in tmp_list:
            add_sprite(TrollNPC(game, pos=i))

        tmp_list = set(self.game.npc_gnome_start_pos)
        for i in tmp_list:
            add_sprite(GnomeNPC(game, pos=i))

        tmp_list = set(self.game.portal_pos)
        for i in tmp_list:
            add_item(Item(game, pos=i))

        # tmp_list = set(self.game.weapons_pos)
        # for i in tmp_list:
        #     add_item(WeaponItem(game, pos=i))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        [item.update() for item in self.item_list]

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_item(self, item):
        self.item_list.append(item)

    def empty_lists(self):
        self.sprite_list = []
        self.npc_list = []
        self.item_list = []

    def get_npc_list(self):
        return self.npc_list
