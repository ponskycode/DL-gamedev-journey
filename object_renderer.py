import pygame as pg
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('DimensionalLabirynth/resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.floor_image = self.get_texture('DimensionalLabirynth/resources/textures/floor.png', (WIDTH, HALF_HEIGHT))
        self.blood_screen = self.get_texture('DimensionalLabirynth/resources/textures/blood_screen.png', RES)
        self.wait_screen = self.get_texture('DimensionalLabirynth/resources/textures/wait.png', RES)
        self.digit_size = 80
        self.health_digit_images = [self.get_texture(f'DimensionalLabirynth/resources/textures/health_digit/{i}.png', [self.digit_size] * 2)
                                    for i in range(11)]
        self.health_digits = dict(zip(map(str, range(11)), self.health_digit_images))
        self.hunger_digit_images = [self.get_texture(f'DimensionalLabirynth/resources/textures/hunger_digit/{i}.png', [self.digit_size] * 2)
                                    for i in range(11)]
        self.hunger_digits = dict(zip(map(str, range(11)), self.hunger_digit_images))
        self.kills_digit_images = [self.get_texture(f'DimensionalLabirynth/resources/textures/kills_digit/{i}.png', [self.digit_size//2] * 2)
                                   for i in range(11)]
        self.kills_digits = dict(zip(map(str, range(11)), self.kills_digit_images))
        self.game_over_image = self.get_texture('DimensionalLabirynth/resources/textures/game_over.png', RES)
        self.game_overlay = self.get_texture('DimensionalLabirynth/resources/textures/overlay.png', RES)
        draw_wait = self.draw_wait()

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_player_hunger()
        self.draw_player_kills()
        self.screen.blit(self.game_overlay, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.health_digits[char], (20 + i * self.digit_size, 10))
        self.screen.blit(self.health_digits['10'], (20 + (i + 1) * self.digit_size, 10))

    def draw_player_hunger(self):
        hunger = str(self.game.player.hunger)
        for i, char in enumerate(hunger):
            self.screen.blit(self.hunger_digits[char], (20 + i * self.digit_size, 30 + self.digit_size))
        self.screen.blit(self.hunger_digits['10'], (20 + (i + 1) * self.digit_size, 30 + self.digit_size))

    def draw_player_kills(self, x=1450, y=800):
        kills = str(self.game.player.kills)
        for i, char in enumerate(kills):
            self.screen.blit(self.kills_digits[char], (x + i * self.digit_size, y))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_wait(self):
        self.screen.blit(self.wait_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        self.screen.blit(self.floor_image, (-self.sky_offset, 540))
        self.screen.blit(self.floor_image, (-self.sky_offset + WIDTH, 540))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('DimensionalLabirynth/resources/textures/wall1.png'),
            2: self.get_texture('DimensionalLabirynth/resources/textures/wall2.png'),
            3: self.get_texture('DimensionalLabirynth/resources/textures/wall3.png'),
            4: self.get_texture('DimensionalLabirynth/resources/textures/wall4.png')
        }