from pico2d import *
import math
import game_globals as g

class Monster:
    def __init__(self, x, y, a):
        self.world_x1 = x
        self.world_y1 = y

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
        self.state = 'idle'
        self.state_dir = 'down'
        self.face_dirX = 1
        self.face_dirY = 1
        self.speed = 2
        self.aggro_range = 250
        self.attack_range = 50


        self.is_hit = False
        self.hit_start_time = 0.0
        self.hit_duration = 0.3
        self.knockback_dir_x = 0
        self.knockback_dir_y = 0
        self.knockback_speed = 10

        if self.kinMonster == 1:
            self.death_max_frame = 8
        elif self.kinMonster == 2:
            self.death_max_frame = 10

        self.is_removable = False

        self.debug_mode = g.DEBUG_MODE_ON



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

        if self.state == 'idle':
            if self.state_dir == 'right':
                self.image1.clip_draw(self.frame * 64, 0, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'left':
                self.image1.clip_draw(self.frame * 64, 64, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'up':
                self.image1.clip_draw(self.frame * 64, 128, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'down':
                self.image1.clip_draw(self.frame * 64, 192, 64, 64, screen_x1, screen_y1, 100, 100)
        elif self.state == 'chase':
            if self.state_dir == 'right':
                self.image2.clip_draw(self.frame * 64, 0, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'left':
                self.image2.clip_draw(self.frame * 64, 64, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'up':
                self.image2.clip_draw(self.frame * 64, 128, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'down':
                self.image2.clip_draw(self.frame * 64, 192, 64, 64, screen_x1, screen_y1, 100, 100)
        elif self.state == 'attack':
            if self.state_dir == 'right':
                self.image3.clip_draw(self.frame * 64, 0, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'left':
                self.image3.clip_draw(self.frame * 64, 64, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'up':
                self.image3.clip_draw(self.frame * 64, 128, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'down':
                self.image3.clip_draw(self.frame * 64, 192, 64, 64, screen_x1, screen_y1, 100, 100)
        elif self.state == 'hit':
            if self.state_dir == 'right':
                self.image4.clip_draw(self.frame * 64, 0, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'left':
                self.image4.clip_draw(self.frame * 64, 64, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'up':
                self.image4.clip_draw(self.frame * 64, 128, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'down':
                self.image4.clip_draw(self.frame * 64, 192, 64, 64, screen_x1, screen_y1, 100, 100)
        elif self.state == 'dead':
            if self.state_dir == 'right':
                    self.image5.clip_draw(self.frame * 64, 0, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'left':
                    self.image5.clip_draw(self.frame * 64, 64, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'up':
                    self.image5.clip_draw(self.frame * 64, 128, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir == 'down':
                    self.image5.clip_draw(self.frame * 64, 192, 64, 64, screen_x1, screen_y1, 100, 100)

    def update(self, knight_x=None, knight_y=None):
        if self.state == 'dead':
            if self.frame < self.death_max_frame - 1:
                self.frame = (self.frame + 1)
            else:
                self.frame = self.death_max_frame - 1
                self.is_removable = True
            return

        if self.is_hit:
            current_time = get_time()
            if current_time - self.hit_start_time < self.hit_duration:
                self.world_x1 += self.knockback_dir_x * self.knockback_speed
                self.world_y1 += self.knockback_dir_y * self.knockback_speed
                if self.kinMonster==1:
                    self.frame = (self.frame + 1) % 6
                elif self.kinMonster==2:
                    self.frame = (self.frame + 2) % 5
                return
            else:
                self.is_hit = False
                self.state = 'idle'

        if self.kinMonster == 1:
            if self.state == 'idle':
                self.frame = (self.frame + 1) % 4
            elif self.state == 'chase' or self.state == 'attack':
                self.frame = (self.frame + 1) % 8


        elif self.kinMonster == 2:
            if self.state == 'idle':
                self.frame = (self.frame + 1) % 6
            elif self.state == 'chase':
                self.frame = (self.frame + 1) % 8
            elif self.state == 'attack':
                self.frame = (self.frame + 1) % 10


        if knight_x is None or knight_y is None:
            self.state = 'idle'
            return

        dist_x = knight_x - self.world_x1
        dist_y = knight_y - self.world_y1
        distance_sq = dist_x ** 2 + dist_y ** 2

        if distance_sq < self.attack_range ** 2:
            self.state = 'attack'
        elif distance_sq < self.aggro_range ** 2:
            self.state = 'chase'
        else:
            self.state = 'idle'

        if self.state == 'chase':
            distance = math.sqrt(distance_sq)
            if distance > 0:
                dir_x = dist_x / distance
                dir_y = dist_y / distance

                self.world_x1 += dir_x * self.speed
                self.world_y1 += dir_y * self.speed

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