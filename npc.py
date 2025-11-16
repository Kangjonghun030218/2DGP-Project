from pico2d import *
import math
import server
import resource_manager

class NPC:
    def __init__(self):
        self.image1 = resource_manager.get_image('npc_old_woman')
        self.image2 = resource_manager.get_image('npc_old_man')
        self.image3 = resource_manager.get_image('npc_man')
        self.image4 = resource_manager.get_image('npc_boy')
        self.frame = 0

        self.world_x1, self.world_y1 = 550 + 600, 200 + 200
        self.world_x2, self.world_y2 = 50 + 600, 230 + 150
        self.world_x3, self.world_y3 = 150 + 600, 400 + 200
        self.world_x4, self.world_y4 = 300 + 550, 100 + 250

        self.talk_range = 50

        self.frame_timer = 0.0
        self.animation_speed = 0.2

    def interact(self, knight_x, knight_y):
        dist_to_1 = math.sqrt((self.world_x1 - knight_x) ** 2 + (self.world_y1 - knight_y) ** 2)
        dist_to_2 = math.sqrt((self.world_x2 - knight_x) ** 2 + (self.world_y2 - knight_y) ** 2)
        dist_to_3 = math.sqrt((self.world_x3 - knight_x) ** 2 + (self.world_y3 - knight_y) ** 2)

        check_quest = server.quest_log['check_npc']
        hunt_quest = server.quest_log['monster_hunt']

        if dist_to_1 < self.talk_range:
            if check_quest['status'] == 'not_started':
                server.dialogue_message = "hello?"
                check_quest['status'] = 'in_progress'
            elif check_quest['status'] == 'in_progress':
                if check_quest['talked_to_man']:
                    server.dialogue_message = "hi!"
                    check_quest['status'] = 'completed'
                else:
                    server.dialogue_message = "nice to meet you"
            elif check_quest['status'] == 'completed':
                server.dialogue_message = "thank you."
            return True

        elif dist_to_2 < self.talk_range:
            if check_quest['status'] == 'not_started':
                server.dialogue_message = "hello2"
            elif check_quest['status'] == 'in_progress':
                server.dialogue_message = "hi2"
                check_quest['talked_to_man'] = True
            elif check_quest['status'] == 'completed':
                server.dialogue_message = "thank you2."
            return True

        elif dist_to_3 < self.talk_range:
            monster_names = {
                1: "green ork", 2: "blue orc", 3: "green strong orc",
                4: "Green Slime", 5: "Blue Slime", 6: "Red Slime"
            }

            current_stage = hunt_quest['total_quest_stage']
            target_name = monster_names.get(current_stage, f"monster (type {current_stage})")

            if hunt_quest['status'] == 'not_started':
                server.dialogue_message = f"hey, {target_name} 10 kill."
                hunt_quest['status'] = 'in_progress'
                hunt_quest['current_target_type'] = 1
                hunt_quest['current_kill_count'] = 0
                hunt_quest['total_quest_stage'] = 1

            elif hunt_quest['status'] == 'in_progress':
                if hunt_quest['current_kill_count'] >= 10:
                    hunt_quest['total_quest_stage'] += 1

                    if hunt_quest['total_quest_stage'] > 6:
                        server.dialogue_message = "great, all quest clear!"
                        hunt_quest['status'] = 'completed'
                    else:
                        hunt_quest['current_target_type'] = hunt_quest['total_quest_stage']
                        hunt_quest['current_kill_count'] = 0
                        next_target_name = monster_names.get(hunt_quest['current_target_type'], "next monster")
                        server.dialogue_message = f"good! next {next_target_name} 10 kill."
                else:
                    remaining = 10 - hunt_quest['current_kill_count']
                    server.dialogue_message = f"{target_name} {remaining}more kill."

            elif hunt_quest['status'] == 'completed':
                server.dialogue_message = "thanks."

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
            self.frame_timer -= self.animation_speed  # 타이머 리셋
            self.frame = (self.frame + 1) % 4