from pico2d import *
import random

class village:
    def __int__(self):
        self.image=load_image('map_1.png')

    def draw(self):
        self.image.draw(400,300)



running=True




def handle_event():
    global running
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            running=False
        elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            running=False



def reset_world():
    global world
    world=[]
    map_1=village()
    world.append(map_1)

def update_world():
    pass


def render_world():
    pass

open_canvas()
reset_world()
while running:
    handle_event()
    reset_world()
    update_world()
    render_world()

