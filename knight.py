from pico2d import *
import game_globals as g
from projectile import Projectile


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
        self.world_x = 1000
        self.world_y = 350

        self.image = load_image('Swordsman_lvl1_Idle_with_shadow.png')
        self.image2 = load_image('Swordsman_lvl1_Walk_with_shadow.png')
        self.image3 = load_image('Swordsman_lvl1_Run_with_shadow.png')
        self.image4 = load_image('Swordsman_lvl1_Attack_with_shadow.png')
        self.image5= load_image('Swordsman_lvl1_Hurt_with_shadow.png')

        self.frame = 0
        self.speed = 5
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


        self.is_hit = False
        self.hit_start_time = 0.0
        self.hit_duration = 0.3
        self.knockback_dir_x = 0
        self.knockback_dir_y = 0
        self.knockback_speed = 10

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

        self.face_dirX = 1
        self.face_dirY = 1

        self.debug_mode = g.DEBUG_MODE_ON

    def draw(self, cam_x, cam_y):
        screen_x = self.world_x - cam_x
        screen_y = self.world_y - cam_y
        if self.debug_mode:
            l, b, r, t = self.get_bb()

            screen_l, screen_b = l - cam_x, b - cam_y
            screen_r, screen_t = r - cam_x, t - cam_y

            draw_rectangle(screen_l, screen_b, screen_r, screen_t)


        clip_y = self.clip_y_table[self.direct]
        if self.state == 'idle':
            self.image.clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)
        elif self.state == 'move':
            self.image2.clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)
        elif self.state == 'run':
            self.image3.clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)
        elif self.state == 'attack':
            self.image4.clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)
        elif self.state == 'hit':
            self.image5.clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)

        if self.skill_name == 'skill1':
            if self.is_effect_active:
                base_img1 = None
                flip = ''

                if self.effect_flip_direction == 'left':
                    base_img1 = g.effect_image1_R1
                    flip = 'h'
                elif self.effect_flip_direction == 'right':
                    base_img1 = g.effect_image1_R1
                    flip = ''
                elif self.effect_flip_direction == 'down':
                    base_img1 = g.effect_image1_U1
                    flip = 'v'
                elif self.effect_flip_direction == 'up':
                    base_img1 = g.effect_image1_U1
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
                base_img1 = None
                base_img2 = None
                flip = ''

                if self.effect_flip_direction == 'left':
                    base_img1 = g.effect_image_R1
                    base_img2 = g.effect_image_R2
                    flip = 'h'
                elif self.effect_flip_direction == 'right':
                    base_img1 = g.effect_image_R1
                    base_img2 = g.effect_image_R2
                    flip = ''
                elif self.effect_flip_direction == 'down':
                    base_img1 = g.effect_image_U1
                    base_img2 = g.effect_image_U2
                    flip = 'v'
                elif self.effect_flip_direction == 'up':
                    base_img1 = g.effect_image_U1
                    base_img2 = g.effect_image_U2
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

    def update(self, game_map):
        if self.is_hit:
            current_time = get_time()
            if current_time - self.hit_start_time < self.hit_duration:
                # 넉백 적용 (맵 경계나 장애물 충돌은 미적용된 단순 넉백)
                self.world_x += self.knockback_dir_x * self.knockback_speed
                self.world_y += self.knockback_dir_y * self.knockback_speed
                self.frame = (self.frame + 1) % 5

                map_width = game_map.width
                map_height = game_map.height
                l, b, r, t = self.get_bb()
                half_width = (r - l) / 2
                half_height = (t - b) / 2
                self.world_x = max(half_width, min(self.world_x, map_width - half_width))
                self.world_y = max(half_height, min(self.world_y, map_height - half_height))

                return
            else:
                self.is_hit = False
                self.state = 'idle'

        if self.is_effect_active:
            time_since_start = get_time() - self.effect_start_time
            half_duration = self.effect_total_duration / 2

            if time_since_start < half_duration:
                self.effect_frame = 0
            elif time_since_start < self.effect_total_duration:
                self.effect_frame = 1
            else:
                self.is_effect_active = False

        if self.state == 'attack':
            self.frame = (self.frame + 1)
            if self.frame >= 8:
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
            current_speed = self.speed
        elif self.state == 'run':
            current_speed = self.speed * 2

        dx = self.dir_x * current_speed
        dy = self.dir_y * current_speed

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

            elif self.skill_name == 'skill2':
                self.is_effect_active = True
                self.effect_start_time = current_time
                self.effect_flip_direction = self.direct
                self.state = 'attack'
                self.effect_frame = 0
                self.frame = 0

            elif self.skill_name == 'skill3':
                if g.projectile_image_LR or g.projectile_image_UD:
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
                        speed=15,
                    )
                    g.world.append(new_projectile)
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
        if self.is_hit: return

        self.current_hp -= amount
        print(f"캐릭터 HP: {self.current_hp}")

        if self.current_hp <= 0:
            print("GAME OVER")
            # self.state = 'dead'
            pass

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