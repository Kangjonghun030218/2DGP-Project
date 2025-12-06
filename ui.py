import server
import resource_manager
import config
from pico2d import get_time
from pico2d import *

BASE_RES_WIDTH = 2560


UI_SCALE = config.CANVAS_WIDTH / BASE_RES_WIDTH
UI_SCALE = max(0.8, min(UI_SCALE, 1.5))

MINIMAP_SIZE = int(200 * UI_SCALE)
MINIMAP_RANGE = 1200
MINIMAP_MARGIN = int(20 * UI_SCALE)
MINIMAP_ALPHA = 0.5

big_font = None


def draw_map_message():
    global big_font

    if not hasattr(server, 'map_message') or not server.map_message:
        return

    current_time = get_time()
    elapsed_time = current_time - server.map_message_start_time

    wait_time = 2.0
    fade_time = 2.0
    total_duration = wait_time + fade_time

    if elapsed_time > total_duration:
        server.map_message = None
        return

    big_font = load_font('resource/malgunbd.ttf', 60)

    if elapsed_time < wait_time:
        intensity = 255
    else:
        progress = (elapsed_time - wait_time) / fade_time
        intensity = int(255 * (1 - progress))
        if intensity < 0: intensity = 0

    text = server.map_message

    text_width_estimate = len(text) * 40
    x = (config.CANVAS_WIDTH - text_width_estimate) // 2
    y = config.CANVAS_HEIGHT - 200

    big_font.draw(x, y, text, (intensity, 0, 0))

def draw_mini_map():
    if not server.knight or not server.game_map:
        return

    mm_x1 = config.CANVAS_WIDTH - MINIMAP_SIZE - MINIMAP_MARGIN
    mm_y1 = config.CANVAS_HEIGHT - MINIMAP_SIZE - MINIMAP_MARGIN
    mm_x2 = config.CANVAS_WIDTH - MINIMAP_MARGIN
    mm_y2 = config.CANVAS_HEIGHT - MINIMAP_MARGIN

    view_left = server.knight.world_x - MINIMAP_RANGE // 2
    view_bottom = server.knight.world_y - MINIMAP_RANGE // 2

    max_left = max(0, server.game_map.width - MINIMAP_RANGE)
    max_bottom = max(0, server.game_map.height - MINIMAP_RANGE)

    view_left = max(0, min(view_left, max_left))
    view_bottom = max(0, min(view_bottom, max_bottom))

    scale = MINIMAP_SIZE / MINIMAP_RANGE

    draw_rectangle(mm_x1, mm_y1, mm_x2, mm_y2)

    if server.game_map.image:
        server.game_map.image.clip_draw_to_origin(
            int(view_left), int(view_bottom),
            MINIMAP_RANGE, MINIMAP_RANGE,
            mm_x1, mm_y1,
            MINIMAP_SIZE, MINIMAP_SIZE
        )

    draw_rectangle(mm_x1, mm_y1, mm_x2, mm_y2)

    from monster import Monster
    from npc import NPC
    from portal import Portal
    from boss import Boss
    from princess import Princess
    from potion import Potion

    icon_scale = UI_SCALE

    for obj in server.world:
        ox, oy = 0, 0
        if hasattr(obj, 'world_x'):
            ox, oy = obj.world_x, obj.world_y
        elif hasattr(obj, 'world_x1'):
            ox, oy = obj.world_x1, obj.world_y1
        elif hasattr(obj, 'x'):
            ox, oy = obj.x, obj.y
        else:
            continue

        draw_x = mm_x1 + (ox - view_left) * scale
        draw_y = mm_y1 + (oy - view_bottom) * scale

        if not (mm_x1 <= draw_x <= mm_x2 and mm_y1 <= draw_y <= mm_y2):
            continue

        if obj is server.knight:
            continue

        elif isinstance(obj, Monster) and obj.current_hp > 0:
            if obj.images and 'idle' in obj.images:
                # 30 -> 30 * icon_scale
                s = 30 * icon_scale
                obj.images['idle'].clip_draw(0, 192, 64, 64, draw_x, draw_y, s, s)

        elif isinstance(obj, NPC):
            if hasattr(obj, 'image1'):
                s = 8 * icon_scale
                obj.image1.clip_draw(0, 0, 48, 48, draw_x, draw_y, s, s)
                coords = [(obj.world_x2, obj.world_y2), (obj.world_x3, obj.world_y3), (obj.world_x4, obj.world_y4)]
                imgs = [obj.image2, obj.image3, obj.image4]
                for (nx, ny), nimg in zip(coords, imgs):
                    ndx = mm_x1 + (nx - view_left) * scale
                    ndy = mm_y1 + (ny - view_bottom) * scale
                    if mm_x1 <= ndx <= mm_x2 and mm_y1 <= ndy <= mm_y2:
                        nimg.clip_draw(0, 0, 48, 48, ndx, ndy, s, s)

        elif isinstance(obj, Boss) and obj.current_hp > 0:
            if obj.body_image: obj.body_image.draw(draw_x, draw_y, 50 * icon_scale, 50 * icon_scale)
        elif isinstance(obj, Portal):
            if obj.image: obj.image.draw(draw_x, draw_y, 20 * icon_scale, 20 * icon_scale)
        elif isinstance(obj, Princess):
            if obj.image: obj.image.clip_draw(0, 0, obj.frame_width, obj.frame_height, draw_x, draw_y, 20 * icon_scale,
                                              20 * icon_scale)
        elif isinstance(obj, Potion):
            if obj.image: obj.image.draw(draw_x, draw_y, 20 * icon_scale, 20 * icon_scale)

    px = mm_x1 + (server.knight.world_x - view_left) * scale
    py = mm_y1 + (server.knight.world_y - view_bottom) * scale

    if server.knight.current_images:
        server.knight.current_images['idle'].clip_draw(0, 192, 64, 64, px, py, 40 * icon_scale, 40 * icon_scale)


