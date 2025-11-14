from pico2d import *
import game_globals as g

class Projectile:
    def __init__(self, start_x, start_y, direction, speed=10):
        self.world_x = start_x
        self.world_y = start_y
        self.direction = direction
        self.speed = speed
        self.image_to_draw = None
        self.debug_mode = g.DEBUG_MODE_ON

        if self.direction == 'left' or self.direction == 'right':
            self.image_to_draw = g.projectile_image_LR
        elif self.direction == 'up' or self.direction == 'down':
            self.image_to_draw = g.projectile_image_UD

        self.life_time = 2.0
        self.start_time = get_time()

        self.vel_x, self.vel_y = 0, 0
        if self.direction == 'left':
            self.vel_x = -self.speed
        elif self.direction == 'right':
            self.vel_x = self.speed
        elif self.direction == 'up':
            self.vel_y = self.speed
        elif self.direction == 'down':
            self.vel_y = -self.speed

    def draw(self, cam_x, cam_y):
        screen_x = self.world_x - cam_x
        screen_y = self.world_y - cam_y

        flip = ''
        if self.direction == 'left':
            flip = 'h'
        elif self.direction == 'down':
            flip = 'v'

        if self.image_to_draw:
            self.image_to_draw.clip_composite_draw(
                0, 0, self.image_to_draw.w, self.image_to_draw.h,
                0, flip,
                screen_x, screen_y,
                self.image_to_draw.w, self.image_to_draw.h
            )
        if self.debug_mode:
            l, b, r, t = self.get_bb()
            screen_l, screen_b = l - cam_x, b - cam_y
            screen_r, screen_t = r - cam_x, t - cam_y
            draw_rectangle(screen_l, screen_b, screen_r, screen_t)

    def get_bb(self):
        half_width = self.image_to_draw.w / 2
        half_height = self.image_to_draw.h / 2
        return (self.world_x - half_width, self.world_y - half_height,
                self.world_x + half_width, self.world_y + half_height)

    def update(self):
        self.world_x += self.vel_x
        self.world_y += self.vel_y

        if get_time() - self.start_time > self.life_time:
            return True
        return False