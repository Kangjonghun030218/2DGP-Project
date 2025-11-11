from pico2d import *
import math

class Monster:
    def __init__(self, x, y, a):
        self.world_x1 = x
        self.world_y1 = y

        if a <= 3:
            self.kinMonster = 1
        elif a > 3:
            self.kinMonster = 2

        if a == 1:
            self.image1 = load_image('orc1_idle_with_shadow.png')
            self.image2 = load_image('orc1_run_with_shadow.png')
            self.image3 = load_image('orc1_attack_with_shadow.png')
        elif a == 2:
            self.image1 = load_image('orc2_idle_with_shadow.png')
            self.image2 = load_image('orc2_run_with_shadow.png')
            self.image3 = load_image('orc2_attack_with_shadow.png')
        elif a == 3:
            self.image1 = load_image('orc3_idle_with_shadow.png')
            self.image2 = load_image('orc3_run_with_shadow.png')
            self.image3 = load_image('orc3_attack_with_shadow.png')
        elif a == 4:
            self.image1 = load_image('Slime1_Idle_with_shadow.png')
            self.image2 = load_image('Slime1_Run_with_shadow.png')
            self.image3 = load_image('Slime1_Attack_with_shadow.png')
        elif a == 5:
            self.image1 = load_image('Slime2_Idle_with_shadow.png')
            self.image2 = load_image('Slime2_Run_with_shadow.png')
            self.image3 = load_image('Slime2_Attack_with_shadow.png')
        elif a == 6:
            self.image1 = load_image('Slime3_Idle_with_shadow.png')
            self.image2 = load_image('Slime3_Run_with_shadow.png')
            self.image3 = load_image('Slime3_Attack_with_shadow.png')

        self.frame = 0
        self.state = 'idle'
        self.state_dir = 'down'
        self.face_dirX = 1
        self.face_dirY = 1
        self.speed = 2
        self.aggro_range = 250
        self.attack_range = 50

    def draw(self, cam_x, cam_y):
        screen_x1 = self.world_x1 - cam_x
        screen_y1 = self.world_y1 - cam_y

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

    def update(self, knight_x=None, knight_y=None):
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