import server
import resource_manager
import config
from pico2d import get_time
from boss import Boss


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

    bar_max_width = 200
    bar_height = 20
    ui_x = 20
    hp_bar_y = config.CANVAS_HEIGHT - 35
    mp_bar_y = config.CANVAS_HEIGHT - 65

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

    text_x = 20
    if font:
        hp_text = f"HP: {server.knight.current_hp} / {server.knight.max_hp}"
        mp_text = f"MP: {server.knight.current_mp} / {server.knight.max_mp}"

        font.draw(text_x + 6, hp_bar_y + 4, hp_text, (0, 0, 0))
        font.draw(text_x + 6, mp_bar_y + 4, mp_text, (0, 0, 0))
        font.draw(text_x + 5, hp_bar_y + 5, hp_text, (255, 255, 255))
        font.draw(text_x + 5, mp_bar_y + 5, mp_text, (255, 255, 255))

    if not (skill1_img and skill2_img and skill3_img):
        return

    current_time = get_time()
    icon_size = 48
    icon_spacing = 10
    icon_y = 40
    key_text_y = icon_y + icon_size // 2 + 10

    center_x = config.CANVAS_WIDTH // 2
    skill2_x = center_x
    skill1_x = center_x - icon_size - icon_spacing
    skill3_x = center_x + icon_size + icon_spacing
    potion2_x = skill1_x - icon_size - icon_spacing
    potion1_x = potion2_x - icon_size - icon_spacing

    positions = {'skill1': skill1_x, 'skill2': skill2_x, 'skill3': skill3_x}
    images = {'skill1': skill1_img, 'skill2': skill2_img, 'skill3': skill3_img}
    keys = {'skill1': '7', 'skill2': '8', 'skill3': '9'}

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
            key_text_y = icon_y + icon_size // 2 + 10
            font.draw(x - 5, key_text_y, keys[skill_name], (255, 255, 0))

    if hp_potion_img:
        hp_potion_img.draw(potion1_x, icon_y, icon_size, icon_size)
        if font:
            font.draw(potion1_x - 5, key_text_y, '5', (255, 255, 0))
            font.draw(potion1_x + 10, icon_y - 15, f'{server.knight.hp_potions}', (255, 255, 255))

    if mp_potion_img:
        mp_potion_img.draw(potion2_x, icon_y, icon_size, icon_size)
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
        bar_x = config.CANVAS_WIDTH // 2
        bar_y = config.CANVAS_HEIGHT - 40
        bar_w = 800
        bar_h = 30

        if bar_bg:
            bar_bg.draw(bar_x, bar_y, bar_w, bar_h)

        if hp_bar:
            hp_ratio = max(0, boss_obj.current_hp / boss_obj.max_hp)
            current_w = int(bar_w * hp_ratio)

            left_edge = bar_x - (bar_w // 2)
            draw_x = left_edge + (current_w // 2)

            if current_w > 0:
                hp_bar.draw(draw_x, bar_y, current_w, bar_h)

        if font:
            hp_text = f"{int(boss_obj.current_hp)} / {int(boss_obj.max_hp)}"
            font.draw(bar_x - 50, bar_y, hp_text, (255, 255, 255))

            font.draw(bar_x - 25, bar_y + 25, "BOSS", (50, 255, 50))

        base_x = config.CANVAS_WIDTH // 2 + 200
        icon_y = config.CANVAS_HEIGHT - 100
        icon_size = 50
        gap = 60

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
