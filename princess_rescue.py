from pico2d import *
import random

class village:
    def __int__(self):
        self.image=load_image('map_1.png')

    def draw(self):
        self.image.draw(400,300)



running=True




def handle_event():
    pass


def reset_world():
    pass


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

