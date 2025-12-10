import ctypes

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
CANVAS_WIDTH = screen_width
CANVAS_HEIGHT = screen_height
DEBUG_MODE_ON = False