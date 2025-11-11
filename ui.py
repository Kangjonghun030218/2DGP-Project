from pico2d import *
import game_globals as g

def draw_ui():
    if not g.knight or not g.bar_bg_image or not g.hp_bar_image or not g.mp_bar_image:
        if g.font:
            g.font.draw(20, g.CANVAS_HEIGHT - 30, "UI Image Load Error", (255, 0, 0))
        return

    bar_max_width = 200
    bar_height = 20
    ui_x = 20
    hp_bar_y = g.CANVAS_HEIGHT - 35
    mp_bar_y = g.CANVAS_HEIGHT - 65

    # hp 관련
    hp_ratio = g.knight.current_hp / g.knight.max_hp
    current_hp_width = int(bar_max_width * hp_ratio)
    g.bar_bg_image.draw(ui_x + bar_max_width // 2, hp_bar_y + bar_height // 2, bar_max_width, bar_height)

    if current_hp_width > 0:
        draw_x = ui_x + current_hp_width // 2
        g.hp_bar_image.draw(draw_x, hp_bar_y + bar_height // 2, current_hp_width, bar_height)

    # mp 관련
    mp_ratio = g.knight.current_mp / g.knight.max_mp
    current_mp_width = int(bar_max_width * mp_ratio)
    g.bar_bg_image.draw(ui_x + bar_max_width // 2, mp_bar_y + bar_height // 2, bar_max_width, bar_height)

    if current_mp_width > 0:
        draw_x_mp = ui_x + current_mp_width // 2
        g.mp_bar_image.draw(draw_x_mp, mp_bar_y + bar_height // 2, current_mp_width, bar_height)

    text_x = 20
    if g.font:
        hp_text = f"HP: {g.knight.current_hp} / {g.knight.max_hp}"
        mp_text = f"MP: {g.knight.current_mp} / {g.knight.max_mp}"

        g.font.draw(text_x + 6, hp_bar_y + 4, hp_text, (0, 0, 0))
        g.font.draw(text_x + 6, mp_bar_y + 4, mp_text, (0, 0, 0))
        g.font.draw(text_x + 5, hp_bar_y + 5, hp_text, (255, 255, 255))
        g.font.draw(text_x + 5, mp_bar_y + 5, mp_text, (255, 255, 255))

    if not (g.skill1_image and g.skill2_image and g.skill3_image):
        return

    current_time = get_time()
    icon_size = 48
    icon_spacing = 10
    icon_y = 40

    center_x = g.CANVAS_WIDTH // 2
    skill2_x = center_x
    skill1_x = center_x - icon_size - icon_spacing
    skill3_x = center_x + icon_size + icon_spacing

    positions = {
        'skill1': skill1_x,
        'skill2': skill2_x,
        'skill3': skill3_x
    }
    images = {
        'skill1': g.skill1_image,
        'skill2': g.skill2_image,
        'skill3': g.skill3_image
    }
    keys = {'skill1': '7', 'skill2': '8', 'skill3': '9'}

    for skill_name in ['skill1', 'skill2', 'skill3']:
        x = positions[skill_name]
        image = images[skill_name]

        cooldown = g.knight.skill_cooldowns[skill_name]
        time_elapsed = current_time - g.knight.skill_last_used[skill_name]

        if time_elapsed < cooldown:
            image.opacify(0.3)
            image.draw(x, icon_y, icon_size, icon_size)
            image.opacify(1.0)

            remaining_time = cooldown - time_elapsed
            if g.font:
                g.font.draw(x - 10, icon_y, f"{remaining_time:.1f}", (255, 0, 0))
        else:
            image.draw(x, icon_y, icon_size, icon_size)

        if g.font:
            key_text_y = icon_y + icon_size // 2 + 10
            g.font.draw(x - 5, key_text_y, keys[skill_name], (255, 255, 0))