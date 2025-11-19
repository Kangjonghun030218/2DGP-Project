from pico2d import *
import server
import resource_manager
import config
import math
from projectile import Projectile


PIXEL_PER_METER = (10.0 / 0.3)

WALK_SPEED_KMPH = 30.0
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)


RUN_SPEED_KMPH = 60.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


#넉백 속도
KNOCKBACK_SPEED_PPS = (WALK_SPEED_PPS * 2)


# 각 동작이 1사이클 도는 데 걸리는 시간 !
TIME_PER_ACTION_IDLE = 2.4
TIME_PER_ACTION_WALK = 0.6
TIME_PER_ACTION_RUN = 0.8
TIME_PER_ACTION_ATTACK = 0.4
TIME_PER_ACTION_HIT = 0.3
TIME_PER_ACTION_DEAD = 0.7

#시트 수
FRAMES_PER_ACTION_IDLE = 12
FRAMES_PER_ACTION_WALK = 6
FRAMES_PER_ACTION_RUN = 8
FRAMES_PER_ACTION_ATTACK = 8
FRAMES_PER_ACTION_HIT = 5
FRAMES_PER_ACTION_DEAD = 7


TIME_PER_FRAME_IDLE = TIME_PER_ACTION_IDLE / FRAMES_PER_ACTION_IDLE
TIME_PER_FRAME_WALK = TIME_PER_ACTION_WALK / FRAMES_PER_ACTION_WALK
TIME_PER_FRAME_RUN = TIME_PER_ACTION_RUN / FRAMES_PER_ACTION_RUN
TIME_PER_FRAME_ATTACK = TIME_PER_ACTION_ATTACK / FRAMES_PER_ACTION_ATTACK
TIME_PER_FRAME_HIT = TIME_PER_ACTION_HIT / FRAMES_PER_ACTION_HIT
TIME_PER_FRAME_DEAD = TIME_PER_ACTION_DEAD / FRAMES_PER_ACTION_DEAD

####-----------여기서 부터는 스킬 관련 시간 조정할거임-----------####
# Skill 1 (Lvl 1)
TIME_PER_ACTION_SKILL1_LVL1 = 0.5
FRAMES_PER_ACTION_SKILL1_LVL1 = 2
TIME_PER_FRAME_SKILL1_LVL1 = TIME_PER_ACTION_SKILL1_LVL1 / FRAMES_PER_ACTION_SKILL1_LVL1

# Skill 1 (Lvl 2)
TIME_PER_ACTION_SKILL1_LVL2 = 0.4
FRAMES_PER_ACTION_SKILL1_LVL2 = 4
TIME_PER_FRAME_SKILL1_LVL2 = TIME_PER_ACTION_SKILL1_LVL2 / FRAMES_PER_ACTION_SKILL1_LVL2

# Skill 1 (Lvl 3)
TIME_PER_ACTION_SKILL1_LVL3 = 0.4
FRAMES_PER_ACTION_SKILL1_LVL3 = 12
TIME_PER_FRAME_SKILL1_LVL3 = TIME_PER_ACTION_SKILL1_LVL3 / FRAMES_PER_ACTION_SKILL1_LVL3

# Skill 2 (Lvl 1)
TIME_PER_ACTION_SKILL2_LVL1 = 0.5
FRAMES_PER_ACTION_SKILL2_LVL1 = 2
TIME_PER_FRAME_SKILL2_LVL1 = TIME_PER_ACTION_SKILL2_LVL1 / FRAMES_PER_ACTION_SKILL2_LVL1

# Skill 2 (Lvl 2)
TIME_PER_ACTION_SKILL2_LVL2 = 0.6
FRAMES_PER_ACTION_SKILL2_LVL2 = 12
TIME_PER_FRAME_SKILL2_LVL2 = TIME_PER_ACTION_SKILL2_LVL2 / FRAMES_PER_ACTION_SKILL2_LVL2

