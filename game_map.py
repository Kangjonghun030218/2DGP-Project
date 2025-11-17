from pico2d import *
import resource_manager
import config


class GameMap:
    def __init__(self, map_number=0):
        self.map1_image = resource_manager.get_image('map_1')
        self.map2_image = resource_manager.get_image('map_2')
        self.map_number = map_number
        self.collision_boxes = []

        if self.map_number == 1:
            self.image = self.map1_image
        elif self.map_number == 2:
            self.image = self.map2_image
        else:
            self.image = self.map1_image

        self.debug_mode = config.DEBUG_MODE_ON

        self.width = self.image.w
        self.height = self.image.h
        self.world_x = self.width // 2
        self.world_y = self.height // 2

        if self.map_number == 1:
            self.collision_boxes = [
                (1000, 800, 1180, 2000),  # 왼쪽 하늘
                (700, 500, 800, 600),  # 분수대
                (600, 600, 1000, 2000),  # 상점으로 부터 위쪽
                (1000, 350, 1080, 700),  # 상점 옆쪽 벽
                (1080, 500, 1170, 580),  # 상점 옆쪽 벽 옆 돌
                (1400, 500, 1680, 2000),  # 법사집
                (1680, 600, 1900, 2000),  # 닌자집
                (1900, 200, 3000, 2000),  # 우측하단 물레방아집부터 위쪽
                (1180, 900, 1400, 2000),  #중앙하늘
                (800, 200, 880, 400),  # 좌측벽
                (1450, 0, 3000, 200),  # 우측하단
                (0, 200, 800, 350),  # 좌측하단 위쪽
                (0, 350, 600, 2000),# 좌측하단 위쪽 위쪽
                (1600, 200, 1900, 350),  # 우측벽 윗쪽
                (1400, 350, 1500, 500),  #
                (1250, 550, 1400, 720),  #
                (1800, 500, 1900, 600),  #
                (0, 0, 1000, 200)  # 좌측하단
            ]
        elif self.map_number == 2:
            pass

    def draw(self, cam_x, cam_y):
        screen_x = self.world_x - cam_x
        screen_y = self.world_y - cam_y
        self.image.draw(screen_x, screen_y)

        if self.debug_mode:
            self.draw_debug_boxes(cam_x, cam_y)

    def get_collision_boxes(self):
        return self.collision_boxes

    def draw_debug_boxes(self, cam_x, cam_y):
        for l, b, r, t in self.collision_boxes:
            sl = l - cam_x
            sb = b - cam_y
            sr = r - cam_x
            st = t - cam_y
            draw_rectangle(sl, sb, sr, st)

    def update(self):
        pass