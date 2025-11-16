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