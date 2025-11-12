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

        if self.map_number == 1:
            self.collision_boxes = [
                (850, 200, 1020, 230),
                (260, 270, 420, 400),  # 상자집
                (540, 380, 560, 400),  # 분수대
                (250, 400, 420, 600),  # 장비상점
                (520, 465, 700, 665),  # 상점
                (1050, 425, 1250, 525),  # 법사집
                (1300, 550, 1550, 850),  # 닌자집
                (1450, 250, 1650, 450)  # 우측하단 물레방아집
            ]

    def draw(self, cam_x, cam_y):
        screen_x = self.world_x - cam_x
        screen_y = self.world_y - cam_y
        self.image.draw(screen_x, screen_y)
        self.draw_debug_boxes(cam_x, cam_y)

    def get_collision_boxes(self):
        return self.collision_boxes

    def draw_debug_boxes(self, cam_x, cam_y):
        for l, b, r, t in self.collision_boxes:
            sl = l - cam_x-20
            sb = b - cam_y-20
            sr = r - cam_x+20
            st = t - cam_y+20
            draw_rectangle(sl, sb, sr, st)

    def update(self):
        pass