from pico2d import *
import game_globals as g
import state

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            g.running = False
            return
        if g.current_state:
            g.current_state.handle_event(event)


def change_state(new_state):
    if g.current_state:
        g.current_state.exit()

    g.current_state = new_state

    if g.current_state:
        g.current_state.enter()



open_canvas(g.CANVAS_WIDTH, g.CANVAS_HEIGHT)

g.font = load_font('ARIAL.ttf', 20)
g.bar_bg_image = load_image('bar_bg.png')
g.hp_bar_image = load_image('bar_hp.png')
g.mp_bar_image = load_image('bar_mp.png')
g.skill1_image = load_image('skill1.png')
g.skill2_image = load_image('skill2.png')
g.skill3_image = load_image('skill3.png')
g.hp_potion_image = load_image('hp_potion.png')
g.mp_potion_image = load_image('mp_potion.png')
g.effect_image_R1 = load_image('skill2-1_R.png')
g.effect_image_R2 = load_image('skill2-2_R.png')
g.effect_image_U1 = load_image('skill2-1_U.png')
g.effect_image_U2 = load_image('skill2-2_U.png')
g.effect_image1_R1 = load_image('skill1-1_R.png')
g.effect_image1_U1 = load_image('skill1-1_U.png')
g.projectile_image_LR = load_image('projectile_LR.png')
g.projectile_image_UD = load_image('projectile_UD.png')


g.menu_image = None


g.change_state = change_state
g.states = {
    'menu': state.MenuState(),
    'play': state.PlayState(),
    'map_view': state.MapViewState(),
    'dialogue': state.DialogueState(),
}
g.current_state = None

change_state(g.states['menu'])


last_time = get_time()
while g.running:
    current_time = get_time()
    frame_time = current_time - last_time
    last_time = current_time

    handle_events()

    if g.current_state:
        g.current_state.update(frame_time)

    if g.current_state:
        g.current_state.draw()

if g.current_state:
    g.current_state.exit()

close_canvas()