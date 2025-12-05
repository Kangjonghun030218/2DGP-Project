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
                1: "초록 오크", 2: "파란 오크", 3: "강한 초록 오크",
                4: "초록 슬라임", 5: "파란 슬라임", 6: "불타오르는 슬라임"
            }

            current_stage = hunt_quest['total_quest_stage']
            target_name = monster_names.get(current_stage, f"monster (type {current_stage})")

            if hunt_quest['status'] == 'not_started':
                server.dialogue_message = f"이봐!, {target_name} 10마리 처치를 부탁할게."
                hunt_quest['status'] = 'in_progress'
                hunt_quest['current_target_type'] = 1
                hunt_quest['current_kill_count'] = 0
                hunt_quest['total_quest_stage'] = 1

            elif hunt_quest['status'] == 'in_progress':
                if hunt_quest['current_kill_count'] >= 10:
                    hunt_quest['total_quest_stage'] += 1

                    if hunt_quest['total_quest_stage'] > 6:
                        server.dialogue_message = "고마워 모든 미션을 클리어 해줬어! 이제 길을 떠나도 좋아."
                        hunt_quest['status'] = 'completed'

                        new_portal = Portal(1290, 884, 'map3')
                        server.world.append(new_portal)
                    else:
                        hunt_quest['current_target_type'] = hunt_quest['total_quest_stage']
                        hunt_quest['current_kill_count'] = 0
                        next_target_name = monster_names.get(hunt_quest['current_target_type'], "next monster")
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

    def update(self, frame_time):
        self.frame_timer += frame_time
        if self.frame_timer >= self.animation_speed:
            self.frame_timer -= self.animation_speed
            self.frame = (self.frame + 1) % 4