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
        self.font = load_font('resource/malgunbd.ttf', 30)
        self.bgm = None

    def enter(self):
        print("--- GAME CLEAR ---")
        self.bgm = resource_manager.get_music('clear_bgm')
        if self.bgm:
            self.bgm.repeat_play()

    def exit(self):
        if self.bgm:
            self.bgm.stop()

    def update(self, frame_time):
        pass

    def draw(self):
        if self.bg_image:
            self.bg_image.draw(config.CANVAS_WIDTH // 2, config.CANVAS_HEIGHT // 2,
                               config.CANVAS_WIDTH, config.CANVAS_HEIGHT)

        if self.font:
            self.font.draw(config.CANVAS_WIDTH // 2 - 300, 800,
                           "아무 키를 입력하여 게임 종료!!! 고생하셨습니다.", (255, 0, 0))

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            game_framework.quit()