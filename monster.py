from pico2d import *
import math
import game_globals as g

PIXEL_PER_METER = (10.0 / 0.3)

#몬스터 추적 속도
MONSTER_SPEED_KMPH = 30.0  # Km / Hour
MONSTER_SPEED_MPM = (MONSTER_SPEED_KMPH * 1000.0 / 60.0)
MONSTER_SPEED_MPS = (MONSTER_SPEED_MPM / 60.0)
MONSTER_SPEED_PPS = (MONSTER_SPEED_MPS * PIXEL_PER_METER) # Pixel / Sec

#몬스터 넉백 속도
KNOCKBACK_SPEED_KMPH = 10.0
KNOCKBACK_SPEED_MPM = (KNOCKBACK_SPEED_KMPH * 1000.0 / 60.0)
KNOCKBACK_SPEED_MPS = (KNOCKBACK_SPEED_MPM / 60.0)
KNOCKBACK_SPEED_PPS = (KNOCKBACK_SPEED_MPS * PIXEL_PER_METER)


#오크
TIME_PER_ACTION_ORC_IDLE = 1.0
FRAMES_PER_ACTION_ORC_IDLE = 4
TIME_PER_FRAME_ORC_IDLE = TIME_PER_ACTION_ORC_IDLE / FRAMES_PER_ACTION_ORC_IDLE

TIME_PER_ACTION_ORC_CHASE = 0.8
FRAMES_PER_ACTION_ORC_CHASE = 8
TIME_PER_FRAME_ORC_CHASE = TIME_PER_ACTION_ORC_CHASE / FRAMES_PER_ACTION_ORC_CHASE

TIME_PER_ACTION_ORC_ATTACK = 0.8
FRAMES_PER_ACTION_ORC_ATTACK = 8
TIME_PER_FRAME_ORC_ATTACK = TIME_PER_ACTION_ORC_ATTACK / FRAMES_PER_ACTION_ORC_ATTACK

TIME_PER_ACTION_ORC_HIT = 0.6
FRAMES_PER_ACTION_ORC_HIT = 6
TIME_PER_FRAME_ORC_HIT = TIME_PER_ACTION_ORC_HIT / FRAMES_PER_ACTION_ORC_HIT

TIME_PER_ACTION_ORC_DEAD = 1.6
FRAMES_PER_ACTION_ORC_DEAD = 8
TIME_PER_FRAME_ORC_DEAD = TIME_PER_ACTION_ORC_DEAD / FRAMES_PER_ACTION_ORC_DEAD


#슬라임
TIME_PER_ACTION_SLIME_IDLE = 1.2
FRAMES_PER_ACTION_SLIME_IDLE = 6
TIME_PER_FRAME_SLIME_IDLE = TIME_PER_ACTION_SLIME_IDLE / FRAMES_PER_ACTION_SLIME_IDLE

TIME_PER_ACTION_SLIME_CHASE = 0.8
FRAMES_PER_ACTION_SLIME_CHASE = 8
TIME_PER_FRAME_SLIME_CHASE = TIME_PER_ACTION_SLIME_CHASE / FRAMES_PER_ACTION_SLIME_CHASE

TIME_PER_ACTION_SLIME_ATTACK = 1.0
FRAMES_PER_ACTION_SLIME_ATTACK = 10
TIME_PER_FRAME_SLIME_ATTACK = TIME_PER_ACTION_SLIME_ATTACK / FRAMES_PER_ACTION_SLIME_ATTACK

TIME_PER_ACTION_SLIME_HIT = 0.5
FRAMES_PER_ACTION_SLIME_HIT = 5
TIME_PER_FRAME_SLIME_HIT = TIME_PER_ACTION_SLIME_HIT / FRAMES_PER_ACTION_SLIME_HIT

TIME_PER_ACTION_SLIME_DEAD = 2.0
FRAMES_PER_ACTION_SLIME_DEAD = 10
TIME_PER_FRAME_SLIME_DEAD = TIME_PER_ACTION_SLIME_DEAD / FRAMES_PER_ACTION_SLIME_DEAD

