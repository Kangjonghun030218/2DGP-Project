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

        self.skill_icon = resource_manager.get_image('boss_skill_icon')
        self.skill_effect = resource_manager.get_image('boss_skill_effect')

        self.max_hp = 2000
        self.current_hp = 2000

        self.timer = 0.0
        self.float_y = 0.0
        self.scale_factor = 1.0
        self.dir = -1

        self.speed = 100.0
        self.detect_range = 1200
        self.attack_range_limit = 400

        self.is_attacking = False
        self.attack_type = 'none'
        self.attack_timer = 0.0
        self.attack_cooldown = 2.0
        self.last_attack_time = 0.0
        self.arm_angle = 0.0

        self.rocket_start_pos = (0, 0)
        self.rocket_target_pos = (0, 0)
        self.rocket_current_pos = [0, 0]

        self.skill_max_cooldown = 10.0
        self.skill_current_cooldown = 10.0
        self.thunder_active = False
        self.thunder_timer = 0.0
        self.thunder_pos = (0, 0)
        self.thunder_hit = False

        self.w, self.h = 350, 450
        self.collision_box = (200, 300)

    def get_bb(self):
        return (self.x - self.collision_box[0] // 2, self.y - self.collision_box[1] // 2,
                self.x + self.collision_box[0] // 2, self.y + self.collision_box[1] // 2)

    def get_attack_bb(self):
        box_size = 150
        if self.attack_type == 'rocket':
            rx, ry = self.rocket_current_pos
            return (rx - box_size // 2, ry - box_size // 2,
                    rx + box_size // 2, ry + box_size // 2)
        else:
            arm_offset = 230 * self.dir
            return (
                self.x + arm_offset - 60, self.y - 75,
                self.x + arm_offset + 60, self.y + 75
            )

    def get_thunder_bb(self):
        if not self.thunder_active: return None

        tx, ty = self.thunder_pos
        half_size = 150
        return (tx - half_size, ty - half_size, tx + half_size, ty + half_size)

    def update(self, frame_time, game_map, player):
        self.timer += frame_time
        self.float_y = math.sin(self.timer * 3.0) * 20
        self.scale_factor = 1.0 + math.sin(self.timer * 5.0) * 0.02

        dist_x = player.world_x - self.x
        dist_y = player.world_y - self.y
        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

        if self.skill_current_cooldown > 0:
            self.skill_current_cooldown -= frame_time

        if self.skill_current_cooldown <= 0 and distance < self.detect_range:
            self.start_thunder_skill(player)

        if self.thunder_active:
            self.update_thunder(frame_time)

        if not self.is_attacking:
            if player.world_x > self.x:
                self.dir = 1
            else:
                self.dir = -1

            if self.attack_range_limit < distance < self.detect_range:
                move_x = (dist_x / distance) * self.speed * frame_time
                move_y = (dist_y / distance) * self.speed * frame_time
                self.x += move_x
                self.y += move_y

        if distance < self.attack_range_limit and not self.is_attacking:
            if self.timer - self.last_attack_time > self.attack_cooldown:
                if abs(dist_y) > abs(dist_x) * 0.8:
                    self.start_attack('rocket', player)
                else:
                    self.start_attack('smash', player)

        if self.is_attacking:
            self.attack_timer += frame_time
            if self.attack_type == 'smash':
                self.update_smash()
            elif self.attack_type == 'rocket':
                self.update_rocket()

    # [추가] 스킬 시작
    def start_thunder_skill(self, player):
        print("보스 스킬: 비격진천뢰 발동!")
        self.skill_current_cooldown = self.skill_max_cooldown
        self.thunder_active = True
        self.thunder_timer = 0.0
        self.thunder_hit = False
        self.thunder_pos = (player.world_x, player.world_y)

    def update_thunder(self, frame_time):
        self.thunder_timer += frame_time
        if self.thunder_timer >= 0.9:
            self.thunder_active = False

    def start_attack(self, attack_type, player=None):
        self.is_attacking = True
        self.attack_type = attack_type
        self.attack_timer = 0.0

        if attack_type == 'rocket' and player:
            self.rocket_start_pos = (self.x + (50 * self.dir), self.y + 50)
            self.rocket_target_pos = (player.world_x, player.world_y)
            self.rocket_current_pos = list(self.rocket_start_pos)

    def update_smash(self):
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
            self.finish_attack()

    def update_rocket(self):
        start_x, start_y = self.rocket_start_pos
        target_x, target_y = self.rocket_target_pos

        if self.attack_timer < 0.4:
            self.rocket_current_pos[0] = start_x + math.sin(self.timer * 50) * 5
            self.rocket_current_pos[1] = start_y + math.cos(self.timer * 50) * 5
        elif self.attack_timer < 0.7:
            t = (self.attack_timer - 0.4) / 0.3
            self.rocket_current_pos[0] = start_x + (target_x - start_x) * t
            self.rocket_current_pos[1] = start_y + (target_y - start_y) * t
        elif self.attack_timer < 1.5:
            t = (self.attack_timer - 0.7) / 0.8
            return_x = self.x + (50 * self.dir)
            return_y = self.y + 50
            self.rocket_current_pos[0] = target_x + (return_x - target_x) * t
            self.rocket_current_pos[1] = target_y + (return_y - target_y) * t
        else:
            self.finish_attack()

    def finish_attack(self):
        self.is_attacking = False
        self.attack_timer = 0.0
        self.arm_angle = 0.0
        self.last_attack_time = self.timer
        self.attack_type = 'none'

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp <= 0:
            self.x = -9999

    def draw(self, cam_x, cam_y):
        sx = self.x - cam_x
        sy = self.y - cam_y + self.float_y
        flip = 'h' if self.dir == 1 else ''
        if self.aura_image:
            self.aura_image.opacify(0.8)
            self.aura_image.clip_composite_draw(0, 0, self.aura_image.w, self.aura_image.h, self.timer * 2, '', sx, sy,
                                                self.aura_image.w * 1.5, self.aura_image.h * 1.5)

        if self.body_image:
            self.body_image.clip_composite_draw(0, 0, self.body_image.w, self.body_image.h, 0, flip, sx, sy,
                                                self.w * self.scale_factor, self.h * self.scale_factor)

        back_arm_img = self.arm_l_image
        front_arm_img = self.arm_r_image
        back_offset_x = -100 * self.dir
        if back_arm_img:
            back_arm_img.clip_composite_draw(0, 0, back_arm_img.w, back_arm_img.h, 0, flip, sx + back_offset_x, sy,
                                             back_arm_img.w * 1.4, back_arm_img.h * 1.4)

        if front_arm_img:
            if self.attack_type == 'rocket':
                rx = self.rocket_current_pos[0] - cam_x
                ry = self.rocket_current_pos[1] - cam_y
                dx = self.rocket_target_pos[0] - self.rocket_start_pos[0]
                dy = self.rocket_target_pos[1] - self.rocket_start_pos[1]
                rocket_angle = math.atan2(dy, dx) - (math.pi / 2)
                front_arm_img.clip_composite_draw(0, 0, front_arm_img.w, front_arm_img.h, rocket_angle, flip, rx, ry,
                                                  front_arm_img.w * 1.4, front_arm_img.h * 1.4)
            else:
                rad_angle = math.radians(self.arm_angle)
                rotation = -rad_angle if self.dir == 1 else rad_angle
                front_offset_x = 150 * self.dir
                front_arm_img.clip_composite_draw(0, 0, front_arm_img.w, front_arm_img.h, rotation, flip,
                                                  sx + front_offset_x, sy, front_arm_img.w * 1.4, front_arm_img.h * 1.4)

        if self.thunder_active and self.skill_effect:
            frame_index = int(self.thunder_timer * 10) % 9
            cols = 3
            col = frame_index % cols
            row = frame_index // cols

            sprite_w = self.skill_effect.w // 3
            sprite_h = self.skill_effect.h // 3

            tx = self.thunder_pos[0] - cam_x
            ty = self.thunder_pos[1] - cam_y

            self.skill_effect.clip_draw(
                col * sprite_w, row * sprite_h, sprite_w, sprite_h,
                tx, ty, 300, 300
            )

        if config.DEBUG_MODE_ON:
            draw_rectangle(*self.get_bb_screen(cam_x, cam_y))
            if self.is_attacking:
                hit = False
                if self.attack_type == 'smash' and 0.5 <= self.attack_timer <= 0.7: hit = True
                if self.attack_type == 'rocket' and 0.4 <= self.attack_timer <= 0.7: hit = True

                if hit:
                    l, b, r, t = self.get_attack_bb()
                    draw_rectangle(l - cam_x, b - cam_y, r - cam_x, t - cam_y)

            if self.thunder_active and (0.4 <= self.thunder_timer <= 0.6):
                tb = self.get_thunder_bb()
                if tb:
                    l, b, r, t = tb
                    draw_rectangle(l - cam_x, b - cam_y, r - cam_x, t - cam_y)
    def get_bb_screen(self, cam_x, cam_y):
        l, b, r, t = self.get_bb()
        return l - cam_x, b - cam_y, r - cam_x, t - cam_y