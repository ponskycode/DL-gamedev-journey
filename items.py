from sprite_object import *
from random import randint, random, choice


class Item(AnimatedSprite):
    def __init__(self, game, path='DimensionalLabirynth/resources/items/portal/0.png', pos=(10.5, 5.5),
                 scale=1.2, shift=0.08, animation_time=180, size=10):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.idle_images = self.get_images(self.path + '/idle')
        self.use_images = self.get_images(self.path + '/use')

        self.size = size
        self.use_item = False
        self.ray_cast_value = False
        self.frame_counter = 0

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        if self.game.switch_2d:
            self.draw_ray_cast()

    def animate_use(self):
        if self.game.global_trigger and self.frame_counter < len(self.use_images) - 1:
            self.use_images.rotate(-1)
            self.image = self.use_images[0]
            self.frame_counter += 1

    def check_use(self):
        if self.ray_cast_value and self.game.player.attack:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.attack = False
                self.use_item = True
                self.game.new_game(self.game.player.health, self.game.player.hunger, self.game.player.kills)

    def run_logic(self):
        self.ray_cast_value = self.ray_cast_player_npc()
        self.check_use()
        if not self.use_item:
            self.animate(self.idle_images)
        else:
            self.animate_use()

    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

            # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    @property
    def map_pos(self):
        return int(self.x), int(self.y)


class WeaponItem(Item):
    def __init__(self, game, path='DimensionalLabirynth/resources/items/weapon/staff1/staff1-att1.png', pos=(10.5, 5.5),
                 scale=1.2, shift=0.08, animation_time=180, size=10):
        super().__init__(game, path, pos, scale, shift, animation_time, size)