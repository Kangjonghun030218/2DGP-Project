from pico2d import *
import math
import game_globals as g

class NPC:
    def __init__(self):
        self.image1 = load_image('Old_woman_idle.png')
        self.image2 = load_image('Old_man_idle.png')
        self.image3 = load_image('Man_idle.png')
        self.image4 = load_image('Boy_idle.png')
        self.frame = 0

        self.world_x1, self.world_y1 = 550 + 600, 200 + 200
        self.world_x2, self.world_y2 = 50 + 600, 230 + 150
        self.world_x3, self.world_y3 = 150 + 600, 400 + 200
        self.world_x4, self.world_y4 = 300 + 550, 100 + 250

        self.talk_range = 50

    def interact(self, knight_x, knight_y):
        dist_to_1 = math.sqrt((self.world_x1 - knight_x) ** 2 + (self.world_y1 - knight_y) ** 2)
        dist_to_2 = math.sqrt((self.world_x2 - knight_x) ** 2 + (self.world_y2 - knight_y) ** 2)
        quest = g.quest_log['check_npc']

        if dist_to_1 < self.talk_range:
            if quest['status'] == 'not_started':
                g.dialogue_message = "hello?"
                quest['status'] = 'in_progress'
            elif quest['status'] == 'in_progress':
                if quest['talked_to_man']:
                    g.dialogue_message = "hi!"
                    quest['status'] = 'completed'
                else:
                    g.dialogue_message = "nice to meet you"
            elif quest['status'] == 'completed':
                g.dialogue_message = "thank you."
            return True

        elif dist_to_2 < self.talk_range:
            if quest['status'] == 'not_started':
                g.dialogue_message = "hello2"
            elif quest['status'] == 'in_progress':
                g.dialogue_message = "hi2"
                quest['talked_to_man'] = True
            elif quest['status'] == 'completed':
                g.dialogue_message = "thank you2."
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

    def update(self):
        self.frame = (self.frame + 1) % 4