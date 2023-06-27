import pygame as pg
import numpy as np
import random as rd
from npc import *

_ = False


class Map:
    def __init__(self, game, rooms_x=2, rooms_y=2, room_size=11, level=3):
        self.game = game
        self.portal = False
        self.room_size = room_size
        self.wall_types = level + 1
        self.rooms_x, self.rooms_y = rooms_x, rooms_y
        self.x = self.rooms_x * self.room_size
        self.y = self.rooms_y * self.room_size
        self.minimap = np.ones(shape=(self.x, self.y), dtype=int)
        self.rooms_sizes = np.zeros(shape=(self.rooms_x, self.rooms_y), dtype=int)
        self.world_map = {}
        self.generate_minimap()
        self.get_map()

    def generate_minimap(self, corridors_generated=7):
        self.map_rooms_gen()
        self.map_corridors_gen(corridors_generated)
        self.create_starter_room()
        self.print_minimap()

    def map_rooms_gen(self):
        for i in range(self.rooms_x):
            for j in range(self.rooms_y):
                # Middle of the current room
                curr_x = i * self.room_size + self.room_size // 2
                curr_y = j * self.room_size + self.room_size // 2

                # Room size
                curr_room_size = rd.randint(3, (self.room_size - 4) // 2 + 1)
                self.rooms_sizes[i, j] = curr_room_size

                # Coordinates of the room edges
                min_x = curr_x - curr_room_size
                max_x = curr_x + curr_room_size + 1
                min_y = curr_y - curr_room_size
                max_y = curr_y + curr_room_size + 1

                # Type of the room wall
                wall = rd.randint(1, self.wall_types)

                # Creating a square room
                for k in range(min_x, max_x):
                    for l in range(min_y, max_y):
                        # creates the room, curr_x, curr_y - middle of the room localization
                        # k, l - walks through every point belonging to the room
                        if (k == min_x or k == max_x - 1) or (l == min_y or l == max_y - 1):
                            self.minimap[k, l] = wall
                        else:
                            self.minimap[k, l] = _

    def map_corridors_gen(self, corridor_amount):
        earlier_dtn = 0
        room_x, room_y = 0, 0
        i = 0

        while i < corridor_amount:
            direction = rd.randint(0, 3)    # Randomises where to move
            curr_x = room_x * self.room_size + self.room_size // 2  # x and
            curr_y = room_y * self.room_size + self.room_size // 2  # y of the middle of the room

            # 0 - up, 1 - right, 2 - down, 3 - left
            if direction == earlier_dtn:
                i -= 1

            elif direction == 0:
                dtn = [1, 0, 0, 0]
                if not room_y - 1 < 0:
                    room_y -= 1
                    if not self.rooms_sizes[room_x, room_y] == 0:
                        self.create_encounter(self.rooms_sizes[room_x, room_y], curr_x, curr_y, room_x, room_y)
                        self.rooms_sizes[room_x, room_y] == 0
                    i += 1
                    self.map_one_corridor(curr_x, curr_y, dtn)
                    # print(curr_x, curr_y)

                else:
                    i -= 1

            elif direction == 1:
                dtn = [0, 1, 0, 0]
                if not room_x + 1 > self.rooms_x - 1:
                    room_x += 1
                    if not self.rooms_sizes[room_x, room_y] == 0:
                        self.create_encounter(self.rooms_sizes[room_x, room_y], curr_x, curr_y, room_x, room_y)
                        self.rooms_sizes[room_x, room_y] == 0
                    i += 1
                    self.map_one_corridor(curr_x, curr_y, dtn)
                    # print(curr_x, curr_y)
                else:
                    i -= 1

            elif direction == 2:
                dtn = [0, 0, 1, 0]
                if not room_y + 1 > self.rooms_y - 1:
                    room_y += 1
                    if not self.rooms_sizes[room_x, room_y] == 0:
                        self.create_encounter(self.rooms_sizes[room_x, room_y], curr_x, curr_y, room_x, room_y)
                        self.rooms_sizes[room_x, room_y] == 0
                    i += 1
                    self.map_one_corridor(curr_x, curr_y, dtn)
                    # print(curr_x, curr_y)
                else:
                    i -= 1

            elif direction == 3:
                dtn = [0, 0, 0, 1]
                if not room_x - 1 < 0:
                    room_x -= 1
                    if not self.rooms_sizes[room_x, room_y] == 0:
                        self.create_encounter(self.rooms_sizes[room_x, room_y], curr_x, curr_y, room_x, room_y)
                        self.rooms_sizes[room_x, room_y] == 0
                    i += 1
                    self.map_one_corridor(curr_x, curr_y, dtn)
                    # print(curr_x, curr_y)
                else:
                    i -= 1
            earlier_dtn = direction

    def map_one_corridor(self, beg_x, beg_y, dtn=[1, 0, 0, 0]):
        # dtn = ['UP', 'RIGHT', 'DOWN', 'LEFT']

        for i in range(self.room_size + 1):
            tmp_x = beg_x + i * dtn[1] - i * dtn[3]
            tmp_y = beg_y - i * dtn[0] + i * dtn[2]
            self.minimap[tmp_x, tmp_y] = _

    def create_encounter(self, curr_room_size, curr_x, curr_y, room_x, room_y):
        if not (room_x == 0 and room_y == 0):
            curr_x = room_x * self.room_size + self.room_size // 2
            curr_y = room_y * self.room_size + self.room_size // 2
            min_x = curr_x - curr_room_size
            max_x = curr_x + curr_room_size + 1
            min_y = curr_y - curr_room_size
            max_y = curr_y + curr_room_size + 1
            # print(room_x, room_y)
            # print('\n')

            # Make this into item roll- room edges
            if rd.randint(1, 4) == 1:
                pass
                # self.game.weapons_pos.append((min_x + 1.5, min_y + 1.5))
            else:
                self.game.candle_start_pos.append((min_x + 1.5, min_y + 1.5))
            self.game.candle_start_pos.append((max_x - 2.5, min_y + 1.5))
            self.game.candle_start_pos.append((min_x + 1.5, max_y - 2.5))
            self.game.candle_start_pos.append((max_x - 2.5, max_y - 2.5))
            # self.minimap[min_x + 1, min_y + 1] = 3
            # self.minimap[max_x - 2, min_y + 1] = 3
            # self.minimap[min_x + 1, max_y - 2] = 3
            # self.minimap[max_x - 2, max_y - 2] = 3

            # Make this into monster roll
            self.game.npc_troll_start_pos.append((min_x + 2.5, min_y + 1.5))
            self.game.npc_gnome_start_pos.append((max_x - 2.5, min_y + 2.5))
            self.game.npc_troll_start_pos.append((min_x + 1.5, max_y - 3.5))
            self.game.npc_gnome_start_pos.append((max_x - 3.5, max_y - 2.5))
            # self.minimap[min_x + 2, min_y + 1] = 4
            # self.minimap[max_x - 2, min_y + 2] = 4
            # self.minimap[min_x + 1, max_y - 3] = 4
            # self.minimap[max_x - 3, max_y - 2] = 4

            if not (room_x == 0 and room_y == 0) and not self.portal:  # Place portal item
                # print(room_x, room_y)
                # print(curr_x, curr_y)
                self.game.portal_pos.append((curr_x+1.5, curr_y+1.5))
                # self.minimap[curr_x+1, curr_y+1] = 3
                self.portal = True

    def create_starter_room(self):
        # Place player
        # self.minimap[self.room_size // 2, self.room_size // 2] = 1

        # Place visual- candles
        self.game.candle_start_pos.append((self.room_size // 2 - 0.5, self.room_size // 2 - 0.5))
        self.game.candle_start_pos.append((self.room_size // 2 - 0.5, self.room_size // 2 + 1.5))
        self.game.candle_start_pos.append((self.room_size // 2 + 1.5, self.room_size // 2 - 0.5))
        self.game.candle_start_pos.append((self.room_size // 2 + 1.5, self.room_size // 2 + 1.5))
        # self.minimap[self.room_size // 2 - 1, self.room_size // 2 - 1] = 2
        # self.minimap[self.room_size // 2 - 1, self.room_size // 2 + 1] = 2
        # self.minimap[self.room_size // 2 + 1, self.room_size // 2 - 1] = 2
        # self.minimap[self.room_size // 2 + 1, self.room_size // 2 + 1] = 2

    def print_minimap(self):
        print(np.matrix(self.minimap))
        print('\n')
        print(np.matrix(self.rooms_sizes))
        print('\n')

    def get_map(self):
        for j, row in enumerate(self.minimap):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1]*100, 100, 100), 2)
        for pos in self.world_map]

# _ = False
# mini_map = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#     [1, _, _, 1, 1, 1, _, _, _, _, _, 1, _, 1],
#     [1, _, _, _, _, _, _, _, 2, 2, _, _, _, 1],
#     [1, _, _, _, _, _, _, _, _, 2, _, _, _, 1],
#     [1, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#     [1, _, _, _, 1, _, _, _, _, _, _, _, _, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]
#
# class Map:
#     def __init__(self, game, level=1):
#         self.game = game
#         self.mini_map = mini_map
#         self.world_map = {}
#         self.get_map()
#
#     def get_map(self):
#         for j, row in enumerate(self.mini_map):
#             for i, value in enumerate(row):
#                 if value:
#                     self.world_map[(i, j)] = value
#
#     def draw(self):
#         [pg.draw.rect(self.game.screen, 'darkgray', w]
