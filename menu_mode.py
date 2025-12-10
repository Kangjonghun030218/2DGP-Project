from pico2d import *
from base_state import BaseState
import game_framework
import state_machine
import play_mode
import resource_manager
from ui import StartButton
import config

class MenuState(BaseState):
    def enter(self):
        self.menu_image = resource_manager.get_image('map_0')
        self.start_button = StartButton(config.CANVAS_WIDTH // 2+800, 500)
        self.bgm = resource_manager.get_music('menu_bgm')
        if self.bgm:
            self.bgm.repeat_play()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
        if self.start_button.handle_event(event):
            state_machine.change(play_mode.PlayState())

    def draw(self):
        if self.menu_image:
            self.menu_image.draw(get_canvas_width() // 2, get_canvas_height() // 2, get_canvas_width(), get_canvas_height())
            self.start_button.draw()

    def exit(self):
        if self.bgm:
            self.bgm.stop()