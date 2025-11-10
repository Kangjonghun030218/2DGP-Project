from pico2d import *
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

cam_x, cam_y = 0, 0
game_mode = 'menu'
knight = None
game_map = None

font = None
dialogue_message = None
quest_log = {
    'check_npc': {
        'status': 'not_started',
        'talked_to_man': False
    }
}

running = True
world = []


class GameMap:
    def __init__(self, map_number=0):
        self.map1_image = load_image('map_1.png')
        self.map2_image = load_image('map_2.png')
        self.map_number = map_number


        if self.map_number == 1:
            self.image = self.map1_image
        elif self.map_number == 2:
            self.image = self.map2_image

        self.width = self.image.w
        self.height = self.image.h
        self.world_x = self.width // 2
        self.world_y = self.height // 2

    def draw(self, cam_x, cam_y):
            screen_x = self.world_x - cam_x
            screen_y = self.world_y - cam_y
            self.image.draw(screen_x, screen_y)

    def update(self):
        pass


class Knight:
    def __init__(self):
        self.world_x = 1000
        self.world_y = 350

        self.image = load_image('Swordsman_lvl1_Idle_with_shadow.png')
        self.image2 = load_image('Swordsman_lvl1_Walk_with_shadow.png')
        self.image3 = load_image('Swordsman_lvl1_Run_with_shadow.png')
        self.image4 = load_image('Swordsman_lvl1_Attack_with_shadow.png')
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

        self.skill_name=''
        self.is_effect_active = False
        self.effect_start_time = 0.0
        self.effect_total_duration = 0.5
        self.effect_frame = 0
        self.effect_flip_direction = 'right'


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

    def draw(self, cam_x, cam_y):
        screen_x = self.world_x - cam_x
        screen_y = self.world_y - cam_y

        clip_y = self.clip_y_table[self.direct]
        if self.state == 'idle':
            self.image.clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)
        elif self.state == 'move':
            self.image2.clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)
        elif self.state == 'run':
            self.image3.clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)
        elif self.state == 'attack':
            self.image4.clip_draw(self.frame * 64, clip_y, 64, 64, screen_x, screen_y)

        if self.skill_name=='skill1':
            if self.is_effect_active:
                base_img1 = None
                flip = ''

                if self.effect_flip_direction == 'left':
                    base_img1 = effect_image1_R1
                    flip = 'h'
                elif self.effect_flip_direction == 'right':
                    base_img1 = effect_image1_R1
                    flip = ''
                elif self.effect_flip_direction == 'down':
                    base_img1 = effect_image1_U1
                    flip = 'v'
                elif self.effect_flip_direction == 'up':
                    base_img1 = effect_image1_U1
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


        elif self.skill_name=='skill2':
            if self.is_effect_active:
                base_img1 = None
                base_img2 = None
                flip = ''


                if self.effect_flip_direction == 'left':
                    base_img1 = effect_image_R1
                    base_img2 = effect_image_R2
                    flip = 'h'
                elif self.effect_flip_direction == 'right':
                    base_img1 = effect_image_R1
                    base_img2 = effect_image_R2
                    flip = ''
                elif self.effect_flip_direction == 'down':
                    base_img1 = effect_image_U1
                    base_img2 = effect_image_U2
                    flip = 'v'
                elif self.effect_flip_direction == 'up':
                    base_img1 = effect_image_U1
                    base_img2 = effect_image_U2
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


    def update(self, map_width=800, map_height=600):
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

        self.world_x += self.dir_x * current_speed
        self.world_y += self.dir_y * current_speed

        half_width = 32
        half_height = 32

        self.world_x = max(half_width, min(self.world_x, map_width - half_width))
        self.world_y = max(half_height, min(self.world_y, map_height - half_height))

    def activate_skill(self, skill_name):
        current_time = get_time()
        cooldown = self.skill_cooldowns[skill_name]
        last_used = self.skill_last_used[skill_name]
        self.skill_name=skill_name

        if current_time - last_used > cooldown:
            print(f"[{self.skill_name}] 스킬 발동!")

            if self.skill_name=='skill1':
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


