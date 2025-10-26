from pico2d import *
import random


class Village:
    def __init__(self):
        self.image = load_image('map_1.png')

    def draw(self):
        self.image.draw(400, 300)

    def update(self):
        pass


class Knight:
    def __init__(self):
        self.x = 400
        self.y = 200
        self.image = load_image('Swordsman_lvl1_Idle_with_shadow.png')
        self.image2 = load_image('Swordsman_lvl1_Walk_with_shadow.png')
        self.image3 = load_image('Swordsman_lvl1_Run_with_shadow.png')
        self.image4= load_image('Swordsman_lvl1_Attack_with_shadow.png')
        self.frame = 0
        self.speed = 5
        self.state = "idle"
        self.direct = "down"
        self.r_key_pressed = False
        self.a_key_pressed = False


        self.clip_y_table = {
            'down': 192,
            'left': 128,
            'right': 64,
            'up': 0
        }
        self.face_dirX = 1
        self.face_dirY = 1

    def draw(self):
        clip_y = self.clip_y_table[self.direct]
        if self.state == 'idle':
            self.image.clip_draw(self.frame * 64, clip_y, 64, 64, self.x, self.y)
        elif self.state == 'move':
            self.image2.clip_draw(self.frame * 64, clip_y, 64, 64, self.x, self.y)
        elif self.state == 'run':
            self.image3.clip_draw(self.frame * 64, clip_y, 64, 64, self.x, self.y)
        elif self.state=='attack':
            self.image4.clip_draw(self.frame * 64, clip_y, 64, 64, self.x, self.y)

    def update(self):
        if self.direct == 'up' and self.state == 'idle':
            self.frame = (self.frame + 1) % 4
        elif self.state == 'move':
            self.frame = (self.frame + 1) % 6
        elif self.state == 'run':
            self.frame = (self.frame + 1) % 8
        else:
            self.frame = (self.frame + 1) % 12
        if self.state == "move":
            if self.direct == "left":
                self.x -= self.speed
            elif self.direct == "right":
                self.x += self.speed
            elif self.direct == "up":
                self.y += self.speed
            elif self.direct == "down":
                self.y -= self.speed
        if self.state == 'run':
            if self.direct == "left":
                self.x -= self.speed * 2
            elif self.direct == "right":
                self.x += self.speed * 2
            elif self.direct == "up":
                self.y += self.speed * 2
            elif self.direct == "down":
                self.y -= self.speed * 2
        elif self.state=='attack':
            self.frame= (self.frame + 1) % 8

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_r:
                self.r_key_pressed = True
                if self.state == 'move':
                    self.state = 'run'
                    self.frame = 0
            elif event.key == SDLK_a:
                self.a_key_pressed= True
                self.state = 'attack'
                self.frame = 0

            elif self.state!='attack' and event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN):
                if self.state == 'idle':
                    self.frame = 0

                if self.r_key_pressed:
                    self.state = 'run'
                else:
                    self.state = 'move'

                if event.key == SDLK_LEFT:
                    self.direct = "left"
                elif event.key == SDLK_RIGHT:
                    self.direct = "right"
                elif event.key == SDLK_UP:
                    self.direct = "up"
                elif event.key == SDLK_DOWN:
                    self.direct = "down"

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_r:
                self.r_key_pressed = False
                if self.state == 'run':
                    self.state = 'move'
                    self.frame = 0
            elif self.state != 'attack' and event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN):
                self.state = "idle"
                self.frame = 0


running = True


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

    world.append(map_1)
    world.append(knight)


def update_world():
    for object in world:
        object.update()


def render_world():
    clear_canvas()
    for object in world:
        object.draw()
    update_canvas()


open_canvas()
reset_world()
while running:
    handle_event()
    update_world()
    render_world()
    delay(0.1)

