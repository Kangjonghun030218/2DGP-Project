from pico2d import *
import resource_manager
import config
import math
import server


class Boss:
    def __init__(self):
        self.x, self.y = 1200, 300
        self.body_image = resource_manager.get_image('boss_body')
        self.arm_l_image = resource_manager.get_image('boss_arm_l')
        self.arm_r_image = resource_manager.get_image('boss_arm_r')
        self.aura_image = None

        self.max_hp = 2000
        self.current_hp = 2000

        self.timer = 0.0
        self.float_y = 0.0
        self.scale_factor = 1.0
        self.dir = -1

        self.is_attacking = False
        self.attack_timer = 0.0
        self.arm_angle = 0.0
        self.attack_cooldown = 2.0
        self.last_attack_time = 0.0

        self.w, self.h = 350, 450
        self.collision_box = (200, 300)

    def get_bb(self):
        return (self.x - self.collision_box[0] // 2, self.y - self.collision_box[1] // 2,
                self.x + self.collision_box[0] // 2, self.y + self.collision_box[1] // 2)

    def get_attack_bb(self):
        arm_offset = 230 * self.dir
        box_size_x = 120
        box_size_y = 150

        return (
            self.x + arm_offset - box_size_x, self.y - box_size_y,
            self.x + arm_offset + box_size_x, self.y + box_size_y
        )

    def update(self, frame_time, game_map, player):
        self.timer += frame_time

        self.float_y = math.sin(self.timer * 3.0) * 20
        self.scale_factor = 1.0 + math.sin(self.timer * 5.0) * 0.02

        if not self.is_attacking:
            if player.world_x > self.x:
                self.dir = 1
            else:
                self.dir = -1
        dist_x = player.world_x - self.x
        dist_y = player.world_y - self.y
        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

        if distance < 400 and not self.is_attacking:
            if self.timer - self.last_attack_time > self.attack_cooldown:
                self.start_attack()
        if self.is_attacking:
            self.attack_timer += frame_time
            if self.attack_timer < 0.5:
                t = self.attack_timer / 0.5
                self.arm_angle = -60 * t
            elif self.attack_timer < 0.7:
                t = (self.attack_timer - 0.5) / 0.2
                self.arm_angle = -60 + (150 * t)
            elif self.attack_timer < 1.2:
                t = (self.attack_timer - 0.7) / 0.5
                self.arm_angle = 90 * (1.0 - t)

            else:
                self.is_attacking = False
                self.attack_timer = 0.0
                self.arm_angle = 0.0
                self.last_attack_time = self.timer

    def start_attack(self):
        self.is_attacking = True
        self.attack_timer = 0.0
        print("보스 파츠 공격 시작!")

    def take_damage(self, amount):
        self.current_hp -= amount
        print(f"보스 체력: {self.current_hp}")
        if self.current_hp <= 0:
            self.x = -9999

    def draw(self, cam_x, cam_y):
        sx = self.x - cam_x
        sy = self.y - cam_y + self.float_y
        flip = 'h' if self.dir == 1 else ''

        if self.aura_image:
            self.aura_image.opacify(0.8)
            self.aura_image.clip_composite_draw(
                0, 0, self.aura_image.w, self.aura_image.h,
                self.timer * 2, '', sx, sy,
                self.aura_image.w * 1.5, self.aura_image.h * 1.5
            )

        if self.body_image:
            self.body_image.clip_composite_draw(
                0, 0, self.body_image.w, self.body_image.h,
                0, flip, sx, sy,
                self.w * self.scale_factor, self.h * self.scale_factor
            )

        rad_angle = math.radians(self.arm_angle)
        rotation = -rad_angle if self.dir == 1 else rad_angle
        back_arm_img = self.arm_l_image
        front_arm_img = self.arm_r_image

        back_offset_x = -100 * self.dir
        back_offset_y = 0

        if back_arm_img:
            back_arm_img.clip_composite_draw(
                0, 0, back_arm_img.w, back_arm_img.h,
                rotation, flip,
                sx + back_offset_x, sy + back_offset_y,
                back_arm_img.w * 1.4, back_arm_img.h * 1.4
            )

        front_offset_x = 150 * self.dir
        front_offset_y = 0

        if front_arm_img:
            front_arm_img.clip_composite_draw(
                0, 0, front_arm_img.w, front_arm_img.h,
                rotation, flip,
                sx + front_offset_x, sy + front_offset_y,
                front_arm_img.w * 1.4, front_arm_img.h * 1.4
            )

        if config.DEBUG_MODE_ON:
            draw_rectangle(*self.get_bb_screen(cam_x, cam_y))
            if self.is_attacking and (0.5 <= self.attack_timer <= 0.7):
                l, b, r, t = self.get_attack_bb()
                draw_rectangle(l - cam_x, b - cam_y, r - cam_x, t - cam_y)

    def get_bb_screen(self, cam_x, cam_y):
        l, b, r, t = self.get_bb()
        return l - cam_x, b - cam_y, r - cam_x, t - cam_y