class Monster:
    def __init__(self, x, y, a):
        self.world_x1 = x
        self.world_y1 = y
        self.monster_type = a
        if a <= 3:
            self.kinMonster = 1
            self.max_hp = 100
        elif a > 3:
            self.kinMonster = 2
            self.max_hp = 50
        self.current_hp = self.max_hp

        if a == 1:
            self.image1 = load_image('orc1_idle_with_shadow.png')
            self.image2 = load_image('orc1_run_with_shadow.png')
            self.image3 = load_image('orc1_attack_with_shadow.png')
            self.image4=load_image('orc1_hurt_with_shadow.png')
            self.image5 = load_image('orc1_death_with_shadow.png')
        elif a == 2:
            self.image1 = load_image('orc2_idle_with_shadow.png')
            self.image2 = load_image('orc2_run_with_shadow.png')
            self.image3 = load_image('orc2_attack_with_shadow.png')
            self.image4 = load_image('orc2_hurt_with_shadow.png')
            self.image5 = load_image('orc2_death_with_shadow.png')
        elif a == 3:
            self.image1 = load_image('orc3_idle_with_shadow.png')
            self.image2 = load_image('orc3_run_with_shadow.png')
            self.image3 = load_image('orc3_attack_with_shadow.png')
            self.image4 = load_image('orc3_hurt_with_shadow.png')
            self.image5 = load_image('orc3_death_with_shadow.png')
        elif a == 4:
            self.image1 = load_image('Slime1_Idle_with_shadow.png')
            self.image2 = load_image('Slime1_Run_with_shadow.png')
            self.image3 = load_image('Slime1_Attack_with_shadow.png')
            self.image4 = load_image('Slime1_Hurt_with_shadow.png')
            self.image5 = load_image('Slime1_Death_with_shadow.png')
        elif a == 5:
            self.image1 = load_image('Slime2_Idle_with_shadow.png')
            self.image2 = load_image('Slime2_Run_with_shadow.png')
            self.image3 = load_image('Slime2_Attack_with_shadow.png')
            self.image4 = load_image('Slime2_Hurt_with_shadow.png')
            self.image5 = load_image('Slime2_Death_with_shadow.png')
        elif a == 6:
            self.image1 = load_image('Slime3_Idle_with_shadow.png')
            self.image2 = load_image('Slime3_Run_with_shadow.png')
            self.image3 = load_image('Slime3_Attack_with_shadow.png')
            self.image4 = load_image('Slime3_Hurt_with_shadow.png')
            self.image5 = load_image('Slime3_Death_with_shadow.png')

        self.frame = 0
        self.frame_timer = 0.0
        self.state = 'idle'
        self.state_dir = 'down'
        self.speed = MONSTER_SPEED_PPS

        self.aggro_range = 250
        self.attack_range = 50


        self.is_hit = False
        self.hit_start_time = 0.0
        self.hit_duration = 0.3
        self.knockback_dir_x = 0
        self.knockback_dir_y = 0
        self.knockback_speed = KNOCKBACK_SPEED_PPS

        if self.kinMonster == 1:
            self.death_max_frame = 8
        elif self.kinMonster == 2:
            self.death_max_frame = 10

        self.is_removable = False

        self.debug_mode = g.DEBUG_MODE_ON

        if self.kinMonster == 1:  # 오크
            self.time_per_frame_idle = TIME_PER_FRAME_ORC_IDLE
            self.time_per_frame_chase = TIME_PER_FRAME_ORC_CHASE
            self.time_per_frame_attack = TIME_PER_FRAME_ORC_ATTACK
            self.time_per_frame_hit = TIME_PER_FRAME_ORC_HIT
            self.time_per_frame_dead = TIME_PER_FRAME_ORC_DEAD

            self.frames_idle = FRAMES_PER_ACTION_ORC_IDLE
            self.frames_chase = FRAMES_PER_ACTION_ORC_CHASE
            self.frames_attack = FRAMES_PER_ACTION_ORC_ATTACK
            self.frames_hit = FRAMES_PER_ACTION_ORC_HIT
            self.frames_dead = FRAMES_PER_ACTION_ORC_DEAD
        else:  # 슬라임
            self.time_per_frame_idle = TIME_PER_FRAME_SLIME_IDLE
            self.time_per_frame_chase = TIME_PER_FRAME_SLIME_CHASE
            self.time_per_frame_attack = TIME_PER_FRAME_SLIME_ATTACK
            self.time_per_frame_hit = TIME_PER_FRAME_SLIME_HIT
            self.time_per_frame_dead = TIME_PER_FRAME_SLIME_DEAD

            self.frames_idle = FRAMES_PER_ACTION_SLIME_IDLE
            self.frames_chase = FRAMES_PER_ACTION_SLIME_CHASE
            self.frames_attack = FRAMES_PER_ACTION_SLIME_ATTACK
            self.frames_hit = FRAMES_PER_ACTION_SLIME_HIT
            self.frames_dead = FRAMES_PER_ACTION_SLIME_DEAD

        self.images = {
            'idle': self.image1,
            'chase': self.image2,
            'attack': self.image3,
            'hit': self.image4,
            'dead': self.image5
        }
        self.clip_y_table = {
            'right': 0,
            'left': 64,
            'up': 128,
            'down': 192
        }



    def get_bb(self):
        half_width = 32
        half_height = 32
        return (self.world_x1 - half_width, self.world_y1 - half_height,
                self.world_x1 + half_width, self.world_y1 + half_height)



    def take_damage(self, amount, attacker_x, attacker_y):
        if self.is_hit: return

        self.current_hp -= amount
        print(f"몬스터 HP: {self.current_hp}")


        if self.current_hp <= 0:
            self.state = 'dead'
            return


        self.state = 'hit'
        self.is_hit = True
        self.hit_start_time = get_time()
        self.frame = 0


        dx = self.world_x1 - attacker_x
        dy = self.world_y1 - attacker_y
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist > 0:
            self.knockback_dir_x = dx / dist
            self.knockback_dir_y = dy / dist
        else:
            self.knockback_dir_x = 1
            self.knockback_dir_y = 0

    def draw(self, cam_x, cam_y):
        screen_x1 = self.world_x1 - cam_x
        screen_y1 = self.world_y1 - cam_y

        if self.debug_mode:
            l, b, r, t = self.get_bb()
            screen_l, screen_b = l - cam_x, b - cam_y
            screen_r, screen_t = r - cam_x, t - cam_y
            draw_rectangle(screen_l, screen_b, screen_r, screen_t)

        if self.state in self.images:
            image_to_draw = self.images[self.state]
            clip_y = self.clip_y_table.get(self.state_dir, 192)

            image_to_draw.clip_draw(
                self.frame * 64, clip_y, 64, 64,
                screen_x1, screen_y1,
                100, 100
            )

    def update(self, frame_time, knight_x=None, knight_y=None):
        self.frame_timer += frame_time
        if self.state == 'dead':
            if self.frame_timer >= self.time_per_frame_dead:
                self.frame_timer -= self.time_per_frame_dead
                if self.frame < self.frames_dead - 1:
                    self.frame += 1
                else:
                    self.is_removable = True
            return

        if self.is_hit:
            current_time = get_time()
            if current_time - self.hit_start_time < self.hit_duration:
                self.world_x1 += self.knockback_dir_x * self.knockback_speed * frame_time
                self.world_y1 += self.knockback_dir_y * self.knockback_speed * frame_time

                if self.frame_timer >= self.time_per_frame_hit:
                    self.frame_timer -= self.time_per_frame_hit
                    self.frame = (self.frame + 1) % self.frames_hit
                return
            else:
                self.is_hit = False
                self.state = 'idle'
                self.frame = 0


        current_anim_speed = 0.1
        current_max_frames = 1
        if self.state == 'idle':
            current_anim_speed = self.time_per_frame_idle
            current_max_frames = self.frames_idle
        elif self.state == 'chase':
            current_anim_speed = self.time_per_frame_chase
            current_max_frames = self.frames_chase
        elif self.state == 'attack':
            current_anim_speed = self.time_per_frame_attack
            current_max_frames = self.frames_attack

        if self.frame_timer >= current_anim_speed:
            self.frame_timer -= current_anim_speed
            self.frame = (self.frame + 1) % current_max_frames

        if knight_x is None or knight_y is None:
            if self.state != 'idle':
                self.state = 'idle'
                self.frame = 0
            return

        dist_x = knight_x - self.world_x1
        dist_y = knight_y - self.world_y1
        distance_sq = dist_x ** 2 + dist_y ** 2

        new_state = self.state
        if distance_sq < self.attack_range ** 2:
            new_state = 'attack'
        elif distance_sq < self.aggro_range ** 2:
            new_state = 'chase'
        else:
            new_state = 'idle'

        if self.state != new_state:
            self.state = new_state
            self.frame = 0



        if self.state == 'chase':
            distance = math.sqrt(distance_sq)
            if distance > 0:
                dir_x = dist_x / distance
                dir_y = dist_y / distance

                self.world_x1 += dir_x * self.speed * frame_time
                self.world_y1 += dir_y * self.speed * frame_time

                if abs(dist_x) > abs(dist_y):
                    if dist_x > 0:
                        self.state_dir = 'right'
                    else:
                        self.state_dir = 'left'
                else:
                    if dist_y > 0:
                        self.state_dir = 'up'
                    else:
                        self.state_dir = 'down'