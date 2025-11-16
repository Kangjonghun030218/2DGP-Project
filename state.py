from pico2d import *
import game_globals as g
from game_map import GameMap
from knight import Knight, check_collision
from npc import NPC
from monster import Monster
from projectile import Projectile
from ui import draw_ui
import random
from potion import Potion

PICKUP_RANGE = 50


class BaseState:
    def enter(self):
        pass

    def exit(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, frame_time):
        pass

    def draw(self):
        pass


class MenuState(BaseState):
    def enter(self):
        if g.menu_image is None:
            g.menu_image = load_image('map_0.png')

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                g.running = False
            else:
                g.states['play'].reset_world(1)
                g.change_state(g.states['play'])

    def draw(self):
        clear_canvas()
        if g.menu_image:
            g.menu_image.draw(g.CANVAS_WIDTH // 2, g.CANVAS_HEIGHT // 2, g.CANVAS_WIDTH, g.CANVAS_HEIGHT)
        update_canvas()


class PlayState(BaseState):

    def reset_world(self, map_number=1):
        g.cam_x, g.cam_y = 0, 0
        g.world = []
        g.game_map = GameMap(map_number)
        g.world.append(g.game_map)

        if map_number == 1:
            npc = NPC()
            g.world.append(npc)
        elif map_number == 2:
            monster_spawn_zones = [
                ((850, 2100, 1200, 2400), 1, 10),
                ((2100, 1600, 2800, 1900), 2, 10),
                ((3300, 2350, 3800, 2500), 3, 10),
                ((3950, 1200, 4100, 1500), 4, 5),
                ((4000, 1800, 4100, 2000), 4, 5),
                ((600, 1250, 1000, 1500), 5, 10),
                ((1400, 1050, 1750, 1200), 6, 10)
            ]
            for zone, m_type, count in monster_spawn_zones:
                x_min, y_min, x_max, y_max = zone
                for _ in range(count):
                    x = random.randint(x_min, x_max)
                    y = random.randint(y_min, y_max)
                    g.world.append(Monster(x, y, m_type))

        if g.knight is None:
            g.knight = Knight()

        if g.knight not in g.world:
            g.world.append(g.knight)

        if g.knight.state == 'dead':
            g.knight.respawn()

    def pickup_item(self):
        if not g.knight:
            return

        potions_in_world = [obj for obj in g.world if isinstance(obj, Potion)]
        if not potions_in_world:
            return

        closest_potion = None
        min_dist_sq = PICKUP_RANGE ** 2

        for potion in potions_in_world:
            dx = potion.world_x - g.knight.world_x
            dy = potion.world_y - g.knight.world_y
            dist_sq = dx ** 2 + dy ** 2

            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_potion = potion

        if closest_potion:
            g.knight.add_potion(closest_potion.potion_type)
            g.world.remove(closest_potion)
            print(f"{closest_potion.potion_type.upper()} 포션을 주웠습니다.")

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                g.running = False
            elif event.key == SDLK_0:
                g.change_state(g.states['menu'])
            elif event.key == SDLK_1:
                self.reset_world(1)
            elif event.key == SDLK_2:
                self.reset_world(2)
            elif event.key == SDLK_3:
                g.change_state(g.states['map_view'])
            elif event.key == SDLK_5:
                if g.knight: g.knight.use_potion('hp')
            elif event.key == SDLK_6:
                if g.knight: g.knight.use_potion('mp')
            elif event.key == SDLK_7:
                if g.knight: g.knight.activate_skill('skill1')
            elif event.key == SDLK_8:
                if g.knight: g.knight.activate_skill('skill2')
            elif event.key == SDLK_9:
                if g.knight: g.knight.activate_skill('skill3')
            elif event.key == SDLK_z:
                self.pickup_item()
            elif event.key == SDLK_SPACE:
                for obj in g.world:
                    if isinstance(obj, NPC):
                        if obj.interact(g.knight.world_x, g.knight.world_y):
                            g.change_state(g.states['dialogue'])
                            break
            else:
                if g.knight:
                    g.knight.handle_event(event)

        elif event.type == SDL_KEYUP:
            if g.knight:
                g.knight.handle_event(event)

    def update(self, frame_time):
        removed_objects = []
        for obj in g.world:
            if obj is g.knight:
                obj.update(g.game_map, frame_time)
            elif isinstance(obj, Monster):
                if g.knight:
                    obj.update(g.knight.world_x, g.knight.world_y)
                else:
                    obj.update()
                if obj.is_removable:
                    removed_objects.append(obj)
            elif isinstance(obj, Projectile):
                if obj.update():
                    removed_objects.append(obj)
            else:
                obj.update()

        for obj in removed_objects:
            if obj in g.world:
                g.world.remove(obj)
                if isinstance(obj, Monster) and obj.current_hp <= 0:
                    hunt_quest = g.quest_log['monster_hunt']
                    if (hunt_quest['status'] == 'in_progress' and
                            obj.monster_type == hunt_quest['current_target_type']):

                        if hunt_quest['current_kill_count'] < 10:
                            hunt_quest['current_kill_count'] += 1
                            print(f"퀘스트 몬스터 처치! 타입: {obj.monster_type}, 현재 카운트: {hunt_quest['current_kill_count']}")
                    if random.random() < 0.3:
                        potion_type = random.choice(['hp', 'mp'])
                        new_potion = Potion(obj.world_x1, obj.world_y1, potion_type)
                        g.world.append(new_potion)
                        print(f"{potion_type.upper()} 포션 드랍!")

        if g.knight and g.knight.is_dead_and_animation_finished:
            print("죽음 애니메이션 완료, 마을로 리스폰합니다.")
            self.reset_world(1)
            return

        if g.knight:
            hunt_quest = g.quest_log['monster_hunt']
            current_stage = hunt_quest['total_quest_stage']
            if current_stage == 3 and g.knight.level == 1:
                g.knight.upgrade_level()
            elif current_stage == 5 and g.knight.level == 2:
                g.knight.upgrade_level()

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

        if not g.knight or g.knight.state == 'dead':
            return

        monsters_in_world = [obj for obj in g.world if isinstance(obj, Monster)]
        knight_attack_frame = (g.knight.state == 'attack' and (g.knight.frame == 3 or g.knight.frame == 4))

        if knight_attack_frame:
            knight_attack_box = g.knight.get_attack_bb()
            for monster in monsters_in_world:
                if monster.current_hp > 0 and check_collision(knight_attack_box, monster.get_bb()):
                    damage = 100
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

    def draw(self):
        clear_canvas()
        for obj in g.world:
            obj.draw(g.cam_x, g.cam_y)
        draw_ui()
        update_canvas()


class MapViewState(BaseState):
    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_3:
                g.change_state(g.states['play'])
            elif event.key == SDLK_0:
                g.change_state(g.states['menu'])
            elif event.key == SDLK_ESCAPE:
                g.running = False

    def update(self, frame_time):
        pass

    def draw(self):
        clear_canvas()
        if g.game_map:
            g.game_map.image.draw(g.CANVAS_WIDTH // 2, g.CANVAS_HEIGHT // 2, g.CANVAS_WIDTH, g.CANVAS_HEIGHT)
            if g.knight:
                screen_x = (g.knight.world_x / g.game_map.width) * g.CANVAS_WIDTH
                screen_y = (g.knight.world_y / g.game_map.height) * g.CANVAS_HEIGHT
                clip_y_down = 192
                g.knight.image.clip_draw(0, clip_y_down, 64, 64, screen_x, screen_y, 100, 100)
        update_canvas()


class DialogueState(BaseState):
    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                g.dialogue_message = None
                g.change_state(g.states['play'])
            elif event.key == SDLK_ESCAPE:
                g.running = False

    def update(self, frame_time):
        pass

    def draw(self):
        clear_canvas()
        for obj in g.world:
            obj.draw(g.cam_x, g.cam_y)

        draw_ui()

        if g.dialogue_message and g.font:
            g.font.draw(101, 101, g.dialogue_message, (0, 0, 0))
            g.font.draw(100, 100, g.dialogue_message, (225, 180, 200))

        update_canvas()