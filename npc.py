from pico2d import *
import math
import server
import resource_manager
from portal import Portal

class NPC:
    def __init__(self):
        self.image1 = resource_manager.get_image('npc_old_woman')
        self.image2 = resource_manager.get_image('npc_old_man')
        self.image3 = resource_manager.get_image('npc_man')
        self.image4 = resource_manager.get_image('npc_boy')
        self.icon_start = resource_manager.get_image('quest_start')
        self.icon_ing = resource_manager.get_image('quest_ing')
        self.icon_end = resource_manager.get_image('quest_end')
        self.frame = 0

        self.world_x1, self.world_y1 = 1540, 480
        self.world_x2, self.world_y2 = 50 + 600, 230 + 150
        self.world_x3, self.world_y3 = 1040, 800
        self.world_x4, self.world_y4 = 1120, 470

        self.talk_range = 50

        self.frame_timer = 0.0
        self.animation_speed = 0.2

    def interact(self, knight_x, knight_y):
        dist_to_1 = math.sqrt((self.world_x1 - knight_x) ** 2 + (self.world_y1 - knight_y) ** 2)
        dist_to_2 = math.sqrt((self.world_x2 - knight_x) ** 2 + (self.world_y2 - knight_y) ** 2)
        dist_to_3 = math.sqrt((self.world_x3 - knight_x) ** 2 + (self.world_y3 - knight_y) ** 2)

        hunt_quest = server.quest_log['monster_hunt']

        if dist_to_1 < self.talk_range:
            server.dialogue_message = "안녕하세요? 날씨가 참 좋네요. 조심해서 다니세요."
            return True
        elif dist_to_2 < self.talk_range:
            server.dialogue_message = "허허, 젊은이 반갑구만. 마을 밖은 위험하다네."
            return True
        elif dist_to_3 < self.talk_range:
            monster_names = {
                1: "초록 오크", 2: "파란 오크", 3: "강한 오크",
                4: "초록 슬라임", 5: "파란 슬라임", 6: "불타는 슬라임"
            }

            quest_order = [4, 5, 6, 1, 2, 3]

            current_stage = hunt_quest['total_quest_stage']

            if hunt_quest['status'] == 'not_started':
                current_target_id = quest_order[0]
            else:
                current_target_id = hunt_quest.get('current_target_type', quest_order[0])
            target_name = monster_names.get(current_target_id, "알 수 없는 몬스터")

            if hunt_quest['status'] == 'not_started':
                server.dialogue_message = f"이봐!, {target_name} 10마리 처치를 부탁할게."
                hunt_quest['status'] = 'in_progress'
                hunt_quest['current_target_type'] = quest_order[0]
                hunt_quest['current_kill_count'] = 0
                hunt_quest['total_quest_stage'] = 1

            elif hunt_quest['status'] == 'in_progress':
                if hunt_quest['current_kill_count'] >= 10:
                    hunt_quest['total_quest_stage'] += 1

                    if hunt_quest['total_quest_stage'] > len(quest_order):
                        server.dialogue_message = "고마워 모든 미션을 클리어 해줬어! 이제 길을 떠나도 좋아."
                        hunt_quest['status'] = 'completed'
                        new_portal = Portal(1290, 884, 'map3')
                        server.world.append(new_portal)
                        hunt_quest['reward_claimed'] = True
                    else:
                        next_type_id = quest_order[hunt_quest['total_quest_stage'] - 1]
                        hunt_quest['current_target_type'] = next_type_id
                        hunt_quest['current_kill_count'] = 0

                        next_target_name = monster_names.get(next_type_id, "다음 몬스터")
                        server.dialogue_message = f"고마워! 다음은 {next_target_name} 10마리를 처치해줘."

                else:
                    remaining = 10 - hunt_quest['current_kill_count']
                    server.dialogue_message = f"이봐 아직 {target_name} {remaining}마리를 더 퇴치해야하네."

            elif hunt_quest['status'] == 'completed':
                server.dialogue_message = "고맙네 자네덕에 평화가 찾아왔어."

            return True
        return False

    def draw(self, cam_x, cam_y):
        screen_x1 = self.world_x1 - cam_x
        screen_y1 = self.world_y1 - cam_y
        screen_x2 = self.world_x2 - cam_x
        screen_y2 = self.world_y2 - cam_y
        screen_x3 = self.world_x3 - cam_x
        screen_y3 = self.world_y3 - cam_y
        screen_x4 = self.world_x4 - cam_x
        screen_y4 = self.world_y4 - cam_y

        self.image1.clip_draw(self.frame * 48, 0, 48, 48, screen_x1, screen_y1)
        self.image2.clip_draw(self.frame * 48, 0, 48, 48, screen_x2, screen_y2)
        self.image3.clip_draw(self.frame * 48, 0, 48, 48, screen_x3, screen_y3)
        self.image4.clip_draw(self.frame * 48, 0, 48, 48, screen_x4, screen_y4)

        hunt_quest = server.quest_log['monster_hunt']
        q_status = hunt_quest['status']
        kill_count = hunt_quest['current_kill_count']
        current_icon = None

        if q_status == 'not_started':
            current_icon = self.icon_start
        elif q_status == 'in_progress':
            if kill_count < 10:
                current_icon = self.icon_ing
            else:
                current_icon = self.icon_end

        if current_icon:
            floating_y = math.sin(get_time() * 5.0) * 5
            icon_x = screen_x3
            icon_y = screen_y3 + 50 + floating_y
            current_icon.draw(icon_x, icon_y, 40, 40)

    def update(self, frame_time):
        self.frame_timer += frame_time
        if self.frame_timer >= self.animation_speed:
            self.frame_timer -= self.animation_speed
            self.frame = (self.frame + 1) % 4