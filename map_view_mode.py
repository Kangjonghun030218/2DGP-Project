from pico2d import *
from base_state import BaseState
import state_machine
import game_framework
import server
import config
import menu_mode
from monster import Monster


class MapViewState(BaseState):
    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_3:
                state_machine.pop()
            elif event.key == SDLK_0:
                state_machine.change(menu_mode.MenuState())
            elif event.key == SDLK_ESCAPE:
                game_framework.quit()

    def update(self, frame_time):
        pass

    def draw(self):
        if server.game_map:
            server.game_map.image.draw(config.CANVAS_WIDTH // 2, config.CANVAS_HEIGHT // 2, config.CANVAS_WIDTH,
                                       config.CANVAS_HEIGHT)

            for obj in server.world:
                if isinstance(obj, Monster) and obj.current_hp > 0:
                    mx = (obj.world_x1 / server.game_map.width) * config.CANVAS_WIDTH
                    my = (obj.world_y1 / server.game_map.height) * config.CANVAS_HEIGHT
                    obj.images['idle'].clip_draw(0, 192, 64, 64, mx, my, 50, 50)
            if server.knight:
                screen_x = (server.knight.world_x / server.game_map.width) * config.CANVAS_WIDTH
                screen_y = (server.knight.world_y / server.game_map.height) * config.CANVAS_HEIGHT
                clip_y_down = 192

                if server.knight.current_images:
                    server.knight.current_images['idle'].clip_draw(0, clip_y_down, 64, 64, screen_x, screen_y, 100, 100)