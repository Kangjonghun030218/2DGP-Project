import resource_manager

class Potion:
    def __init__(self, x, y, potion_type):
        self.world_x = x
        self.world_y = y
        self.potion_type = potion_type

        if self.potion_type == 'hp':
            self.image = resource_manager.get_image('hp_potion')
        else:
            self.image = resource_manager.get_image('mp_potion')

        self.width = self.image.w
        self.height = self.image.h

    def draw(self, cam_x, cam_y):
        screen_x = self.world_x - cam_x
        screen_y = self.world_y - cam_y
        self.image.draw(screen_x, screen_y,40,40)

    def get_bb(self):
        half_width = self.width / 2
        half_height = self.height / 2
        return (self.world_x - half_width, self.world_y - half_height,
                self.world_x + half_width, self.world_y + half_height)

    def update(self):
        pass