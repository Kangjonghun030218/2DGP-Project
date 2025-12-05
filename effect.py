from pico2d import *
import resource_manager
import config


class LevelUpEffect:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.images = resource_manager.get_image('level_up_effect')
        self.font = resource_manager.get_font()

        self.frame_index = 0
        self.timer = 0.0
        self.frame_duration = 0.15
        self.total_duration = self.frame_duration * len(self.images)
        self.is_finished = False
        self.scale = 2.5

    def update(self, frame_time):
        self.timer += frame_time
        if self.timer >= self.total_duration:
            self.is_finished = True
        else:
            self.frame_index = int(self.timer / self.frame_duration)

    def draw(self, cam_x, cam_y):
        if self.is_finished: return

        sx = self.x - cam_x
        sy = self.y - cam_y
        img = self.images[self.frame_index]
        img.draw(sx, sy, img.w * self.scale, img.h * self.scale)

        if self.font:
            text = "Level Up!"
            text_y = sy + 60
            self.font.draw(sx - 40, text_y, text, (255, 255, 0))