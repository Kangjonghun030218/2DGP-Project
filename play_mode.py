from pico2d import *
from base_state import BaseState
from game_map import GameMap
from knight import Knight, check_collision
from npc import NPC
from monster import Monster
from projectile import Projectile
from ui import draw_ui
from potion import Potion
import random

import server
import config
import state_machine
import game_framework

import menu_mode
import map_view_mode
import dialogue_mode

PICKUP_RANGE = 50


class PlayState(BaseState):
    def __init__(self):
        self.start_map_number = 1

    def enter(self):
        if server.knight is None:
            server.knight = Knight()

        self.reset_world(self.start_map_number)

    def exit(self):
        pass

    def reset_world(self, map_number=1):
        server.cam_x, server.cam_y = 0, 0
        server.world = []
        server.game_map = GameMap(map_number)
        server.world.append(server.game_map)

        if map_number == 1:
            server.knight.world_x = 1000
            server.knight.world_y = 300
            npc = NPC()
            server.world.append(npc)
        elif map_number == 2:
            server.knight.world_x = 800
            server.knight.world_y = 500
            monster_spawn_zones = [
                ((700, 2150, 1000, 2350), 1, 10),
                ((2100, 1600, 2800, 1900), 2, 10),
                ((3320, 2350, 3700, 2450), 3, 10),
                ((3950, 1220, 4100, 1500), 4, 5),
                ((4000, 1800, 4100, 2000), 4, 5),
                ((600, 1250, 1000, 1500), 5, 10),
                ((1350, 1050, 1700, 1200), 6, 10)
            ]
            for zone, m_type, count in monster_spawn_zones:
                x_min, y_min, x_max, y_max = zone
                for _ in range(count):
                    x = random.randint(x_min, x_max)
                    y = random.randint(y_min, y_max)
                    server.world.append(Monster(x, y, m_type))
        elif map_number == 3:
            server.knight.world_x = 1200
            server.knight.world_y = 300
            monster_spawn_zones = [
                ((300, 600, 2400, 1200), 5, 5),
                ((300, 800, 2400, 1400), 6, 5),
                ((400, 1800, 2400, 2200), 1, 5),
                ((400, 2200, 2400, 2600), 4, 5),
                ((500, 3200, 2400, 3800), 3, 5),
                ((600, 3800, 2400, 4100), 2, 5),
            ]
            for zone, m_type, count in monster_spawn_zones:
                x_min, y_min, x_max, y_max = zone
                for _ in range(count):
                    x = random.randint(x_min, x_max)
                    y = random.randint(y_min, y_max)
                    server.world.append(Monster(x, y, m_type))
        elif map_number == 4:
            server.knight.world_x = 1200
            server.knight.world_y = 300

        if server.knight not in server.world:
            server.world.append(server.knight)

        if server.knight.state == 'dead':
            server.knight.respawn()

    def pickup_item(self):
        if not server.knight:
            return

        potions_in_world = [obj for obj in server.world if isinstance(obj, Potion)]
        if not potions_in_world:
            return

        closest_potion = None
        min_dist_sq = PICKUP_RANGE ** 2

        for potion in potions_in_world:
            dx = potion.world_x - server.knight.world_x
            dy = potion.world_y - server.knight.world_y
            dist_sq = dx ** 2 + dy ** 2

            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_potion = potion

        if closest_potion:
            server.knight.add_potion(closest_potion.potion_type)
            server.world.remove(closest_potion)
            print(f"{closest_potion.potion_type.upper()} 포션을 주웠습니다.")

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_0:
                state_machine.change(menu_mode.MenuState())
            elif event.key == SDLK_1:
                self.reset_world(1)
            elif event.key == SDLK_2:
                self.reset_world(2)
            elif event.key == SDLK_3:
                state_machine.push(map_view_mode.MapViewState())
            elif event.key == SDLK_5:
                if server.knight: server.knight.use_potion('hp')
            elif event.key == SDLK_6:
                if server.knight: server.knight.use_potion('mp')
            elif event.key == SDLK_7:
                if server.knight: server.knight.activate_skill('skill1')
            elif event.key == SDLK_8:
                if server.knight: server.knight.activate_skill('skill2')
            elif event.key == SDLK_9:
                if server.knight: server.knight.activate_skill('skill3')
            elif event.key == SDLK_z:
                self.pickup_item()
            elif event.key == SDLK_p:
                print(f"현재 좌표: {int(server.knight.world_x)}, {int(server.knight.world_y)}")
            elif event.key == SDLK_SPACE:
                for obj in server.world:
                    if isinstance(obj, NPC):
                        if obj.interact(server.knight.world_x, server.knight.world_y):
                            state_machine.push(dialogue_mode.DialogueState())
                            break
            else:
                if server.knight:
                    server.knight.handle_event(event)

        elif event.type == SDL_KEYUP:
            if server.knight:
                server.knight.handle_event(event)

    def update(self, frame_time):
        removed_objects = []
        for obj in server.world:
            if obj is server.knight:
                obj.update(server.game_map, frame_time)
            elif isinstance(obj, Monster):
                if server.knight:
                    obj.update(frame_time, server.game_map, server.knight.world_x, server.knight.world_y)
                else:
                    obj.update(frame_time, server.game_map)
                if obj.is_removable:
                    removed_objects.append(obj)
            elif isinstance(obj, Projectile):
                if obj.update(frame_time):
                    removed_objects.append(obj)
            elif isinstance(obj, NPC):
                obj.update(frame_time)
            else:
                if hasattr(obj, 'update'):
                    obj.update()

        for obj in removed_objects:
            if obj in server.world:
                server.world.remove(obj)
                if isinstance(obj, Monster) and obj.current_hp <= 0:
                    hunt_quest = server.quest_log['monster_hunt']
                    if (hunt_quest['status'] == 'in_progress' and
                            obj.monster_type == hunt_quest['current_target_type']):
                        if hunt_quest['current_kill_count'] < 10:
                            hunt_quest['current_kill_count'] += 1
                    if random.random() < 0.3:
                        potion_type = random.choice(['hp', 'mp'])
                        new_potion = Potion(obj.world_x1, obj.world_y1, potion_type)
                        server.world.append(new_potion)
        self.check_portal()
        if server.knight and server.knight.is_dead_and_animation_finished:
            self.start_map_number = 1
            state_machine.change(PlayState())
            return

        if server.knight:
            hunt_quest = server.quest_log['monster_hunt']
            current_stage = hunt_quest['total_quest_stage']
            if current_stage == 3 and server.knight.level == 1:
                server.knight.upgrade_level()
            elif current_stage == 5 and server.knight.level == 2:
                server.knight.upgrade_level()

        if server.knight and server.game_map:
            target_cam_x = server.knight.world_x - config.CANVAS_WIDTH // 2
            target_cam_y = server.knight.world_y - config.CANVAS_HEIGHT // 2
            min_cam_x = 0
            max_cam_x = server.game_map.width - config.CANVAS_WIDTH
            min_cam_y = 0
            max_cam_y = server.game_map.height - config.CANVAS_HEIGHT
            server.cam_x = max(min_cam_x, min(target_cam_x, max_cam_x))
            server.cam_y = max(min_cam_y, min(target_cam_y, max_cam_y))
            if max_cam_x < 0: server.cam_x = 0
            if max_cam_y < 0: server.cam_y = 0

        if not server.knight or server.knight.state == 'dead':
            return

        monsters_in_world = [obj for obj in server.world if isinstance(obj, Monster)]
        knight_attack_frame = (
                    server.knight.state == 'attack' and (server.knight.frame == 3 or server.knight.frame == 4))

        if knight_attack_frame:
            knight_attack_box = server.knight.get_attack_bb()
            for monster in monsters_in_world:
                if monster.current_hp > 0 and check_collision(knight_attack_box, monster.get_bb()):
                    damage = 100
                    if server.knight.skill_name == 'skill1':
                        damage = 20
                    elif server.knight.skill_name == 'skill2':
                        damage = 30
                    monster.take_damage(damage, server.knight.world_x, server.knight.world_y)

        projectiles_in_world = [obj for obj in server.world if isinstance(obj, Projectile)]
        for obj in projectiles_in_world:
            for monster in monsters_in_world:
                if monster.current_hp > 0 and check_collision(obj.get_bb(), monster.get_bb()):
                    monster.take_damage(15, obj.world_x, obj.world_y)
                    if obj in server.world:
                        server.world.remove(obj)
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
                    dist_x = server.knight.world_x - monster.world_x1
                    dist_y = server.knight.world_y - monster.world_y1
                    distance_sq = dist_x ** 2 + dist_y ** 2
                    if distance_sq < monster.attack_range ** 2:
                        server.knight.take_damage(5, monster.world_x1, monster.world_y1)

    def draw(self):
        for obj in server.world:
            obj.draw(server.cam_x, server.cam_y)
        draw_ui()

    def check_portal(self):
        if server.game_map.map_number == 1:
            if server.knight:
                portal_box = (1230, 180, 1290, 230)
                if check_collision(server.knight.get_bb(), portal_box):
                    self.reset_world(2)
            if server.knight:
                portal_box = (1248, 856, 1332, 912)
                if check_collision(server.knight.get_bb(), portal_box):
                    self.reset_world(3)
        elif server.game_map.map_number == 3:
            if server.knight:
                portal_box = (1245, 4257, 1352, 4329)
                if check_collision(server.knight.get_bb(), portal_box):
                    self.reset_world(4)