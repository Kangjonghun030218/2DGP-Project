from pico2d import *
import random

class Village:
    def __init__(self):
        self.image=load_image('map_1.png')


    def draw(self):
        self.image.draw(400,300)
    def update(self):
        pass
class Knight:
    def __init__(self):
        self.x=400
        self.y=200
        self.image=load_image('Swordsman_lvl1_Idle_with_shadow.png')
        self.frame=0
        self.speed=5
        self.direct = "stop"
        self.face_dirX=1
        self.face_dirY=1

    def draw(self):
        if self.direct=="stop":
            self.image.clip_draw(self.frame*64, 196,64,64,self.x,self.y)

    def update(self):
        self.frame=(self.frame+1)%12
        if self.direct == "left":
            self.x -= self.speed
        elif self.direct == "right":
            self.x += self.speed
        elif self.direct == "up":
            self.y += self.speed
        elif self.direct == "down":
            self.y -= self.speed

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.direct = "left"
            elif event.key == SDLK_RIGHT:
                self.direct = "right"
            elif event.key == SDLK_UP:
                self.direct = "up"
            elif event.key == SDLK_DOWN:
                self.direct = "down"

        elif event.type == SDL_KEYUP:
            if (event.key == SDLK_LEFT and self.direct == "left") or \
                    (event.key == SDLK_RIGHT and self.direct == "right") or \
                    (event.key == SDLK_UP and self.direct == "up") or \
                    (event.key == SDLK_DOWN and self.direct == "down"):
                self.direct = "stop"





running=True




def handle_event():
    global running
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            running=False

        elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            running=False
        else:
            for obj in world:
                if isinstance(obj, Knight):
                    obj.handle_event(event)



def reset_world():
    global world
    world=[]
    map_1=Village()
    knight=Knight()

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

