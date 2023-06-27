from sprite_object import *


class Weapon(AnimatedSprite):
    def __init__(self, game, base_damage=50, path='DimensionalLabirynth/resources/sprites/weapon/staff1/staff1-att1.png', scale=1.0, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.cooldown = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = base_damage + self.player.kills // 5

    def animate_attack(self):
        if self.cooldown:
            self.game.player.attack = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.cooldown = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_attack()


class Tier1Weapon(Weapon):
    def __init__(self, game, base_damage=40, path='DimensionalLabirynth/resources/sprites/weapon/staff1/staff1-att1.png'
                 , scale=2.5, animation_time=90):
        super().__init__(game, base_damage, path, scale, animation_time)


class Tier2Weapon(Weapon):
    def __init__(self, game, base_damage=50, path='DimensionalLabirynth/resources/sprites/weapon/staff1/staff1-att1.png'
                 , scale=2.5, animation_time=90):
        super().__init__(game, base_damage, path, scale, animation_time)


class Tier3Weapon(Weapon):
    def __init__(self, game, base_damage=60, path='DimensionalLabirynth/resources/sprites/weapon/staff1/staff1-att1.png'
                 , scale=2.5, animation_time=90):
        super().__init__(game, base_damage, path, scale, animation_time)
