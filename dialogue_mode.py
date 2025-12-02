from pico2d import *
from base_state import BaseState
import state_machine
import game_framework
import server
import resource_manager
import config
from ui import UI_SCALE


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
        bg_w = int(bg_image.w * UI_SCALE)
        bg_h = int(bg_image.h * UI_SCALE)
        bg_x = config.CANVAS_WIDTH // 2
        bg_y = int(config.CANVAS_HEIGHT * 0.3)

        bg_image.draw(bg_x, bg_y, bg_w, bg_h)
        image_left_edge = bg_x - (bg_w // 2)

        padding_x = int(60 * UI_SCALE)
        padding_y = int(5 * UI_SCALE)

        text_x = image_left_edge + padding_x
        text_y = bg_y + padding_y
        font.draw(text_x, text_y, server.dialogue_message, (0, 0, 0))