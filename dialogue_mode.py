from pico2d import *
from base_state import BaseState
import state_machine
import game_framework
import server
import resource_manager
import config
from ui import draw_ui


class DialogueState(BaseState):
    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                server.dialogue_message = None
                state_machine.pop()
            elif event.key == SDLK_ESCAPE:
                game_framework.quit()

    def update(self, frame_time):
        pass

    def draw(self):
        bg_image = resource_manager.get_image('dialogue_bg')
        font = resource_manager.get_font()
        if bg_image is None or font is None or not server.dialogue_message:
            return
        bg_x = config.CANVAS_WIDTH // 2
        bg_y = 800
        bg_image.draw(bg_x, bg_y)
        image_left_edge = bg_x - (bg_image.w // 2)
        padding_x = 60
        padding_y = 5
        text_x = image_left_edge + padding_x
        text_y = bg_y + padding_y
        font.draw(text_x, text_y, server.dialogue_message, (0, 0, 0))