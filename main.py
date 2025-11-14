from pico2d import *
import game_globals as g
from game_map import GameMap
from knight import Knight, check_collision
from npc import NPC
from monster import Monster
from projectile import Projectile
from ui import draw_ui


def handle_event():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            g.running = False
            return

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                g.running = False
                return

            if g.game_mode == 'menu':
                g.game_mode = 'play'
                reset_world(1)

            elif g.game_mode == 'play':
                if event.key == SDLK_0:
                    g.game_mode = 'menu'
                elif event.key == SDLK_1:
                    reset_world(1)
                elif event.key == SDLK_2:
                    reset_world(2)
                elif event.key == SDLK_3:
                    g.game_mode = 'map_view'
                elif event.key == SDLK_7:
                    if g.knight: g.knight.activate_skill('skill1')
                elif event.key == SDLK_8:
                    if g.knight: g.knight.activate_skill('skill2')
                elif event.key == SDLK_9:
                    if g.knight: g.knight.activate_skill('skill3')

                elif event.key == SDLK_SPACE:
                    for obj in g.world:
                        if isinstance(obj, NPC):
                            if obj.interact(g.knight.world_x, g.knight.world_y):
                                g.game_mode = 'dialogue'
                                break
                else:
                    for obj in g.world:
                        if isinstance(obj, Knight):
                            obj.handle_event(event)

            elif g.game_mode == 'map_view':
                if event.key == SDLK_3:
                    g.game_mode = 'play'
                elif event.key == SDLK_0:
                    g.game_mode = 'menu'

            elif g.game_mode == 'dialogue':
                if event.key == SDLK_SPACE:
                    g.game_mode = 'play'
                    g.dialogue_message = None

        elif event.type == SDL_KEYUP and g.game_mode == 'play':
            for obj in g.world:
                if isinstance(obj, Knight):
                    obj.handle_event(event)


def reset_world(map_number=1):
    g.cam_x, g.cam_y = 0, 0
    g.world = []
    g.game_map = GameMap(map_number)
    g.world.append(g.game_map)

    if map_number == 1:
        npc = NPC()
        g.world.append(npc)
    elif map_number == 2:
        monster = Monster(400, 400, 1)
        monster_1 = Monster(380, 400, 1)
        monster2 = Monster(400, 500, 2)
        monster2_1 = Monster(200, 500, 2)
        monster3 = Monster(400, 600, 3)
        monster3_1 = Monster(100, 600, 3)
        monster4 = Monster(400, 700, 4)
        monster4_1 = Monster(500, 700, 4)
        monster5 = Monster(400, 800, 5)
        monster5_1 = Monster(570, 800, 5)
        monster6 = Monster(400, 900, 6)
        monster6_1 = Monster(600, 900, 6)
        g.world.append(monster)
        g.world.append(monster2)
        g.world.append(monster3)
        g.world.append(monster4)
        g.world.append(monster5)
        g.world.append(monster6)
        g.world.append(monster_1)
        g.world.append(monster2_1)
        g.world.append(monster3_1)
        g.world.append(monster4_1)
        g.world.append(monster5_1)
        g.world.append(monster6_1)

    if g.knight is None:
        g.knight = Knight()
    g.world.append(g.knight)


