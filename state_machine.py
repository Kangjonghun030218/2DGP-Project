from pico2d import *
import game_framework

_stack = []

def push(state):
    _stack.append(state)
    state.enter()

def pop():
    if _stack:
        state = _stack.pop()
        state.exit()
        return state

def change(state):
    pop()
    push(state)

def clear():
    while _stack:
        pop()

def update(frame_time):
    if _stack:
        _stack[-1].update(frame_time)

def draw():
    if _stack:
        for state in _stack:
            state.draw()

def handle_events():
    if not _stack:
        return

    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        else:
            _stack[-1].handle_event(e)