knight = None
game_map = None
world = []

quest_log = {
    'check_npc': {
        'status': 'not_started',
        'talked_to_man': False
    },
    'monster_hunt': {
        'status': 'not_started',
        'total_quest_stage': 1,
        'current_target_type': 1,
        'current_kill_count': 0
    }
}
dialogue_message = None
quest_board_active = True
cam_x, cam_y = 0, 0