def draw_quest_board():
    if not server.quest_board_active:
        return
    bg_image = resource_manager.get_image('quest_board')
    font = resource_manager.get_font()

    if bg_image is None or font is None:
        return

    minimap_left_x = config.CANVAS_WIDTH - MINIMAP_SIZE - MINIMAP_MARGIN
    gap = int(10 * UI_SCALE)
    bg_w = bg_image.w * UI_SCALE
    bg_h = bg_image.h * UI_SCALE
    board_x = minimap_left_x - gap - (bg_w // 2)
    minimap_center_y = config.CANVAS_HEIGHT - MINIMAP_MARGIN - (MINIMAP_SIZE // 2)
    board_y = minimap_center_y

    if server.game_map and server.game_map.map_number == 3:
        from monster import Monster

        living_monsters = [obj for obj in server.world if isinstance(obj, Monster)]
        count = len(living_monsters)

        bg_image.draw(board_x, board_y, bg_w, bg_h)

        title_text = "적들을 섬멸하라!"
        count_text = f"남은 적: {count}마리"

        title_width_est = len(title_text) * 12 * UI_SCALE
        font.draw(board_x - (title_width_est // 2), board_y + (15 * UI_SCALE), title_text, (0, 0, 0))

        count_width_est = len(count_text) * 10 * UI_SCALE
        font.draw(board_x - (count_width_est // 2), board_y - (15 * UI_SCALE), count_text, (200, 0, 0))

        return
    current_quest = server.quest_log.get('monster_hunt')

    if current_quest and current_quest['status'] == 'in_progress':
        monster_names = {
            1: "초록 오크",
            2: "파란 오크",
            3: "강한 오크",
            4: "초록 슬라임",
            5: "파란 슬라임",
            6: "불타는 슬라임"
        }

        target_id = current_quest.get('current_target_type', 4)
        target_name = monster_names.get(target_id, "알 수 없는 몬스터")

        bg_image.draw(board_x, board_y, bg_w, bg_h)

        title_text = f"{target_name} 사냥"
        count_text = f"{current_quest['current_kill_count']} / 10"

        title_width_est = len(title_text) * 15 * UI_SCALE
        font.draw(board_x - (title_width_est // 2), board_y + (15 * UI_SCALE), title_text, (0, 0, 0))

        count_width_est = len(count_text) * 12 * UI_SCALE
        font.draw(board_x - (count_width_est // 2), board_y - (15 * UI_SCALE), count_text, (200, 0, 0))

def draw_ui():
    font = resource_manager.get_font()
    bar_bg = resource_manager.get_image('bar_bg')
    hp_bar = resource_manager.get_image('bar_hp')
    mp_bar = resource_manager.get_image('bar_mp')
    skill1_img = resource_manager.get_image('skill1')
    skill2_img = resource_manager.get_image('skill2')
    skill3_img = resource_manager.get_image('skill3')
    hp_potion_img = resource_manager.get_image('hp_potion')
    mp_potion_img = resource_manager.get_image('mp_potion')

    if not server.knight or not bar_bg or not hp_bar or not mp_bar:
        if font:
            font.draw(20, config.CANVAS_HEIGHT - 30, "UI Load Error", (255, 0, 0))
        return

    bar_max_width = int(200 * UI_SCALE)
    bar_height = int(20 * UI_SCALE)
    ui_x = int(20 * UI_SCALE)

    hp_bar_y = config.CANVAS_HEIGHT - int(35 * UI_SCALE)
    mp_bar_y = config.CANVAS_HEIGHT - int(65 * UI_SCALE)

    hp_ratio = server.knight.current_hp / server.knight.max_hp
    current_hp_width = int(bar_max_width * hp_ratio)

    bar_bg.draw(ui_x + bar_max_width // 2, hp_bar_y + bar_height // 2, bar_max_width, bar_height)

    if current_hp_width > 0:
        draw_x = ui_x + current_hp_width // 2
        hp_bar.draw(draw_x, hp_bar_y + bar_height // 2, current_hp_width, bar_height)

    mp_ratio = server.knight.current_mp / server.knight.max_mp
    current_mp_width = int(bar_max_width * mp_ratio)
    bar_bg.draw(ui_x + bar_max_width // 2, mp_bar_y + bar_height // 2, bar_max_width, bar_height)

    if current_mp_width > 0:
        draw_x_mp = ui_x + current_mp_width // 2
        mp_bar.draw(draw_x_mp, mp_bar_y + bar_height // 2, current_mp_width, bar_height)

    text_x = int(20 * UI_SCALE)
    if font:
        hp_text = f"HP: {int(server.knight.current_hp)} / {server.knight.max_hp}"
        mp_text = f"MP: {int(server.knight.current_mp)} / {server.knight.max_mp}"

        font.draw(text_x + 6, hp_bar_y + 4, hp_text, (0, 0, 0))
        font.draw(text_x + 6, mp_bar_y + 4, mp_text, (0, 0, 0))
        font.draw(text_x + 5, hp_bar_y + 5, hp_text, (255, 255, 255))
        font.draw(text_x + 5, mp_bar_y + 5, mp_text, (255, 255, 255))

    if not (skill1_img and skill2_img and skill3_img):
        return

    current_time = get_time()
    icon_size = int(48 * UI_SCALE)
    icon_spacing = int(10 * UI_SCALE)
    icon_y = int(40 * UI_SCALE)

    center_x = config.CANVAS_WIDTH // 2
    skill2_x = center_x
    skill1_x = center_x - icon_size - icon_spacing
    skill3_x = center_x + icon_size + icon_spacing
    potion2_x = skill1_x - icon_size - icon_spacing
    potion1_x = potion2_x - icon_size - icon_spacing

    positions = {'skill1': skill1_x, 'skill2': skill2_x, 'skill3': skill3_x}
    images = {'skill1': skill1_img, 'skill2': skill2_img, 'skill3': skill3_img}
    keys = {'skill1': 's', 'skill2': 'd', 'skill3': 'f'}

    for skill_name in ['skill1', 'skill2', 'skill3']:
        x = positions[skill_name]
        image = images[skill_name]

        cooldown = server.knight.skill_cooldowns[skill_name]
        time_elapsed = current_time - server.knight.skill_last_used[skill_name]

        if time_elapsed < cooldown:
            image.opacify(0.3)
            image.draw(x, icon_y, icon_size, icon_size)
            image.opacify(1.0)

            remaining_time = cooldown - time_elapsed
            if font:
                font.draw(x - 10, icon_y, f"{remaining_time:.1f}", (255, 0, 0))
        else:
            image.draw(x, icon_y, icon_size, icon_size)

        if font:
            key_text_y = icon_y + icon_size // 2 + int(10 * UI_SCALE)
            font.draw(x - 5, key_text_y, keys[skill_name], (255, 255, 0))

    if hp_potion_img:
        hp_potion_img.draw(potion1_x, icon_y, icon_size, icon_size)
        key_text_y = icon_y + icon_size // 2 + int(10 * UI_SCALE)
        if font:
            font.draw(potion1_x - 5, key_text_y, '5', (255, 255, 0))
            font.draw(potion1_x + 10, icon_y - 15, f'{server.knight.hp_potions}', (255, 255, 255))

    if mp_potion_img:
        mp_potion_img.draw(potion2_x, icon_y, icon_size, icon_size)
        key_text_y = icon_y + icon_size // 2 + int(10 * UI_SCALE)
        if font:
            font.draw(potion2_x - 5, key_text_y, '6', (255, 255, 0))
            font.draw(potion2_x + 10, icon_y - 15, f'{server.knight.mp_potions}', (255, 255, 255))

    boss_obj = None
    for obj in server.world:
        from boss import Boss
        if isinstance(obj, Boss):
            boss_obj = obj
            break

    if boss_obj and boss_obj.current_hp > 0:
        bar_w = int(800 * UI_SCALE)
        bar_h = int(30 * UI_SCALE)
        bar_x = config.CANVAS_WIDTH // 2
        bar_y = config.CANVAS_HEIGHT - int(40 * UI_SCALE)

        if bar_bg:
            bar_bg.draw(bar_x, bar_y, bar_w, bar_h)

        if hp_bar:
            hp_ratio = max(0, boss_obj.current_hp / boss_obj.max_hp)
            current_w = int(bar_w * hp_ratio)
            if current_w > 0:
                hp_bar.draw(bar_x - (bar_w - current_w) // 2, bar_y, current_w, bar_h)

        if font:
            hp_text = f"{int(boss_obj.current_hp)} / {int(boss_obj.max_hp)}"
            font.draw(bar_x - int(50 * UI_SCALE), bar_y, hp_text, (255, 255, 255))
            font.draw(bar_x - int(25 * UI_SCALE), bar_y + int(25 * UI_SCALE), "BOSS", (50, 255, 50))

        base_x = config.CANVAS_WIDTH // 2 + int(200 * UI_SCALE)
        icon_y = config.CANVAS_HEIGHT - int(100 * UI_SCALE)
        icon_size = int(50 * UI_SCALE)
        gap = int(60 * UI_SCALE)

        icon1 = resource_manager.get_image('boss_skill_icon')
        if icon1:
            if boss_obj.skill1_cd > 0:
                icon1.opacify(0.4)
                icon1.draw(base_x, icon_y, icon_size, icon_size)
                icon1.opacify(1.0)
                if font: font.draw(base_x - 15, icon_y, f"{boss_obj.skill1_cd:.1f}", (255, 50, 50))
            else:
                icon1.draw(base_x, icon_y, icon_size, icon_size)

        icon2 = resource_manager.get_image('boss_skill2_icon')
        if icon2:
            x2 = base_x + gap
            if boss_obj.skill2_cd > 0:
                icon2.opacify(0.4)
                icon2.draw(x2, icon_y, icon_size, icon_size)
                icon2.opacify(1.0)
                if font: font.draw(x2 - 15, icon_y, f"{boss_obj.skill2_cd:.1f}", (255, 50, 50))
            else:
                icon2.draw(x2, icon_y, icon_size, icon_size)

        icon3 = resource_manager.get_image('boss_skill3_icon')
        if icon3:
            x3 = base_x + gap * 2
            if boss_obj.skill3_cd > 0:
                icon3.opacify(0.4)
                icon3.draw(x3, icon_y, icon_size, icon_size)
                icon3.opacify(1.0)
                if font:
                    font.draw(x3 - 15, icon_y, f"{boss_obj.skill3_cd:.1f}", (255, 50, 50))
            else:
                icon3.draw(x3, icon_y, icon_size, icon_size)

    draw_quest_board()
    draw_mini_map()
    draw_map_message()