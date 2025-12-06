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
from boss import Boss
from princess import Princess
from portal import Portal
from effect import LevelUpEffect

import server
import config
import state_machine
import game_framework

import menu_mode
import map_view_mode
import dialogue_mode


from portal import Portal
from damage_text import DamageText

PICKUP_RANGE = 50

RESPAWN_TIME = 5.0


class PlayState(BaseState):
    def __init__(self):
        self.start_map_number = 1
        self.respawn_queue = []

    def enter(self):
        if server.knight is None:
            server.knight = Knight()

        self.reset_world(self.start_map_number)

    def exit(self):
        pass

    def reset_world(self, map_number=1):
        self.respawn_queue = []
        server.cam_x, server.cam_y = 0, 0
        server.world = []
        server.game_map = GameMap(map_number)
        server.world.append(server.game_map)

        if map_number == 1:
            server.knight.world_x = 1000
            server.knight.world_y = 300
            portal = Portal(1257, 196, 'normal')
            server.world.append(portal)
            if server.quest_log['monster_hunt']['status'] == 'completed':
                portal_to_3 = Portal(1290, 884, 'map3')
                server.world.append(portal_to_3)
            npc = NPC()
            server.world.append(npc)
        elif map_number == 2:
            server.knight.world_x = 800
            server.knight.world_y = 500

            village_portal = Portal(300, 300, 'village')
            server.world.append(village_portal)

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
            server.map_message = "모든 몬스터들을 물리치세요, 보스 포탈이 열릴 겁니다."
            server.map_message_start_time = get_time()
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
            self.boss = Boss()
            server.world.append(self.boss)

            self.princess = Princess()
            self.princess.x = 1600
            self.princess.y = 600
            server.world.append(self.princess)

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
            elif event.key == SDLK_x:
                self.check_portal()
            elif event.key == SDLK_0:
                state_machine.change(menu_mode.MenuState())
            elif event.key == SDLK_1:
                self.reset_world(1)
            elif event.key == SDLK_2:
                self.reset_world(2)
            elif event.key == SDLK_3:
                state_machine.push(map_view_mode.MapViewState())
            elif event.key == SDLK_4:
                self.reset_world(4)
            elif event.key == SDLK_l:
                self.reset_world(3)
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
            elif event.key == SDLK_t:
                server.quest_board_active = not server.quest_board_active
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
        current_time = get_time()
        for entry in self.respawn_queue[:]:
            monster, respawn_at = entry
            if current_time >= respawn_at:
                monster.respawn()
                server.world.append(monster)
                self.respawn_queue.remove(entry)
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
            elif isinstance(obj, LevelUpEffect):
                obj.update(frame_time)
                if obj.is_finished:
                    removed_objects.append(obj)
            elif isinstance(obj, DamageText):
                obj.update(frame_time)
                if obj.is_finished:
                    removed_objects.append(obj)
            elif isinstance(obj, NPC):
                obj.update(frame_time)
            elif isinstance(obj, Boss):
                if server.knight:
                    obj.update(frame_time, server.game_map, server.knight)
            elif isinstance(obj, Princess):
                obj.update(frame_time)
            elif isinstance(obj, Portal):
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
                    if server.game_map.map_number == 3:
                        remaining_monsters = [m for m in server.world if isinstance(m, Monster)]
                        if not remaining_monsters:
                            print("맵3 클리어! 보스 포탈 생성")
                            boss_portal = Portal(1300, 4273, 'boss')
                            server.world.append(boss_portal)
                    if random.random() < 0.3:
                        potion_type = random.choice(['hp', 'mp'])
                        new_potion = Potion(obj.world_x1, obj.world_y1, potion_type)
                        server.world.append(new_potion)
                if isinstance(obj, Monster):
                    if server.game_map.map_number != 3:
                        self.respawn_queue.append((obj, get_time() + RESPAWN_TIME))
        if server.game_map.map_number == 4:
            if self.boss and self.boss.current_hp <= 0:
                portal_exists = False
                for obj in server.world:
                    if isinstance(obj, Portal) and obj.portal_type == 'boss_clear':
                        portal_exists = True
                        break
                if not portal_exists:
                    print("보스 격파! 클리어 포탈 생성")
                    clear_portal = Portal(1600, 350, 'boss_clear')
                    server.world.append(clear_portal)
        #self.check_portal()
        if server.knight and server.knight.is_dead_and_animation_finished:
            self.start_map_number = 1
            state_machine.change(PlayState())
            return


        if server.knight:
            hunt_quest = server.quest_log['monster_hunt']
            current_stage = hunt_quest['total_quest_stage']
            leveled_up = False
            if current_stage == 3 and server.knight.level == 1:
                server.knight.upgrade_level()
                leveled_up = True
            elif current_stage == 5 and server.knight.level == 2:
                server.knight.upgrade_level()
                leveled_up = True
            if leveled_up:
                effect = LevelUpEffect(server.knight.world_x, server.knight.world_y)
                server.world.append(effect)

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
                if monster in server.knight.hit_list:
                    continue

                if monster.current_hp > 0 and check_collision(knight_attack_box, monster.get_bb()):
                    damage = 0
                    lvl = server.knight.level
                    skill = server.knight.skill_name

                    if skill == 'skill1':
                        if lvl == 1:
                            damage = 50
                        elif lvl == 2:
                            damage = 100
                        elif lvl == 3:
                            damage = 150
                    elif skill == 'skill2':
                        if lvl == 1:
                            damage = 80
                        elif lvl == 2:
                            damage = 150
                        elif lvl == 3:
                            damage = 250
                    else:
                        if lvl == 1:
                            damage = 30
                        elif lvl == 2:
                            damage = 50
                        elif lvl == 3:
                            damage = 80

                    monster.take_damage(damage, server.knight.world_x, server.knight.world_y)
                    server.world.append(DamageText(monster.world_x1, monster.world_y1 + 50, damage))
                    server.knight.hit_list.append(monster)

        projectiles_in_world = [obj for obj in server.world if isinstance(obj, Projectile)]
        for obj in projectiles_in_world:
            for monster in monsters_in_world:
                if monster.current_hp > 0 and check_collision(obj.get_bb(), monster.get_bb()):
                    damage = 0
                    lvl = server.knight.level

                    if lvl == 1:
                        damage = 50
                    elif lvl == 2:
                        damage = 80
                    elif lvl == 3:
                        damage = 120

                    monster.take_damage(damage, obj.world_x, obj.world_y)
                    server.world.append(DamageText(monster.world_x1, monster.world_y1 + 50, damage))
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

        if knight_attack_frame:
                knight_attack_box = server.knight.get_attack_bb()
                for obj in server.world:
                    if isinstance(obj, Boss) and obj.current_hp > 0:
                        if obj in server.knight.hit_list:
                            continue

                        if check_collision(knight_attack_box, obj.get_bb()):
                            damage = 0
                            lvl = server.knight.level
                            skill = server.knight.skill_name

                            if skill == 'skill1':
                                if lvl == 1:
                                    damage = 50
                                elif lvl == 2:
                                    damage = 100
                                elif lvl == 3:
                                    damage = 150
                            elif skill == 'skill2':
                                if lvl == 1:
                                    damage = 80
                                elif lvl == 2:
                                    damage = 150
                                elif lvl == 3:
                                    damage = 250
                            else:
                                if lvl == 1:
                                    damage = 30
                                elif lvl == 2:
                                    damage = 50
                                elif lvl == 3:
                                    damage = 80
                            obj.take_damage(damage)
                            server.world.append(DamageText(obj.x, obj.y + 150, damage))
                            server.knight.hit_list.append(obj)

        for obj in server.world:
            if isinstance(obj, Boss) and obj.current_hp > 0:
                if obj.is_attacking and (0.4 <= obj.attack_timer <= 0.7):
                    if check_collision(server.knight.get_bb(), obj.get_attack_bb()):
                        server.knight.take_damage(20, obj.x, obj.y)

                if obj.skill1_active and not obj.skill1_hit:
                    if 0.4 <= obj.skill1_timer <= 0.6:
                        thunder_bb = obj.get_thunder_bb()
                        if thunder_bb and check_collision(server.knight.get_bb(), thunder_bb):
                            server.knight.take_damage(50, obj.x, obj.y)
                            obj.skill1_hit = True
                if obj.skill2_active and not obj.skill2_hit:
                    if 0.3 <= obj.skill2_timer <= 0.6:
                        claw_bb = obj.get_skill2_bb()
                        if claw_bb and check_collision(server.knight.get_bb(), claw_bb):
                            server.knight.take_damage(30, obj.skill2_pos[0], obj.skill2_pos[1])
                            obj.skill2_hit = True
                if obj.skill3_state == 'firing':
                    laser_bb = obj.get_laser_bb()
                    if laser_bb and check_collision(server.knight.get_bb(), laser_bb):
                        current_time = get_time()
                        if not hasattr(obj, 'laser_hit_timer'):
                            obj.laser_hit_timer = 0
                        if current_time - obj.laser_hit_timer > 0.2:
                            server.knight.take_damage(10, obj.x, obj.y)
                            obj.laser_hit_timer = current_time

    def draw(self):
        for obj in server.world:
            obj.draw(server.cam_x, server.cam_y)
        draw_ui()

    def check_portal(self):
        portals = [obj for obj in server.world if isinstance(obj, Portal)]

        if not portals: return

        knight_bb = server.knight.get_bb()

        for portal in portals:
            if check_collision(knight_bb, portal.get_bb()):
                if portal.portal_type == 'normal' and server.game_map.map_number == 1:
                    self.reset_world(2)
                elif portal.portal_type == 'village' and server.game_map.map_number == 2:
                    self.reset_world(1)
                elif portal.portal_type == 'map3' and server.game_map.map_number == 1:
                    self.reset_world(3)
                elif portal.portal_type == 'boss' and server.game_map.map_number == 3:
                    self.reset_world(4)
                elif portal.portal_type == 'boss_clear':
                    import game_clear_state
                    state_machine.change(game_clear_state.GameClearState())