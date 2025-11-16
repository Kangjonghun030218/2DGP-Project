from pico2d import *
from base_state import BaseState
import game_framework
import state_machine
import play_mode
import resource_manager

class MenuState(BaseState):
    def enter(self):
        self.menu_image = resource_manager.get_image('map_0')

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            else:
                state_machine.change(play_mode.PlayState())

    def draw(self):
        if self.menu_image:
            self.menu_image.draw(get_canvas_width() // 2, get_canvas_height() // 2, get_canvas_width(), get_canvas_height())