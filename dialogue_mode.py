from pico2d import *
from base_state import BaseState
import state_machine
import game_framework
import server
import resource_manager
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
        if server.dialogue_message:
            font = resource_manager.get_font()
            font.draw(101, 101, server.dialogue_message, (0, 0, 0))
            font.draw(100, 100, server.dialogue_message, (225, 180, 200))