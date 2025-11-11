from pico2d import *

class GameMap:
    def __init__(self, map_number=0):
        self.map1_image = load_image('map_1.png')
        self.map2_image = load_image('map_2.png')
        self.map_number = map_number

        if self.map_number == 1:
            self.image = self.map1_image
        elif self.map_number == 2:
            self.image = self.map2_image
        else:
             self.image = self.map1_image


        self.width = self.image.w
        self.height = self.image.h
        self.world_x = self.width // 2
        self.world_y = self.height // 2

    def draw(self, cam_x, cam_y):
        screen_x = self.world_x - cam_x
        screen_y = self.world_y - cam_y
        self.image.draw(screen_x, screen_y)

    def update(self):
        pass