CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800


cam_x, cam_y = 0, 0
game_mode = 'menu'
running = True


knight = None
game_map = None
world = []

font = None
dialogue_message = None

quest_log = {
    'check_npc': {
        'status': 'not_started',
        'talked_to_man': False
    }
}

menu_image = None
bar_bg_image = None
hp_bar_image = None
mp_bar_image = None
skill1_image = None
skill2_image = None
skill3_image = None

effect_image_R1 = None
effect_image_R2 = None
effect_image_U1 = None
effect_image_U2 = None
effect_image1_R1 = None
effect_image1_U1 = None

projectile_image_LR = None
projectile_image_UD = None
