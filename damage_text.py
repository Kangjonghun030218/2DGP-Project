from pico2d import *
import resource_manager


class DamageText:
    def __init__(self, x, y, damage, color=(255, 0, 0)):
        self.x, self.y = x, y
        self.damage = damage

        self.timer = 0.0
        self.life_time = 0.8
        self.float_speed = 100.0

        self.font = load_font('resource/malgunbd.ttf', 30)


        self.is_finished = False
        self.color = color

    def update(self, frame_time):
        self.timer += frame_time

        self.y += self.float_speed * frame_time

        if self.timer >= self.life_time:
            self.is_finished = True

    def draw(self, cam_x, cam_y):
        if self.is_finished: return

        sx = self.x - cam_x
        sy = self.y - cam_y
        if self.font:
            self.font.draw(sx, sy, f"{int(self.damage)}", self.color)