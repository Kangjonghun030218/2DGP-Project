from pico2d import *
import resource_manager
import server
import config


class Princess:
    def __init__(self):
        self.x, self.y = 1600, 300

        self.image = resource_manager.get_image('princess_sheet')
        self.cage_image = resource_manager.get_image('cage')

        self.frame = 0.0
        self.is_freed = False

        self.speed = 8.0

        if self.image:
            self.frame_width = self.image.w // 5
            self.frame_height = self.image.h // 2
        else:
            self.frame_width = 100
            self.frame_height = 100

    def update(self, frame_time):
        boss = None
        for obj in server.world:
            if hasattr(obj, 'max_hp') and hasattr(obj, 'rocket_start_pos'):
                boss = obj
                break

        if boss is None or boss.current_hp <= 0:
            if not self.is_freed:
                self.is_freed = True
                self.frame = 0.0

        if self.is_freed:
            self.frame += self.speed * frame_time
            if self.frame >= 4.0:
                self.frame = 4.0
        else:
            self.frame = 0

    def draw(self, cam_x, cam_y):
        if not self.image: return
        sx = self.x - cam_x
        sy = self.y - cam_y
        int_frame = int(self.frame)
        princess_y_offset = -20
        cage_y_offset = 30


        if not self.is_freed:
            self.image.clip_draw(
                int_frame * self.frame_width, self.frame_height,
                self.frame_width, self.frame_height,
                sx, sy + princess_y_offset,
                150, 150
            )

            if self.cage_image:
                self.cage_image.draw(sx, sy + cage_y_offset, 800, 400)

        else:
            self.image.clip_draw(
                int_frame * self.frame_width, 0,
                self.frame_width, self.frame_height,
                sx, sy + princess_y_offset,
                150, 150
            )

    def get_bb(self):
        return 0, 0, 0, 0