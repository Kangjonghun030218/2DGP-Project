import state_machine
from pico2d import get_time, update_canvas, clear_canvas

running = True


def run(start_state):
    global running
    running = True

    state_machine.push(start_state)
    last_time = get_time()

    while running:
        current_time = get_time()
        frame_time = current_time - last_time
        last_time = current_time

        # 상태 머신을 통해 모든 것을 처리
        state_machine.handle_events()
        state_machine.update(frame_time)

        clear_canvas()
        state_machine.draw()
        update_canvas()

    state_machine.clear()


def quit():
    global running
    running = False