class NPC:
    def __init__(self):
        self.image1 = load_image('Old_woman_idle.png')
        self.image2 = load_image('Old_man_idle.png')
        self.image3 = load_image('Man_idle.png')
        self.image4 = load_image('Boy_idle.png')
        self.frame = 0

        self.world_x1, self.world_y1 = 550 + 600, 200 + 200
        self.world_x2, self.world_y2 = 50 + 600, 230 + 150
        self.world_x3, self.world_y3 = 150 + 600, 400 + 200
        self.world_x4, self.world_y4 = 300 + 550, 100 + 250

        self.talk_range = 50
    def interact(self, knight_x, knight_y):
        global dialogue_message, quest_log


        dist_to_1 = math.sqrt((self.world_x1 - knight_x) ** 2 + (self.world_y1 - knight_y) ** 2)
        dist_to_2 = math.sqrt((self.world_x2 - knight_x) ** 2 + (self.world_y2 - knight_y) ** 2)
        quest = quest_log['check_npc']


        if dist_to_1 < self.talk_range:
            if quest['status'] == 'not_started':
                dialogue_message = "hello?"
                quest['status'] = 'in_progress'
            elif quest['status'] == 'in_progress':
                if quest['talked_to_man']:
                    dialogue_message = "hi!"
                    quest['status'] = 'completed'
                else:
                    dialogue_message = "nice to meet you"
            elif quest['status'] == 'completed':
                dialogue_message = "thank you."
            return True

        elif dist_to_2 < self.talk_range:
            if quest['status'] == 'not_started':
                dialogue_message = "hello2"
            elif quest['status'] == 'in_progress':
                dialogue_message = "hi2"
                quest['talked_to_man'] = True
            elif quest['status'] == 'completed':
                dialogue_message = "thank you2."
            return True

    def draw(self, cam_x, cam_y):
        screen_x1 = self.world_x1 - cam_x
        screen_y1 = self.world_y1 - cam_y

        screen_x2 = self.world_x2 - cam_x
        screen_y2 = self.world_y2 - cam_y

        screen_x3 = self.world_x3 - cam_x
        screen_y3 = self.world_y3 - cam_y

        screen_x4 = self.world_x4 - cam_x
        screen_y4 = self.world_y4 - cam_y

        self.image1.clip_draw(self.frame * 48, 0, 48, 48, screen_x1, screen_y1)
        self.image2.clip_draw(self.frame * 48, 0, 48, 48, screen_x2, screen_y2)
        self.image3.clip_draw(self.frame * 48, 0, 48, 48, screen_x3, screen_y3)
        self.image4.clip_draw(self.frame * 48, 0, 48, 48, screen_x4, screen_y4)

    def update(self):
        self.frame = (self.frame + 1) % 4


