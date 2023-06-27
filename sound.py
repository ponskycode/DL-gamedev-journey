import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'DimensionalLabirynth/resources/sound/'
        self.weapon = pg.mixer.Sound(self.path + 'staff1.wav')
        self.npc_pain = pg.mixer.Sound(self.path + 'staff1.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'staff1.wav')
        self.npc_attack = pg.mixer.Sound(self.path + 'staff1.wav')
        self.player_pain = pg.mixer.Sound(self.path + 'staff1.wav')
        self.item_use = pg.mixer.Sound(self.path + 'staff1.wav')
        self.theme = pg.mixer.music.load(self.path + 'theme.mp3')
