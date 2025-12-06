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

        self.skill_icon1 = resource_manager.get_image('boss_skill_icon')
        self.skill_effect1 = resource_manager.get_image('boss_skill_effect')

        self.skill_icon2 = resource_manager.get_image('boss_skill2_icon')
        self.skill_effect2 = resource_manager.get_image('boss_skill2_effect')

        self.charge_anim = resource_manager.get_image('boss_charge_anim')
        self.fire_anim = resource_manager.get_image('boss_fire_anim')

        self.max_hp = 30000
        self.current_hp = 30000
        self.speed = 100.0
        self.detect_range = 1200
        self.attack_range_limit = 400

        self.timer = 0.0
        self.float_y = 0.0
        self.scale_factor = 1.0
        self.dir = -1

        self.is_attacking = False
        self.attack_type = 'none'
        self.attack_timer = 0.0
        self.attack_cooldown = 2.0
        self.last_attack_time = 0.0
        self.arm_angle = 0.0

        self.rocket_start_pos = (0, 0)
        self.rocket_target_pos = (0, 0)
        self.rocket_current_pos = [0, 0]

        self.skill1_max_cd = 15.0
        self.skill1_cd = 15.0
        self.skill1_active = False
        self.skill1_timer = 0.0
        self.skill1_pos = (0, 0)
        self.skill1_hit = False

        self.skill2_max_cd = 10.0
        self.skill2_cd = 10.0
        self.skill2_active = False
        self.skill2_timer = 0.0
        self.skill2_pos = (0, 0)
        self.skill2_hit = False

        self.skill3_active = False
        self.skill3_state = 'none'
        self.skill3_timer = 0.0
        self.skill3_frame = 0
        self.skill3_cd = 0
        self.skill3_max_cd = 25.0

        self.w, self.h = 350, 450
        self.collision_box = (200, 300)

    def get_bb(self):
        return (self.x - self.collision_box[0] // 2, self.y - self.collision_box[1] // 2,
                self.x + self.collision_box[0] // 2, self.y + self.collision_box[1] // 2)

    def get_laser_bb(self):
        if self.skill3_state != 'firing': return None

        beam_len = 1000
        beam_h = 100
        if self.dir == 1:
            return (self.x + 100, self.y - beam_h // 2, self.x + 100 + beam_len, self.y + beam_h // 2)
        else:
            return (self.x - 100 - beam_len, self.y - beam_h // 2, self.x - 100, self.y + beam_h // 2)

    def start_skill3(self):
        print("보스 스킬3: 차징 시작!")
        self.skill3_active = True
        self.skill3_state = 'charging'
        self.skill3_timer = 0.0
        self.skill3_frame = 0
        self.skill3_cd = self.skill3_max_cd

    def get_attack_bb(self):
        box_size = 150
        if self.attack_type == 'rocket':
            rx, ry = self.rocket_current_pos
            return (rx - box_size // 2, ry - box_size // 2, rx + box_size // 2, ry + box_size // 2)
        else:
            # 스매시
            arm_offset = 230 * self.dir
            return (self.x + arm_offset - 60, self.y - 75,
                    self.x + arm_offset + 60, self.y + 75)

    def get_thunder_bb(self):
        if not self.skill1_active: return None
        tx, ty = self.skill1_pos
        half_size = 350
        return (tx - half_size, ty - half_size, tx + half_size, ty + half_size)

    def get_skill2_bb(self):
        if not self.skill2_active: return None
        tx, ty = self.skill2_pos
        half = 50
        return (tx - half, ty - half, tx + half, ty + half)

    def get_bb_screen(self, cam_x, cam_y):
        l, b, r, t = self.get_bb()
        return l - cam_x, b - cam_y, r - cam_x, t - cam_y

    def update(self, frame_time, game_map, player):
        self.timer += frame_time
        dist_x = player.world_x - self.x
        dist_y = player.world_y - self.y
        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

        if self.skill1_cd > 0: self.skill1_cd -= frame_time
        if self.skill2_cd > 0: self.skill2_cd -= frame_time
        if self.skill3_cd > 0: self.skill3_cd -= frame_time

        can_act = (not self.is_attacking and
                   not self.skill1_active and
                   not self.skill2_active and
                   not self.skill3_active)

        if can_act and distance < self.detect_range:
            if self.skill3_cd <= 0:
                self.start_skill3()
            elif self.skill1_cd <= 0:
                self.start_skill1()
            elif self.skill2_cd <= 0:
                self.start_skill2(player)

        bobbing_speed = 3.0

        if can_act:
            if player.world_x > self.x:
                self.dir = 1
            else:
                self.dir = -1

            if self.attack_range_limit < distance < self.detect_range:
                move_x = (dist_x / distance) * self.speed * frame_time
                move_y = (dist_y / distance) * self.speed * frame_time
                self.x += move_x
                self.y += move_y

                bobbing_speed = 8.0
        self.float_y = math.sin(self.timer * bobbing_speed) * 20
        self.scale_factor = 1.0 + math.sin(self.timer * 5.0) * 0.02

        if can_act and distance < self.attack_range_limit:
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

        if self.skill1_active:
            self.skill1_timer += frame_time
            if self.skill1_timer >= 0.9: self.skill1_active = False

        if self.skill2_active:
            self.skill2_timer += frame_time
            if self.skill2_timer >= 0.8: self.skill2_active = False

        if self.skill3_active:
            self.skill3_timer += frame_time

            if self.skill3_state == 'charging':
                charge_speed = 0.2
                self.skill3_frame = int(self.skill3_timer / charge_speed)

                if player.world_x > self.x:
                    self.dir = 1
                else:
                    self.dir = -1
                if self.skill3_frame >= 8:
                    print("차징 완료! 발사!")
                    self.skill3_state = 'firing'
                    self.skill3_timer = 0.0
                    self.skill3_frame = 0

            elif self.skill3_state == 'firing':
                fire_speed = 0.05
                self.skill3_frame = int(self.skill3_timer / fire_speed)
                if self.skill3_frame >= 36:
                    print("스킬3 종료")
                    self.skill3_active = False
                    self.skill3_state = 'none'

    def start_skill1(self):
        print("보스 스킬1: 비격진천뢰 (광역)")
        self.skill1_cd = self.skill1_max_cd
        self.skill1_active = True
        self.skill1_timer = 0.0
        self.skill1_hit = False
        self.skill1_pos = (self.x, self.y)

    def start_skill2(self, player):
        print("보스 스킬2: 암흑 발톱 (유도)")
        self.skill2_cd = self.skill2_max_cd
        self.skill2_active = True
        self.skill2_timer = 0.0
        self.skill2_hit = False
        self.skill2_pos = (player.world_x, player.world_y)

    def start_attack(self, type, player=None):
        self.is_attacking = True
        self.attack_type = type
        self.attack_timer = 0.0

        if type == 'rocket' and player:
            print("로켓 펀치!")
            self.rocket_start_pos = (self.x + (50 * self.dir), self.y + 50)
            self.rocket_target_pos = (player.world_x, player.world_y)
            self.rocket_current_pos = list(self.rocket_start_pos)
        else:
            print("스매시!")

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
        body_rotation = 0.0

        if self.aura_image:
            self.aura_image.opacify(0.8)
            self.aura_image.clip_composite_draw(0, 0, self.aura_image.w, self.aura_image.h,
                                                self.timer * 2, '', sx, sy,
                                                self.aura_image.w * 1.5, self.aura_image.h * 1.5)

        if self.body_image:
            self.body_image.clip_composite_draw(0, 0, self.body_image.w, self.body_image.h,
                                                body_rotation, flip, sx, sy,
                                                self.w * self.scale_factor, self.h * self.scale_factor)

        back_arm_img = self.arm_l_image
        front_arm_img = self.arm_r_image

        if back_arm_img:
            back_arm_img.clip_composite_draw(0, 0, back_arm_img.w, back_arm_img.h,
                                             body_rotation, flip, sx - (100 * self.dir), sy,
                                             back_arm_img.w * 1.4, back_arm_img.h * 1.4)

        if front_arm_img:
            if self.attack_type == 'rocket':
                rx = self.rocket_current_pos[0] - cam_x
                ry = self.rocket_current_pos[1] - cam_y
                dx = self.rocket_target_pos[0] - self.rocket_start_pos[0]
                dy = self.rocket_target_pos[1] - self.rocket_start_pos[1]
                rocket_angle = math.atan2(dy, dx) - (math.pi / 2)

                front_arm_img.clip_composite_draw(0, 0, front_arm_img.w, front_arm_img.h,
                                                  rocket_angle, flip, rx, ry,
                                                  front_arm_img.w * 1.4, front_arm_img.h * 1.4)
            else:
                rad_angle = math.radians(self.arm_angle)
                total_rot = (-rad_angle if self.dir == 1 else rad_angle)

                front_arm_img.clip_composite_draw(0, 0, front_arm_img.w, front_arm_img.h,
                                                  total_rot, flip, sx + (150 * self.dir), sy,
                                                  front_arm_img.w * 1.4, front_arm_img.h * 1.4)

        if self.skill1_active and self.skill_effect1:
            frame_index = int(self.skill1_timer * 10) % 9
            cols = 3
            col = frame_index % cols
            row = frame_index // cols
            sw, sh = self.skill_effect1.w // 3, self.skill_effect1.h // 3
            tx = self.skill1_pos[0] - cam_x
            ty = self.skill1_pos[1] - cam_y
            self.skill_effect1.clip_draw(col * sw, row * sh, sw, sh, tx, ty, 800, 800)

        if self.skill2_active and self.skill_effect2:
            frame_index = int(self.skill2_timer * 10) % 8
            cols = 4
            col = frame_index % cols
            row = frame_index // cols
            sw, sh = self.skill_effect2.w // 4, self.skill_effect2.h // 2
            tx = self.skill2_pos[0] - cam_x
            ty = self.skill2_pos[1] - cam_y
            self.skill_effect2.clip_draw(col * sw, row * sh, sw, sh, tx, ty + 50, 200, 200)

        if self.skill3_active:
            if self.skill3_state == 'charging':
                if self.charge_anim:
                    idx = min(self.skill3_frame, 7)
                    img = self.charge_anim[idx]
                    img.clip_composite_draw(0, 0, img.w, img.h, 0, flip, sx, sy, 400, 400)

            elif self.skill3_state == 'firing':
                if self.fire_anim:
                    idx = min(self.skill3_frame, 35)
                    img = self.fire_anim[idx]
                    offset_x = 600 * self.dir
                    img.clip_composite_draw(0, 0, img.w, img.h,
                                            0, flip, sx + offset_x, sy, 1000, 400)

        else:
            if self.body_image:
                self.body_image.clip_composite_draw(0, 0, self.body_image.w, self.body_image.h,
                                                    0, flip, sx, sy, self.w * self.scale_factor,
                                                    self.h * self.scale_factor)

        if config.DEBUG_MODE_ON:
            draw_rectangle(*self.get_bb_screen(cam_x, cam_y))

            if self.is_attacking:
                hit = False
                if self.attack_type == 'smash' and 0.5 <= self.attack_timer <= 0.7: hit = True
                if self.attack_type == 'rocket' and 0.4 <= self.attack_timer <= 0.7: hit = True
                if hit:
                    l, b, r, t = self.get_attack_bb()
                    draw_rectangle(l - cam_x, b - cam_y, r - cam_x, t - cam_y)

            if self.skill1_active and (0.4 <= self.skill1_timer <= 0.6):
                tb = self.get_thunder_bb()
                if tb: draw_rectangle(tb[0] - cam_x, tb[1] - cam_y, tb[2] - cam_x, tb[3] - cam_y)

            if self.skill2_active and (0.3 <= self.skill2_timer <= 0.6):
                sb = self.get_skill2_bb()
                if sb: draw_rectangle(sb[0] - cam_x, sb[1] - cam_y, sb[2] - cam_x, sb[3] - cam_y)
            if self.skill3_state == 'firing':
                lb = self.get_laser_bb()
                if lb: draw_rectangle(lb[0] - cam_x, lb[1] - cam_y, lb[2] - cam_x, lb[3] - cam_y)