def update_world():
    if g.game_mode != 'play':
        return

    removed_objects = []
    for obj in g.world:
        if obj is g.knight:
            obj.update(g.game_map)
        elif isinstance(obj, Monster):
            if g.knight:
                obj.update(g.knight.world_x, g.knight.world_y)
            else:
                obj.update()
        elif isinstance(obj, Projectile):
            if obj.update():
                removed_objects.append(obj)
        else:
            obj.update()

    for obj in removed_objects:
        if obj in g.world:
            g.world.remove(obj)


    if g.knight and g.game_map:
        target_cam_x = g.knight.world_x - g.CANVAS_WIDTH // 2
        target_cam_y = g.knight.world_y - g.CANVAS_HEIGHT // 2

        min_cam_x = 0
        max_cam_x = g.game_map.width - g.CANVAS_WIDTH
        min_cam_y = 0
        max_cam_y = g.game_map.height - g.CANVAS_HEIGHT

        g.cam_x = max(min_cam_x, min(target_cam_x, max_cam_x))
        g.cam_y = max(min_cam_y, min(target_cam_y, max_cam_y))

        if max_cam_x < 0: g.cam_x = 0
        if max_cam_y < 0: g.cam_y = 0

    if not g.knight:
        return

    monsters_in_world = [obj for obj in g.world if isinstance(obj, Monster)]
    knight_attack_frame = (g.knight.state == 'attack' and (g.knight.frame == 3 or g.knight.frame == 4))

    if knight_attack_frame:
        knight_attack_box = g.knight.get_attack_bb()
        for monster in monsters_in_world:
            if monster.current_hp > 0 and check_collision(knight_attack_box, monster.get_bb()):
                damage = 10

                if g.knight.skill_name == 'skill1':
                    damage = 20
                elif g.knight.skill_name == 'skill2':
                    damage = 30


                monster.take_damage(damage, g.knight.world_x, g.knight.world_y)

    projectiles_in_world = [obj for obj in g.world if isinstance(obj, Projectile)]

    for obj in projectiles_in_world:
        for monster in monsters_in_world:
            if monster.current_hp > 0 and check_collision(obj.get_bb(), monster.get_bb()):
                monster.take_damage(15, obj.world_x, obj.world_y)

                if obj in g.world:
                    g.world.remove(obj)
                break


    for monster in monsters_in_world:
        if monster.current_hp <= 0: continue

        if monster.state == 'attack':
            damage_frame = False
            if monster.kinMonster == 1 and monster.frame == 4:
                damage_frame = True
            elif monster.kinMonster == 2 and monster.frame == 5:
                damage_frame = True

            if damage_frame:
                dist_x = g.knight.world_x - monster.world_x1
                dist_y = g.knight.world_y - monster.world_y1
                distance_sq = dist_x ** 2 + dist_y ** 2

                if distance_sq < monster.attack_range ** 2:
                    g.knight.take_damage(5, monster.world_x1, monster.world_y1)

def render_world():
    clear_canvas()

    if g.game_mode == 'play':
        for object in g.world:
            object.draw(g.cam_x, g.cam_y)
        draw_ui()

    elif g.game_mode == 'map_view':
        if g.game_map:
            g.game_map.image.draw(g.CANVAS_WIDTH // 2, g.CANVAS_HEIGHT // 2, g.CANVAS_WIDTH, g.CANVAS_HEIGHT)
            if g.knight:
                screen_x = (g.knight.world_x / g.game_map.width) * g.CANVAS_WIDTH
                screen_y = (g.knight.world_y / g.game_map.height) * g.CANVAS_HEIGHT
                clip_y_down = 192
                g.knight.image.clip_draw(0, clip_y_down, 64, 64, screen_x, screen_y, 100, 100)

    elif g.game_mode == 'menu':
        if g.menu_image:
            g.menu_image.draw(g.CANVAS_WIDTH // 2, g.CANVAS_HEIGHT // 2, g.CANVAS_WIDTH, g.CANVAS_HEIGHT)

    elif g.game_mode == 'dialogue':
        for object in g.world:
            object.draw(g.cam_x, g.cam_y)

        if g.dialogue_message and g.font:
            g.font.draw(101, 101, g.dialogue_message, (0, 0, 0))
            g.font.draw(100, 100, g.dialogue_message, (225, 180, 200))

    update_canvas()


open_canvas(g.CANVAS_WIDTH, g.CANVAS_HEIGHT)

g.menu_image = load_image('map_0.png')
g.font = load_font('ARIAL.ttf', 20)

g.bar_bg_image = load_image('bar_bg.png')
g.hp_bar_image = load_image('bar_hp.png')
g.mp_bar_image = load_image('bar_mp.png')

g.skill1_image = load_image('skill1.png')
g.skill2_image = load_image('skill2.png')
g.skill3_image = load_image('skill3.png')

g.effect_image_R1 = load_image('skill2-1_R.png')
g.effect_image_R2 = load_image('skill2-2_R.png')
g.effect_image_U1 = load_image('skill2-1_U.png')
g.effect_image_U2 = load_image('skill2-2_U.png')

g.effect_image1_R1 = load_image('skill1-1_R.png')
g.effect_image1_U1 = load_image('skill1-1_U.png')

g.projectile_image_LR = load_image('projectile_LR.png')
g.projectile_image_UD = load_image('projectile_UD.png')

while g.running:
    handle_event()
    update_world()
    render_world()
    delay(0.03)

close_canvas()