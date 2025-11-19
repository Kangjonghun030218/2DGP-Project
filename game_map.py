from pico2d import *
import resource_manager
import config
import knight


class GameMap:
    def __init__(self, map_number=0):
        self.map1_image = resource_manager.get_image('map_1')
        self.map2_image = resource_manager.get_image('map_2')

        self.portal_image = resource_manager.get_image('portal')
        self.map_number = map_number
        self.portal_x = 1257
        self.portal_y = 196
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
            self.collision_boxes = [
                (850, 0, 4500, 1000),  # 1. 맵 상단 전체 (숲/절벽)
                (2063, 2050, 3284, 3050),  # 2. 절벽 구간
                (3284, 2500, 4500, 3050),  # 3. 절벽 구간 우측
                (3726, 2200, 4500, 2500),  # 4. 절벽 구간 우측 아래
                (4326, 1700, 4500, 2500),  # 5. 절벽 구간 우측 아래 아래
                (49096, 1220, 4500, 1700),  # 6. 절벽 구간 우측 아래 아래 아래
                (3950, 920, 4500, 1220),  # 7. 절벽 구간 우측 아래 아래 아래 아래
                (3617, 920, 3950, 1200),  # 8. 절벽 구간 우측 아래 아래 아래 아래 옆
                (3383, 920, 3617, 1280),  # 9. 절벽 구간 우측 아래 아래 아래 아래 옆 옆
                (1046, 1700, 1620, 3050),  # 10. 절벽 구간 좌측 좌측
                (1277, 1530, 1330,1700 ),  # 절벽 구간 좌측 좌측 아래
                (1330, 1580, 1390, 1700),  # 절벽 구간 좌측 좌측 아래옆
                (1390, 1620, 1450, 1700),  # 절벽 구간 좌측 좌측 아래옆옆
                (0, 2400, 1046, 3050),  # 11. 절벽 구간 좌측 좌측 좌측
                (0, 2270, 610, 2400),  # 12. 절벽 구간 좌측 좌측 좌측 아래
                (0,2120, 660, 2270),  # 13. 절벽 구간 좌측 좌측 좌측 아래 아래
                (0, 1800, 930, 2120),  # 14. 절벽 구간 좌측 좌측 좌측 아래 아래 아래
                (1729, 1000, 1990, 1500),  # 15. 중앙 폭포
                (1502, 1250, 1729, 1550),  # 16. 중앙 폭포 왼쪽
                (1480, 1450, 1502, 1540),  # 17. 중앙 폭포 왼쪽 왼쪽
            ]

    def draw(self, cam_x, cam_y):
        screen_x = self.world_x - cam_x
        screen_y = self.world_y - cam_y
        self.image.draw(screen_x, screen_y)
        if self.map_number == 1:
            # 월드 좌표에서 카메라 좌표를 빼서 화면 좌표(Screen Coordinate)를 구함
            p_screen_x = self.portal_x - cam_x
            p_screen_y = self.portal_y - cam_y
            self.portal_image.draw(p_screen_x, p_screen_y)
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