class Monster:
    def __init__(self, x, y, a):
        self.world_x1 = x
        self.world_y1 = y

        if a<=3:
            self.kinMonster=1
        elif a>3:
            self.kinMonster=2

        if a==1:
            self.image1 = load_image('orc1_idle_with_shadow.png')
            self.image2 = load_image('orc1_run_with_shadow.png')
            self.image3 = load_image('orc1_attack_with_shadow.png')
        elif a==2:
            self.image1= load_image('orc2_idle_with_shadow.png')
            self.image2 = load_image('orc2_run_with_shadow.png')
            self.image3 = load_image('orc2_attack_with_shadow.png')
        elif a==3:
            self.image1= load_image('orc3_idle_with_shadow.png')
            self.image2 = load_image('orc3_run_with_shadow.png')
            self.image3=load_image('orc3_attack_with_shadow.png')
        elif a==4:
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
        self.state_dir='down'
        self.face_dirX = 1
        self.face_dirY = 1
        self.speed = 2
        self.aggro_range = 250
        self.attack_range = 50

    def draw(self, cam_x, cam_y):
        screen_x1 = self.world_x1 - cam_x
        screen_y1 = self.world_y1 - cam_y

        if self.state == 'idle':
            if self.state_dir=='right':
                self.image1.clip_draw(self.frame * 64, 0, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir=='left':
                self.image1.clip_draw(self.frame * 64, 64, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir=='up':
                self.image1.clip_draw(self.frame * 64, 128, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir=='down':
                self.image1.clip_draw(self.frame * 64, 192, 64, 64, screen_x1, screen_y1, 100, 100)
        elif self.state == 'chase':
            if self.state_dir=='right':
                self.image2.clip_draw(self.frame * 64, 0, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir=='left':
                self.image2.clip_draw(self.frame * 64, 64, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir=='up':
                self.image2.clip_draw(self.frame * 64, 128, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir=='down':
                self.image2.clip_draw(self.frame * 64, 192, 64, 64, screen_x1, screen_y1, 100, 100)
        elif self.state == 'attack':
            if self.state_dir=='right':
                self.image3.clip_draw(self.frame * 64, 0, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir=='left':
                self.image3.clip_draw(self.frame * 64, 64, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir=='up':
                self.image3.clip_draw(self.frame * 64, 128, 64, 64, screen_x1, screen_y1, 100, 100)
            elif self.state_dir=='down':
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
            elif self.state=='attack':
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






def handle_event():
    global running, game_mode, dialogue_message

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
            return

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
                return
            if game_mode == 'menu':
                game_mode = 'play'
                reset_world(1)
            elif game_mode == 'play':
                if event.key == SDLK_0:
                    game_mode = 'menu'
                elif event.key == SDLK_1:
                    reset_world(1)
                elif event.key == SDLK_2:
                    reset_world(2)
                elif event.key == SDLK_3:
                    game_mode = 'map_view'
                elif event.key == SDLK_7:
                    if knight: knight.activate_skill('skill1')
                elif event.key == SDLK_8:
                    if knight: knight.activate_skill('skill2')
                elif event.key == SDLK_9:
                    if knight: knight.activate_skill('skill3')

                elif event.key == SDLK_SPACE:
                    for obj in world:
                        if isinstance(obj, NPC):
                            if obj.interact(knight.world_x, knight.world_y):
                                game_mode = 'dialogue'
                                break
                else:
                    for obj in world:
                        if isinstance(obj, Knight):
                            obj.handle_event(event)
            elif game_mode == 'map_view':
                if event.key == SDLK_3:
                    game_mode = 'play'
                elif event.key == SDLK_0:
                    game_mode = 'menu'
            elif game_mode == 'dialogue':
                if event.key == SDLK_SPACE:
                    game_mode = 'play'
                    dialogue_message = None
        elif event.type == SDL_KEYUP and game_mode == 'play':
            for obj in world:
                if isinstance(obj, Knight):
                    obj.handle_event(event)


def reset_world(map_number=1):
    global world, cam_x, cam_y, knight, game_map

    cam_x, cam_y = 0, 0
    world = []
    game_map = GameMap(map_number)
    world.append(game_map)
    if map_number == 1:
        npc = NPC()
        world.append(npc)
    elif map_number == 2:
        monster = Monster(400, 400,1)
        monster_1=Monster(380, 400,1)
        monster2=Monster(400, 500,2)
        monster2_1 = Monster(200, 500, 2)
        monster3=Monster(400, 600,3)
        monster3_1 = Monster(100, 600, 3)
        monster4=Monster(400, 700,4)
        monster4_1=Monster(500, 700,4)
        monster5=Monster(400, 800,5)
        monster5_1 = Monster(570, 800, 5)
        monster6=Monster(400, 900,6)
        monster6_1 = Monster(600, 900, 6)
        world.append(monster)
        world.append(monster2)
        world.append(monster3)
        world.append(monster4)
        world.append(monster5)
        world.append(monster6)
        world.append(monster_1)
        world.append(monster2_1)
        world.append(monster3_1)
        world.append(monster4_1)
        world.append(monster5_1)
        world.append(monster6_1)

    if knight is None:
        knight = Knight()
    world.append(knight)


def update_world():
    global world, cam_x, cam_y, game_mode, knight, game_map

    if game_mode != 'play':
        return

    if knight and game_map:
        for obj in world:
            if obj is knight:
                obj.update(game_map.width, game_map.height)
            elif isinstance(obj, Monster):
                obj.update(knight.world_x, knight.world_y)
            else:
                obj.update()
    else:
        for obj in world:
            obj.update()

    if knight and game_map:
        target_cam_x = knight.world_x - CANVAS_WIDTH // 2
        target_cam_y = knight.world_y - CANVAS_HEIGHT // 2

        min_cam_x = 0
        max_cam_x = game_map.width - CANVAS_WIDTH

        min_cam_y = 0
        max_cam_y = game_map.height - CANVAS_HEIGHT

        cam_x = max(min_cam_x, min(target_cam_x, max_cam_x))
        cam_y = max(min_cam_y, min(target_cam_y, max_cam_y))

        if max_cam_x < 0: cam_x = 0
        if max_cam_y < 0: cam_y = 0


def render_world():
    global world, cam_x, cam_y, game_mode, knight, game_map,menu_image

    clear_canvas()

    if game_mode == 'play':
        for object in world:
            object.draw(cam_x, cam_y)
        draw_ui()

    elif game_mode == 'map_view':
        if game_map:
            game_map.image.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, CANVAS_WIDTH, CANVAS_HEIGHT)
            if knight:
                 screen_x = (knight.world_x / game_map.width) * CANVAS_WIDTH
                 screen_y = (knight.world_y / game_map.height) * CANVAS_HEIGHT
                 clip_y_down = 192
                 knight.image.clip_draw(0, clip_y_down, 64, 64, screen_x, screen_y, 100, 100)
    elif game_mode == 'menu':
        if menu_image:
            menu_image.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, CANVAS_WIDTH, CANVAS_HEIGHT)

    elif game_mode == 'dialogue':
        for object in world:
            object.draw(cam_x, cam_y)

        if dialogue_message and font:
            font.draw(101, 101, dialogue_message, (0, 0, 0))  # -- > 그림자 디테일 ~
            font.draw(100, 100, dialogue_message, (225, 180, 200))

    update_canvas()


open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
menu_image = load_image('map_0.png')
font = load_font('ARIAL.ttf', 20)
#reset_world(1)

bar_bg_image = load_image('bar_bg.png')
hp_bar_image = load_image('bar_hp.png')
mp_bar_image = load_image('bar_mp.png')

skill1_image = load_image('skill1.png')
skill2_image = load_image('skill2.png')
skill3_image = load_image('skill3.png')

effect_image_R1 = load_image('skill2-1_R.png')
effect_image_R2 = load_image('skill2-2_R.png')
effect_image_U1 = load_image('skill2-1_U.png')
effect_image_U2 = load_image('skill2-2_U.png')

effect_image1_R1 = load_image('skill1-1_R.png')
effect_image1_U1 = load_image('skill1-1_U.png')



def draw_ui():
    if not knight or not bar_bg_image or not hp_bar_image or not mp_bar_image:
        if font:
            font.draw(20, CANVAS_HEIGHT - 30, "UI Image Load Error", (255, 0, 0))
        return


    bar_max_width = 200
    bar_height = 20
    ui_x = 20
    hp_bar_y = CANVAS_HEIGHT - 35
    mp_bar_y = CANVAS_HEIGHT - 65

  #hp 관련
    hp_ratio = knight.current_hp / knight.max_hp
    current_hp_width = int(bar_max_width * hp_ratio)
    bar_bg_image.draw(ui_x + bar_max_width // 2, hp_bar_y + bar_height // 2, bar_max_width, bar_height)



    if current_hp_width > 0:
        draw_x = ui_x + current_hp_width // 2
        hp_bar_image.draw(draw_x, hp_bar_y + bar_height // 2, current_hp_width, bar_height)

    #mp 관련
    mp_ratio = knight.current_mp / knight.max_mp
    current_mp_width = int(bar_max_width * mp_ratio)
    bar_bg_image.draw(ui_x + bar_max_width // 2, mp_bar_y + bar_height // 2, bar_max_width, bar_height)


    if current_mp_width > 0:
        draw_x_mp = ui_x + current_mp_width // 2
        mp_bar_image.draw(draw_x_mp, mp_bar_y + bar_height // 2, current_mp_width, bar_height)


    text_x = 20
    if font:
        hp_text = f"HP: {knight.current_hp} / {knight.max_hp}"
        mp_text = f"MP: {knight.current_mp} / {knight.max_mp}"


        font.draw(text_x + 6, hp_bar_y + 4, hp_text, (0, 0, 0))
        font.draw(text_x + 6, mp_bar_y + 4, mp_text, (0, 0, 0))

        font.draw(text_x + 5, hp_bar_y + 5, hp_text, (255, 255, 255))
        font.draw(text_x + 5, mp_bar_y + 5, mp_text, (255, 255, 255))

    if not (skill1_image and skill2_image and skill3_image):
        return

    current_time = get_time()
    icon_size = 48
    icon_spacing = 10
    icon_y = 40

    center_x = CANVAS_WIDTH // 2
    skill2_x = center_x
    skill1_x = center_x - icon_size - icon_spacing
    skill3_x = center_x + icon_size + icon_spacing

    positions = {
        'skill1': skill1_x,
        'skill2': skill2_x,
        'skill3': skill3_x
    }
    images = {
        'skill1': skill1_image,
        'skill2': skill2_image,
        'skill3': skill3_image
    }
    keys = {'skill1': '7', 'skill2': '8', 'skill3': '9'}

    for skill_name in ['skill1', 'skill2', 'skill3']:
        x = positions[skill_name]
        image = images[skill_name]

        cooldown = knight.skill_cooldowns[skill_name]
        time_elapsed = current_time - knight.skill_last_used[skill_name]

        if time_elapsed < cooldown:
            image.opacify(0.3)
            image.draw(x, icon_y, icon_size, icon_size)
            image.opacify(1.0)


            remaining_time = cooldown - time_elapsed
            if font:
                font.draw(x - 10, icon_y, f"{remaining_time:.1f}", (255, 0, 0))
        else:
            image.draw(x, icon_y, icon_size, icon_size)

        if font:
            key_text_y = icon_y + icon_size // 2 + 10
            font.draw(x - 5, key_text_y, keys[skill_name], (255, 255, 0))





while running:
    handle_event()
    update_world()
    render_world()
    delay(0.05)

close_canvas()