from pico2d import *
from base_state import BaseState
import game_framework
import resource_manager
import config
import state_machine
import menu_mode


class GameClearState(BaseState):
    def __init__(self):
        self.bg_image = resource_manager.get_image('game_clear_screen')
        self.font = resource_manager.get_font()

    def enter(self):
        print("--- GAME CLEAR ---")

    def exit(self):
        pass

    def update(self, frame_time):
        pass

    def draw(self):
        if self.bg_image:
            self.bg_image.draw(config.CANVAS_WIDTH // 2, config.CANVAS_HEIGHT // 2,
                               config.CANVAS_WIDTH, config.CANVAS_HEIGHT)

        if self.font:
            self.font.draw(config.CANVAS_WIDTH // 2 - 100, 100,
                           "Press ESC to Menu", (255, 255, 255))

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                state_machine.change(menu_mode.MenuState())