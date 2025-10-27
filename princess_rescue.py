from pico2d import *
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600


class Village:
    def __init__(self):
        self.image = load_image('map_1.png')
        self.x = 400
        self.y = 300

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self, move_x=0, move_y=0):
        self.x -= move_x
        self.y -= move_y


class Knight:
    def __init__(self):
        self.x = CANVAS_WIDTH // 2
        self.y = CANVAS_HEIGHT // 2

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

        self.move_x = 0
        self.move_y = 0

        self.clip_y_table = {
            'down': 192,
            'left': 128,
            'right': 64,
            'up': 0
        }
        self.face_dirX = 1
        self.face_dirY = 1
#
    def draw(self):
        clip_y = self.clip_y_table[self.direct]
        if self.state == 'idle':
            self.image.clip_draw(self.frame * 64, clip_y, 64, 64, self.x, self.y)
        elif self.state == 'move':
            self.image2.clip_draw(self.frame * 64, clip_y, 64, 64, self.x, self.y)
        elif self.state == 'run':
            self.image3.clip_draw(self.frame * 64, clip_y, 64, 64, self.x, self.y)
        elif self.state == 'attack':
            self.image4.clip_draw(self.frame * 64, clip_y, 64, 64, self.x, self.y)

    def update(self):
        if self.state == 'attack':
            self.frame = (self.frame + 1)
            if self.frame >= 8:
                self.state = 'idle'
                self.frame = 0
            self.move_x = 0
            self.move_y = 0
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

        self.move_x = self.dir_x * current_speed
        self.move_y = self.dir_y * current_speed

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

        self.x1, self.y1 = 550, 200
        self.x2, self.y2 = 50, 230
        self.x3, self.y3 = 150, 400
        self.x4, self.y4 = 300, 100

    def draw(self):
        self.image1.clip_draw(self.frame * 48, 0, 48, 48, self.x1, self.y1)
        self.image2.clip_draw(self.frame * 48, 0, 48, 48, self.x2, self.y2)
        self.image3.clip_draw(self.frame * 48, 0, 48, 48, self.x3, self.y3)
        self.image4.clip_draw(self.frame * 48, 0, 48, 48, self.x4, self.y4)

    def update(self, move_x=0, move_y=0):
        self.frame = (self.frame + 1) % 4

        self.x1 -= move_x
        self.y1 -= move_y

        self.x2 -= move_x
        self.y2 -= move_y

        self.x3 -= move_x
        self.y3 -= move_y

        self.x4 -= move_x
        self.y4 -= move_y


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
    global world
    world = []
    map_1 = Village()
    knight = Knight()
    npc = NPC()

    world.append(map_1)
    world.append(npc)
    world.append(knight)


def update_world():
    knight = None
    for obj in world:
        if isinstance(obj, Knight):
            knight = obj
            break

    if knight:
        knight.update()

        move_x = knight.move_x
        move_y = knight.move_y

        for obj in world:
            if obj is knight:
                continue
            obj.update(move_x, move_y)
    else:
        for obj in world:
            obj.update()


def render_world():
    clear_canvas()
    for object in world:
        object.draw()
    update_canvas()


open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
reset_world()
while running:
    handle_event()
    update_world()
    render_world()
    delay(0.05)