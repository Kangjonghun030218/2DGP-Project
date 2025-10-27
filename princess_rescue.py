from pico2d import *
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

cam_x, cam_y = 0, 0


class Village:
    def __init__(self):
        self.image = load_image('map_1.png')

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

        self.clip_y_table = {
            'down': 192,
            'left': 128,
            'right': 64,
            'up': 0
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

    def update(self, map_width=800, map_height=600):
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

        self.world_x1, self.world_y1 = 550+600, 200+150
        self.world_x2, self.world_y2 = 50+600, 230+150
        self.world_x3, self.world_y3 = 150+600, 400+150
        self.world_x4, self.world_y4 = 300+600, 100+150

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


running = True
world = []


def handle_event():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            for obj in world:
                if isinstance(obj, Knight):
                    obj.handle_event(event)


def reset_world():
    global world, cam_x, cam_y

    cam_x, cam_y = 0, 0

    world = []
    map_1 = Village()
    knight = Knight()
    npc = NPC()

    world.append(map_1)
    world.append(npc)
    world.append(knight)


def update_world():
    global world, cam_x, cam_y

    knight = None
    village = None

    for obj in world:
        if isinstance(obj, Knight):
            knight = obj
        elif isinstance(obj, Village):
            village = obj

    if knight and village:
        for obj in world:
            if obj is knight:
                obj.update(village.width, village.height)
            else:
                obj.update()
    else:
        for obj in world:
            obj.update()

    if knight and village:
        target_cam_x = knight.world_x - CANVAS_WIDTH // 2
        target_cam_y = knight.world_y - CANVAS_HEIGHT // 2

        min_cam_x = 0
        max_cam_x = village.width - CANVAS_WIDTH

        min_cam_y = 0
        max_cam_y = village.height - CANVAS_HEIGHT

        cam_x = max(min_cam_x, min(target_cam_x, max_cam_x))
        cam_y = max(min_cam_y, min(target_cam_y, max_cam_y))

        if max_cam_x < 0: cam_x = 0
        if max_cam_y < 0: cam_y = 0


def render_world():
    global world, cam_x, cam_y

    clear_canvas()
    for object in world:
        object.draw(cam_x, cam_y)
    update_canvas()


open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
reset_world()
while running:
    handle_event()
    update_world()
    render_world()
    delay(0.05)