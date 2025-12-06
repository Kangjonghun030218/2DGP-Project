from pico2d import *
from base_state import BaseState
import state_machine
import game_framework
import server
import config
import menu_mode
from monster import Monster
from portal import Portal
from boss import Boss
from npc import NPC
from princess import Princess
from potion import Potion


class MapViewState(BaseState):
    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_m:
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

                elif isinstance(obj, Portal):
                    mx = (obj.x / server.game_map.width) * config.CANVAS_WIDTH
                    my = (obj.y / server.game_map.height) * config.CANVAS_HEIGHT
                    if obj.image:
                        obj.image.draw(mx, my, 40, 40)

                elif isinstance(obj, Boss) and obj.current_hp > 0:
                    mx = (obj.x / server.game_map.width) * config.CANVAS_WIDTH
                    my = (obj.y / server.game_map.height) * config.CANVAS_HEIGHT
                    if obj.body_image:
                        obj.body_image.draw(mx, my, 100, 100)

                elif isinstance(obj, NPC):
                    mx1 = (obj.world_x1 / server.game_map.width) * config.CANVAS_WIDTH
                    my1 = (obj.world_y1 / server.game_map.height) * config.CANVAS_HEIGHT
                    obj.image1.clip_draw(0, 0, 48, 48, mx1, my1, 40, 40)

                    mx2 = (obj.world_x2 / server.game_map.width) * config.CANVAS_WIDTH
                    my2 = (obj.world_y2 / server.game_map.height) * config.CANVAS_HEIGHT
                    obj.image2.clip_draw(0, 0, 48, 48, mx2, my2, 40, 40)

                    mx3 = (obj.world_x3 / server.game_map.width) * config.CANVAS_WIDTH
                    my3 = (obj.world_y3 / server.game_map.height) * config.CANVAS_HEIGHT
                    obj.image3.clip_draw(0, 0, 48, 48, mx3, my3, 40, 40)

                    mx4 = (obj.world_x4 / server.game_map.width) * config.CANVAS_WIDTH
                    my4 = (obj.world_y4 / server.game_map.height) * config.CANVAS_HEIGHT
                    obj.image4.clip_draw(0, 0, 48, 48, mx4, my4, 40, 40)

                elif isinstance(obj, Princess):
                    mx = (obj.x / server.game_map.width) * config.CANVAS_WIDTH
                    my = (obj.y / server.game_map.height) * config.CANVAS_HEIGHT

                    if obj.image:
                        clip_y = 0 if obj.is_freed else obj.frame_height

                        obj.image.clip_draw(
                            0, clip_y,
                            obj.frame_width, obj.frame_height,
                            mx, my, 50, 50
                        )

                elif isinstance(obj, Potion):
                    mx = (obj.world_x / server.game_map.width) * config.CANVAS_WIDTH
                    my = (obj.world_y / server.game_map.height) * config.CANVAS_HEIGHT

                    if obj.image:
                        obj.image.draw(mx, my, 20, 20)

            if server.knight:
                screen_x = (server.knight.world_x / server.game_map.width) * config.CANVAS_WIDTH
                screen_y = (server.knight.world_y / server.game_map.height) * config.CANVAS_HEIGHT
                clip_y_down = 192

                if server.knight.current_images:
                    server.knight.current_images['idle'].clip_draw(0, clip_y_down, 64, 64, screen_x, screen_y, 100, 100)