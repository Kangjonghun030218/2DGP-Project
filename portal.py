from pico2d import *
import resource_manager
import config


class Portal:

    def __init__(self, x, y, portal_type='normal'):
        self.x, self.y = x, y
        self.portal_type = portal_type

        if self.portal_type == 'normal':
            self.image = resource_manager.get_image('portal')
            self.w, self.h = 100, 100
        elif self.portal_type == 'boss':
            self.image = resource_manager.get_image('boss_portal')
            self.w, self.h = 150, 150
        elif self.portal_type == 'map3':
            self.image = resource_manager.get_image('portal')
            self.w, self.h = 100, 100
        elif self.portal_type == 'boss_clear':
            self.image = resource_manager.get_image('boss_clear_portal')
            self.w, self.h = 200, 200
        else:
            self.image = resource_manager.get_image('portal')
            self.w, self.h = 100, 100

    def update(self, frame_time):
        pass

    def draw(self, cam_x, cam_y):
        if self.image:
            sx = self.x - cam_x
            sy = self.y - cam_y
            self.image.draw(sx, sy, self.w, self.h)

            if config.DEBUG_MODE_ON:
                draw_rectangle(*self.get_bb_screen(cam_x, cam_y))

    def get_bb(self):
        return (self.x - self.w // 2, self.y - self.h // 2,
                self.x + self.w // 2, self.y + self.h // 2)

    def get_bb_screen(self, cam_x, cam_y):
        l, b, r, t = self.get_bb()
        return l - cam_x, b - cam_y, r - cam_x, t - cam_y