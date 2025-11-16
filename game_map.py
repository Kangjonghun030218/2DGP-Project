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
                (740, 650, 870, 1000),  # 왼쪽하늘
                (1050, 560, 1180, 1000),  # 오른쪽하늘
                (260, 270, 420, 400),  # 상자집
                (540, 380, 560, 400),  # 분수대
                (250, 450, 470, 600),  # 장비상점
                (520, 465, 700, 665),  # 상점
                (1050, 425, 1250, 525),  # 법사집
                (1300, 515, 1550, 850),  # 닌자집
                (1400, 250, 1650, 450),  # 우측하단 물레방아집
                (750, 300, 810, 540),  # 좌측벽
                (1050, 300, 1100, 380),  # 우측벽
                (1200, 0, 1800, 210),  # 우측하단
                (0, 0, 670, 210)  # 좌측하단
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