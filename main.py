from pico2d import open_canvas, close_canvas
import game_framework
import resource_manager
import menu_mode
import config

open_canvas(config.CANVAS_WIDTH, config.CANVAS_HEIGHT)

resource_manager.load_all()

game_framework.run(menu_mode.MenuState())

close_canvas()