# Skill 2 (Lvl 3)
TIME_PER_ACTION_SKILL2_LVL3 = 0.6
FRAMES_PER_ACTION_SKILL2_LVL3 = 12
TIME_PER_FRAME_SKILL2_LVL3 = TIME_PER_ACTION_SKILL2_LVL3 / FRAMES_PER_ACTION_SKILL2_LVL3

def check_collision(a, b):
    left_a, bottom_a, right_a, top_a = a
    left_b, bottom_b, right_b, top_b = b

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


class Knight:
    def __init__(self):
        self.world_x = 1250
        self.world_y = 350

        self.images_lvl1 = {
            'idle': resource_manager.get_image('knight_lvl1_idle'),
            'walk': resource_manager.get_image('knight_lvl1_walk'),
            'run': resource_manager.get_image('knight_lvl1_run'),
            'attack': resource_manager.get_image('knight_lvl1_attack'),
            'hit': resource_manager.get_image('knight_lvl1_hit'),
            'dead': resource_manager.get_image('knight_lvl1_dead')
        }
        self.images_lvl2 = {
            'idle': resource_manager.get_image('knight_lvl2_idle'),
            'walk': resource_manager.get_image('knight_lvl2_walk'),
            'run': resource_manager.get_image('knight_lvl2_run'),
            'attack': resource_manager.get_image('knight_lvl2_attack'),
            'hit': resource_manager.get_image('knight_lvl2_hit'),
            'dead': resource_manager.get_image('knight_lvl2_dead')
        }
        self.images_lvl3 = {
            'idle': resource_manager.get_image('knight_lvl3_idle'),
            'walk': resource_manager.get_image('knight_lvl3_walk'),
            'run': resource_manager.get_image('knight_lvl3_run'),
            'attack': resource_manager.get_image('knight_lvl3_attack'),
            'hit': resource_manager.get_image('knight_lvl3_hit'),
            'dead': resource_manager.get_image('knight_lvl3_dead')
        }

        self.level =3
        self.quests_completed = 0
        self.current_images = self.images_lvl3

        self.frame = 0
        self.frame_timer = 0.0

        self.state = "idle"
        self.direct = "down"
        self.r_key_pressed = False
        self.a_key_pressed = False
        self.dir_x = 0
        self.dir_y = 0

        self.max_hp = 100
        self.current_hp = 100
        self.max_mp = 50
        self.current_mp = 50

        self.skill_name = ''
        self.is_effect_active = False
        self.effect_start_time = 0.0
        self.effect_total_duration = 0.5
        self.effect_frame = 0
        self.effect_flip_direction = 'right'

        self.walk_speed = WALK_SPEED_PPS
        self.run_speed = RUN_SPEED_PPS
        self.knockback_speed = KNOCKBACK_SPEED_PPS

        self.is_hit = False
        self.hit_start_time = 0.0
        self.hit_duration = 0.3
        self.knockback_dir_x = 0
        self.knockback_dir_y = 0

        self.i=0
        self.hp_potions = 0
        self.mp_potions = 0

        self.effect_anim_frame = 0
        self.effect_anim_timer = 0.0


        self.death_max_frame = 7
        self.is_dead_and_animation_finished = False

        self.clip_y_table = {
            'down': 192,
            'left': 128,
            'right': 64,
            'up': 0
        }

        self.skill_cooldowns = {
            'skill1': 5.0,
            'skill2': 8.0,
            'skill3': 10.0
        }
        self.skill_last_used = {
            'skill1': 0.0,
            'skill2': 0.0,
            'skill3': 0.0
        }

        self.debug_mode = config.DEBUG_MODE_ON

        self.skill1_lvl2_effect_anim = resource_manager.get_image('skill_lvl2_anim')
        self.skill1_lvl3_effect_anim = resource_manager.get_image('skill_lvl3_anim')
        self.skill1_lvl2_1_effect_anim = resource_manager.get_image('skill_lvl2_R_anim')
        self.skill1_lvl2_1_U_effect_anim = resource_manager.get_image('skill_lvl2_U_anim')
        self.skill1_lvl3_1_effect_anim = resource_manager.get_image('skill_lvl3_R_anim')
        self.skill1_lvl3_1_U_effect_anim = resource_manager.get_image('skill_lvl3_U_anim')


        self.skill1_new_sheet = resource_manager.get_image('skill1_new_sheet')
        self.skill2_new_sheet = resource_manager.get_image('skill2_new_sheet')
        self.skill3_new_sheet = resource_manager.get_image('skill3_new_sheet')

    def draw(self, cam_x, cam_y):
        screen_x = self.world_x - cam_x
        screen_y = self.world_y - cam_y
        if self.debug_mode:
            l, b, r, t = self.get_bb()

            screen_l, screen_b = l - cam_x, b - cam_y
            screen_r, screen_t = r - cam_x, t - cam_y

            draw_rectangle(screen_l, screen_b, screen_r, screen_t)
            is_attack_frame = (self.state == 'attack')
            if is_attack_frame:
                al, ab, ar, at = self.get_attack_bb()

                screen_al, screen_ab = al - cam_x, ab - cam_y
                screen_ar, screen_at = ar - cam_x, at - cam_y

                draw_rectangle(screen_al, screen_ab, screen_ar, screen_at)

        clip_y = self.clip_y_table[self.direct]
        if self.state == 'idle':
            self.current_images['idle'].clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)
        elif self.state == 'move':
            self.current_images['walk'].clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)
        elif self.state == 'run':
            self.current_images['run'].clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)
        elif self.state == 'attack':
            self.current_images['attack'].clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)
        elif self.state == 'hit':
            self.current_images['hit'].clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)
        elif self.state == 'dead':
            self.current_images['dead'].clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)

        if self.skill_name == 'skill1':
            if self.is_effect_active:
                if self.level == 2:
                    if self.effect_anim_frame < 4:
                        image_to_draw = None
                        flip = ''
                        offset_x = 0

                        if self.effect_flip_direction == 'left':
                            flip = 'h'
                            image_to_draw = self.skill1_lvl2_1_effect_anim[self.effect_anim_frame]

                        elif self.effect_flip_direction == 'right':
                            flip = ''
                            image_to_draw = self.skill1_lvl2_1_effect_anim[self.effect_anim_frame]
                        elif self.effect_flip_direction == 'up':
                            flip = ''
                            image_to_draw = self.skill1_lvl2_1_U_effect_anim[self.effect_anim_frame]

                        elif self.effect_flip_direction == 'down':
                            flip = 'v'
                            image_to_draw = self.skill1_lvl2_1_U_effect_anim[self.effect_anim_frame]

                        effect_img_to_draw = image_to_draw
                        if effect_img_to_draw:
                            effect_offset_x = 0
                            effect_offset_y = 0

                            if self.effect_flip_direction == 'left':
                                effect_offset_x = -30
                            elif self.effect_flip_direction == 'right':
                                effect_offset_x = 30
                            elif self.effect_flip_direction == 'down':
                                effect_offset_y = -30
                            elif self.effect_flip_direction == 'up':
                                effect_offset_y = 30

                            effect_img_to_draw.clip_composite_draw(
                                0, 0, effect_img_to_draw.w, effect_img_to_draw.h,
                                0, flip,
                                screen_x + effect_offset_x, screen_y + effect_offset_y,
                                effect_img_to_draw.w, effect_img_to_draw.h)
                elif self.level == 3:
                    if self.effect_anim_frame < 12:
                        sheet = self.skill1_new_sheet
                        fw = sheet.w // 3
                        fh = sheet.h // 4
                        idx = int(self.effect_anim_frame)

                        col = idx % 3
                        row_from_top = idx // 3

                        rect_x = col * fw
                        rect_y = sheet.h - (row_from_top + 1) * fh

                        flip = ''
                        rotation = 0

                        offset_x = 0
                        offset_y = 0
                        if self.effect_flip_direction == 'left':
                            flip = ''
                            offset_x = -60
                        elif self.effect_flip_direction == 'right':
                            flip = 'h'
                            offset_x = 60
                        elif self.effect_flip_direction == 'down':
                            flip = ''
                            rotation = math.radians(90)
                            offset_y = -60
                        elif self.effect_flip_direction == 'up':
                            flip = ''
                            rotation = math.radians(-90)
                            offset_y = +60
                        sheet.clip_composite_draw(
                            rect_x, rect_y, fw, fh,
                            rotation, flip,
                            screen_x + offset_x, screen_y + offset_y,
                            fw*2 , fh*2,
                        )
                else:
                    base_img1 = None
                    flip = ''
                    if self.effect_flip_direction == 'left':
                        base_img1 = resource_manager.get_image('effect_skill1_R1')
                        flip = 'h'
                    elif self.effect_flip_direction == 'right':
                        base_img1 = resource_manager.get_image('effect_skill1_R1')
                        flip = ''
                    elif self.effect_flip_direction == 'down':
                        base_img1 = resource_manager.get_image('effect_skill1_U1')
                        flip = 'v'
                    elif self.effect_flip_direction == 'up':
                        base_img1 = resource_manager.get_image('effect_skill1_U1')
                        flip = ''

                    effect_img_to_draw = base_img1
                    if effect_img_to_draw:
                        effect_offset_x = 0
                        effect_offset_y = 0

                        if self.effect_flip_direction == 'left':
                            effect_offset_x = -30
                        elif self.effect_flip_direction == 'right':
                            effect_offset_x = 30
                        elif self.effect_flip_direction == 'down':
                            effect_offset_y = -30
                        elif self.effect_flip_direction == 'up':
                            effect_offset_y = 30

                        effect_img_to_draw.clip_composite_draw(
                            0, 0, effect_img_to_draw.w, effect_img_to_draw.h,
                            0, flip,
                            screen_x + effect_offset_x, screen_y + effect_offset_y,
                            effect_img_to_draw.w, effect_img_to_draw.h)



        elif self.skill_name == 'skill2':
            if self.is_effect_active:
                if self.level == 2:
                    if self.effect_anim_frame < 12:
                        image_to_draw = self.skill1_lvl2_effect_anim[self.effect_anim_frame]

                        flip = ''
                        offset_x = 0

                        if self.effect_flip_direction == 'left':
                            flip = 'h'

                        elif self.effect_flip_direction == 'right':
                            flip = ''
                        image_to_draw.clip_composite_draw(
                            0, 0, image_to_draw.w, image_to_draw.h,
                            0, flip,
                            screen_x + offset_x, screen_y, 100, 100)




                elif self.level == 3:
                    if self.effect_anim_frame < 12:
                        sheet = self.skill3_new_sheet
                        fw = sheet.w // 4
                        fh = sheet.h // 3

                        idx = self.effect_anim_frame
                        col = idx % 4
                        row = idx // 4

                        rect_x = col * fw
                        rect_y = (2 - row) * fh

                        rotation = 0
                        flip = ''
                        offset_x = 0
                        offset_y = 0

                        if self.effect_flip_direction == 'left':
                            flip = ''
                            offset_x = -60
                        elif self.effect_flip_direction == 'right':
                            flip = 'h'
                            offset_x = 60
                        elif self.effect_flip_direction == 'up':
                            flip = ''
                            rotation = math.radians(-90)
                            offset_y = 60
                        elif self.effect_flip_direction == 'down':
                            flip = ''
                            rotation = math.radians(90)
                            offset_y = -60

                        sheet.clip_composite_draw(
                            rect_x, rect_y, fw, fh,
                            rotation, flip,
                            screen_x + offset_x, screen_y + offset_y,
                            125, 125
                        )

                elif self.level == 1:
                    base_img1 = None
                    base_img2 = None
                    flip = ''
                    if self.effect_flip_direction == 'left':
                        base_img1 = resource_manager.get_image('effect_skill2_R1')
                        base_img2 = resource_manager.get_image('effect_skill2_R2')
                        flip = 'h'
                    elif self.effect_flip_direction == 'right':
                        base_img1 = resource_manager.get_image('effect_skill2_R1')
                        base_img2 = resource_manager.get_image('effect_skill2_R2')
                        flip = ''
                    elif self.effect_flip_direction == 'down':
                        base_img1 = resource_manager.get_image('effect_skill2_U1')
                        base_img2 = resource_manager.get_image('effect_skill2_U2')
                        flip = 'v'
                    elif self.effect_flip_direction == 'up':
                        base_img1 = resource_manager.get_image('effect_skill2_U1')
                        base_img2 = resource_manager.get_image('effect_skill2_U2')
                        flip = ''

                    effect_img_to_draw = None
                    if self.effect_frame == 0:
                        effect_img_to_draw = base_img1
                    else:
                        effect_img_to_draw = base_img2

                    if effect_img_to_draw:
                        effect_offset_x = 0
                        effect_offset_y = 0

                        if self.effect_flip_direction == 'left':
                            effect_offset_x = -30
                        elif self.effect_flip_direction == 'right':
                            effect_offset_x = 30
                        elif self.effect_flip_direction == 'down':
                            effect_offset_y = -30
                        elif self.effect_flip_direction == 'up':
                            effect_offset_y = 30

                        effect_img_to_draw.clip_composite_draw(
                            0, 0, effect_img_to_draw.w, effect_img_to_draw.h,
                            0, flip,
                            screen_x + effect_offset_x, screen_y + effect_offset_y,
                            effect_img_to_draw.w, effect_img_to_draw.h)

    def update(self, game_map,frame_time):
        self.frame_timer += frame_time

        current_animation_speed = 0.1
        if self.state == 'idle':
            current_animation_speed = TIME_PER_FRAME_IDLE
        elif self.state == 'move':
            current_animation_speed = TIME_PER_FRAME_WALK
        elif self.state == 'run':
            current_animation_speed = TIME_PER_FRAME_RUN
        elif self.state == 'attack':
            current_animation_speed = TIME_PER_FRAME_ATTACK
        elif self.state == 'hit':
            current_animation_speed = TIME_PER_FRAME_HIT

        if self.state == 'dead':
            if self.frame < FRAMES_PER_ACTION_DEAD - 1:
                if self.frame_timer >= TIME_PER_FRAME_DEAD:
                    self.frame_timer -= TIME_PER_FRAME_DEAD
                    self.frame = (self.frame + 1)
            else:
                self.frame = self.death_max_frame - 1
                self.is_dead_and_animation_finished = True
            return

        if self.is_hit:
            current_time = get_time()
            if current_time - self.hit_start_time < self.hit_duration:
                dx = self.knockback_dir_x * self.knockback_speed * frame_time
                dy = self.knockback_dir_y * self.knockback_speed * frame_time

                l, b, r, t = self.get_bb()
                next_bb_x = (l + dx, b, r + dx, t)
                if not any(check_collision(next_bb_x, box) for box in game_map.get_collision_boxes()):
                    self.world_x += dx

                l, b, r, t = self.get_bb()
                next_bb_y = (l, b + dy, r, t + dy)
                if not any(check_collision(next_bb_y, box) for box in game_map.get_collision_boxes()):
                    self.world_y += dy

                map_width = game_map.width
                map_height = game_map.height
                l, b, r, t = self.get_bb()
                half_width = (r - l) / 2
                half_height = (t - b) / 2
                self.world_x = max(half_width, min(self.world_x, map_width - half_width))
                self.world_y = max(half_height, min(self.world_y, map_height - half_height))

                if self.frame_timer >= current_animation_speed:
                    self.frame_timer -= current_animation_speed
                    self.frame = (self.frame + 1) % FRAMES_PER_ACTION_HIT

                return
            else:
                self.is_hit = False
                self.state = 'idle'

        time_since_start = get_time() - self.effect_start_time

        if self.is_effect_active:
            if self.skill_name == 'skill2':
                if self.level == 2:
                    self.effect_anim_timer += frame_time
                    if self.effect_anim_timer >= TIME_PER_FRAME_SKILL2_LVL2:
                        self.effect_anim_timer -= TIME_PER_FRAME_SKILL2_LVL2
                        self.effect_anim_frame = (self.effect_anim_frame + 1)

                elif self.level == 3:
                    self.effect_anim_timer += frame_time
                    if self.effect_anim_timer >= TIME_PER_FRAME_SKILL2_LVL3:
                        self.effect_anim_timer -= TIME_PER_FRAME_SKILL2_LVL3
                        self.effect_anim_frame = (self.effect_anim_frame + 1)

                elif self.level == 1:
                    half_duration = self.effect_total_duration / 2
                    if time_since_start < half_duration:
                        self.effect_frame = 0
                    elif time_since_start < self.effect_total_duration:
                        self.effect_frame = 1

            elif self.skill_name == 'skill1':
                if self.level == 2:
                    self.effect_anim_timer += frame_time
                    if self.effect_anim_timer >= TIME_PER_FRAME_SKILL1_LVL2:
                        self.effect_anim_timer -= TIME_PER_FRAME_SKILL1_LVL2
                        self.effect_anim_frame = (self.effect_anim_frame + 1) % FRAMES_PER_ACTION_SKILL1_LVL2

                elif self.level == 3:
                    self.effect_anim_timer += frame_time
                    if self.effect_anim_timer >= TIME_PER_FRAME_SKILL1_LVL3:
                        self.effect_anim_timer -= TIME_PER_FRAME_SKILL1_LVL3
                        self.effect_anim_frame = (self.effect_anim_frame + 1)

                elif self.level == 1:
                    half_duration = self.effect_total_duration / 2
                    if time_since_start < half_duration:
                        self.effect_frame = 0
                    elif time_since_start < self.effect_total_duration:
                        self.effect_frame = 1

        if time_since_start > self.effect_total_duration:
            self.is_effect_active = False
            self.effect_anim_frame = 0
            self.effect_frame = 0

        if self.state == 'attack':
            if self.frame_timer >= current_animation_speed:
                self.frame_timer -= current_animation_speed
                self.frame = (self.frame + 1)

            if self.frame >= FRAMES_PER_ACTION_ATTACK:
                self.state = 'idle'
                self.frame = 0
            return

        if self.dir_x == 0 and self.dir_y == 0:
            if self.state != 'idle':
                self.frame = 0
            self.state = 'idle'
        else:
            if self.r_key_pressed:
                if self.state != 'run':
                    self.frame = 0
                self.state = 'run'
            else:
                if self.state != 'move':
                    self.frame = 0
                self.state = 'move'

        if self.dir_x > 0:
            self.direct = 'right'
        elif self.dir_x < 0:
            self.direct = 'left'
        elif self.dir_y > 0:
            self.direct = 'up'
        elif self.dir_y < 0:
            self.direct = 'down'

        if self.frame_timer >= current_animation_speed:
            self.frame_timer -= current_animation_speed
            if self.direct == 'up' and self.state == 'idle':
                self.frame = (self.frame + 1) % 4
            elif self.state == 'move':
                self.frame = (self.frame + 1) % 6
            elif self.state == 'run':
                self.frame = (self.frame + 1) % 8
            elif self.state == 'idle':
                self.frame = (self.frame + 1) % 12

        current_speed = 0
        if self.state == 'move':
            current_speed = self.walk_speed
        elif self.state == 'run':
            current_speed = self.run_speed

        dx = self.dir_x * current_speed * frame_time
        dy = self.dir_y * current_speed * frame_time

        map_width = game_map.width
        map_height = game_map.height
        l, b, r, t = self.get_bb()
        half_width = (r - l) / 2
        half_height = (t - b) / 2

        next_bb_x = (l + dx, b, r + dx, t)

        x_collides = False
        for box in game_map.get_collision_boxes():
            if check_collision(next_bb_x, box):
                x_collides = True
                break

        if not x_collides:
            self.world_x += dx

        l, b, r, t = self.get_bb()
        next_bb_y = (l, b + dy, r, t + dy)

        y_collides = False
        for box in game_map.get_collision_boxes():
            if check_collision(next_bb_y, box):
                y_collides = True
                break

        if not y_collides:
            self.world_y += dy

        self.world_x = max(half_width, min(self.world_x, map_width - half_width))
        self.world_y = max(half_height, min(self.world_y, map_height - half_height))



    def activate_skill(self, skill_name):
        current_time = get_time()
        cooldown = self.skill_cooldowns[skill_name]
        last_used = self.skill_last_used[skill_name]
        self.skill_name = skill_name

        if current_time - last_used > cooldown:
            print(f"[{self.skill_name}] 스킬 발동!")

            if self.skill_name == 'skill1':
                self.is_effect_active = True
                self.effect_start_time = current_time
                self.effect_flip_direction = self.direct
                self.state = 'attack'
                self.frame = 0
                self.effect_anim_frame = 0
                self.effect_anim_timer = 0.0

                if self.level == 1:
                    self.effect_total_duration = TIME_PER_ACTION_SKILL1_LVL1
                elif self.level == 2:
                    self.effect_total_duration = TIME_PER_ACTION_SKILL1_LVL2
                elif self.level == 3:
                    self.effect_total_duration = TIME_PER_ACTION_SKILL1_LVL3

            elif self.skill_name == 'skill2':
                self.is_effect_active = True
                self.effect_start_time = current_time
                self.effect_flip_direction = self.direct
                self.state = 'attack'
                self.effect_frame = 0
                self.frame = 0
                self.effect_anim_frame = 0
                self.effect_anim_timer = 0.0

                if self.level == 1:
                    self.effect_total_duration = TIME_PER_ACTION_SKILL2_LVL1
                elif self.level == 2:
                    self.effect_total_duration = TIME_PER_ACTION_SKILL2_LVL2
                elif self.level == 3:
                    self.effect_total_duration = TIME_PER_ACTION_SKILL2_LVL3

            elif self.skill_name == 'skill3':
                if resource_manager.get_image('projectile_LR') or resource_manager.get_image('projectile_UD'):
                    offset_x = 0
                    offset_y = 0
                    if self.direct == 'right':
                        offset_x = 30
                    elif self.direct == 'left':
                        offset_x = -30
                    elif self.direct == 'up':
                        offset_y = 30
                    elif self.direct == 'down':
                        offset_y = -30

                    new_projectile = Projectile(
                        self.world_x + offset_x,
                        self.world_y + offset_y,
                        self.direct,
                        speed=700,
                    )
                    server.world.append(new_projectile)
            self.skill_last_used[self.skill_name] = current_time
        else:
            print(f"[{self.skill_name}] 쿨타임 중!")

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_r:
                self.r_key_pressed = True
            elif event.key == SDLK_a:
                if self.state != 'attack':
                    self.a_key_pressed = True
                    self.state = 'attack'
                    self.frame = 0
                    self.skill_name = 'normal'
            elif event.key == SDLK_LEFT:
                self.dir_x -= 1
            elif event.key == SDLK_RIGHT:
                self.dir_x += 1
            elif event.key == SDLK_DOWN:
                self.dir_y -= 1
            elif event.key == SDLK_UP:
                self.dir_y += 1

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_r:
                self.r_key_pressed = False
            elif event.key == SDLK_a:
                self.a_key_pressed = False
            elif event.key == SDLK_LEFT:
                self.dir_x += 1
            elif event.key == SDLK_RIGHT:
                self.dir_x -= 1
            elif event.key == SDLK_DOWN:
                self.dir_y += 1
            elif event.key == SDLK_UP:
                self.dir_y -= 1

    def get_attack_bb(self):
            l, b, r, t = self.get_bb()
            attack_range = 0
            if self.skill_name == 'skill1':
                attack_range = 75
            elif self.skill_name == 'skill2':
                attack_range = 100
            else:
                attack_range = 50

            if self.direct == 'right':
                return (r, b, r + attack_range, t)
            elif self.direct == 'left':
                return (l - attack_range, b, l, t)
            elif self.direct == 'up':
                return (l, t, r, t + attack_range)
            elif self.direct == 'down':
                return (l, b - attack_range, r, b)
            return self.get_bb()

    def take_damage(self, amount, attacker_x, attacker_y):
        if self.is_hit or self.state == 'dead': return

        self.current_hp -= amount
        print(f"캐릭터 HP: {self.current_hp}")

        if self.current_hp <= 0:
            self.current_hp = 0
            self.state = 'dead'
            self.frame = 0
            self.is_dead_and_animation_finished = False
            return

        self.state = 'hit'
        self.is_hit = True
        self.hit_start_time = get_time()
        self.frame = 0

        dx = self.world_x - attacker_x
        dy = self.world_y - attacker_y
        dist = math.sqrt(dx**2 + dy**2)

        if dist > 0:
            self.knockback_dir_x = dx / dist
            self.knockback_dir_y = dy / dist
        else:
            self.knockback_dir_x = 1
            self.knockback_dir_y = 0

    def get_bb(self):
        half_width = 32
        half_height = 32
        return (self.world_x - half_width, self.world_y - half_height,
                self.world_x + half_width, self.world_y + half_height)

    def respawn(self):
        print("캐릭터가 부활합니다. (마을에서 스폰)")
        self.world_x = 1000
        self.world_y = 350
        self.current_hp = self.max_hp
        self.current_mp = self.max_mp
        self.state = 'idle'
        self.frame = 0
        self.is_hit = False
        self.is_dead_and_animation_finished = False
        self.direct = 'down'
        self.dir_x = 0
        self.dir_y = 0

    def use_potion(self, potion_type):
        if self.state == 'dead' or self.is_hit:
            return

        if potion_type == 'hp':
            if self.hp_potions > 0:
                if self.current_hp < self.max_hp:
                    self.hp_potions -= 1
                    self.current_hp += 50  # HP 회복량
                    self.current_hp = min(self.max_hp, self.current_hp)
                    print(f"HP 포션 사용! 현재 HP: {self.current_hp}")
                else:
                    print("HP가 이미 가득 찼습니다.")
            else:
                print("HP 포션이 없습니다.")

        elif potion_type == 'mp':
            if self.mp_potions > 0:
                if self.current_mp < self.max_mp:
                    self.mp_potions -= 1
                    self.current_mp += 20
                    self.current_mp = min(self.max_mp, self.current_mp)
                    print(f"MP 포션 사용! 현재 MP: {self.current_mp}")
                else:
                    print("MP가 이미 가득 찼습니다.")
            else:
                print("MP 포션이 없습니다.")

    def add_potion(self, potion_type):
        if potion_type == 'hp':
            self.hp_potions += 1
            print(f"HP 포션 획득! (총: {self.hp_potions}개)")
        elif potion_type == 'mp':
            self.mp_potions += 1
            print(f"MP 포션 획득! (총: {self.mp_potions}개)")

    def upgrade_level(self):
        if self.level >= 3:
            return

        self.level += 1
        print(f"--- 장비 업그레이드! 레벨 {self.level} 달성 ---")

        if self.level == 2:
            self.current_images = self.images_lvl2
        elif self.level == 3:
            self.current_images = self.images_lvl3