from pico2d import load_image, load_font, load_music, load_wav

_images = {}
_fonts = {}
_music = {}
_sounds = {}


def load_all():
    print("Loading resources...")

    _images['map_0'] = load_image('resource/map_0.png')
    _images['map_1'] = load_image('resource/map_1.png')
    _images['map_2'] = load_image('resource/map_2.png')
    _images['map_3'] = load_image('resource/map_3.png')
    _images['map_4'] = load_image('resource/map_4.png')

    # --- UI 아이템 이미지 ---
    _images['bar_bg'] = load_image('resource/bar_bg.png')
    _images['bar_hp'] = load_image('resource/bar_hp.png')
    _images['bar_mp'] = load_image('resource/bar_mp.png')
    _images['skill1'] = load_image('resource/skill1.png')
    _images['skill2'] = load_image('resource/skill2.png')
    _images['skill3'] = load_image('resource/skill3.png')
    _images['hp_potion'] = load_image('resource/hp_potion.png')
    _images['mp_potion'] = load_image('resource/mp_potion.png')
    _images['projectile_LR'] = load_image('resource/projectile_LR.png')
    _images['projectile_UD'] = load_image('resource/projectile_UD.png')

    # --- Lvl 1 이미지 ---
    _images['knight_lvl1_idle'] = load_image('resource/Swordsman_lvl1_Idle_with_shadow.png')
    _images['knight_lvl1_walk'] = load_image('resource/Swordsman_lvl1_Walk_with_shadow.png')
    _images['knight_lvl1_run'] = load_image('resource/Swordsman_lvl1_Run_with_shadow.png')
    _images['knight_lvl1_attack'] = load_image('resource/Swordsman_lvl1_Attack_with_shadow.png')
    _images['knight_lvl1_hit'] = load_image('resource/Swordsman_lvl1_Hurt_with_shadow.png')
    _images['knight_lvl1_dead'] = load_image('resource/Swordsman_lvl1_Death_with_shadow.png')

    # --- Lvl 2 이미지 ---
    _images['knight_lvl2_idle'] = load_image('resource/Swordsman_lvl2_Idle_with_shadow.png')
    _images['knight_lvl2_walk'] = load_image('resource/Swordsman_lvl2_Walk_with_shadow.png')
    _images['knight_lvl2_run'] = load_image('resource/Swordsman_lvl2_Run_with_shadow.png')
    _images['knight_lvl2_attack'] = load_image('resource/Swordsman_lvl2_Attack_with_shadow.png')
    _images['knight_lvl2_hit'] = load_image('resource/Swordsman_lvl2_Hurt_with_shadow.png')
    _images['knight_lvl2_dead'] = load_image('resource/Swordsman_lvl2_Death_with_shadow.png')

    # --- Lvl 3 이미지 ---
    _images['knight_lvl3_idle'] = load_image('resource/Swordsman_lvl3_Idle_with_shadow.png')
    _images['knight_lvl3_walk'] = load_image('resource/Swordsman_lvl3_Walk_with_shadow.png')
    _images['knight_lvl3_run'] = load_image('resource/Swordsman_lvl3_Run_with_shadow.png')
    _images['knight_lvl3_attack'] = load_image('resource/Swordsman_lvl3_Attack_with_shadow.png')
    _images['knight_lvl3_hit'] = load_image('resource/Swordsman_lvl3_Hurt_with_shadow.png')
    _images['knight_lvl3_dead'] = load_image('resource/Swordsman_lvl3_Death_with_shadow.png')

    # --- 스킬 Lvl 1  이펙트 ---
    _images['effect_skill1_R1'] = load_image('resource/skill1-1_R.png')
    _images['effect_skill1_U1'] = load_image('resource/skill1-1_U.png')
    _images['effect_skill2_R1'] = load_image('resource/skill2-1_R.png')
    _images['effect_skill2_R2'] = load_image('resource/skill2-2_R.png')
    _images['effect_skill2_U1'] = load_image('resource/skill2-1_U.png')
    _images['effect_skill2_U2'] = load_image('resource/skill2-2_U.png')

    _images['knight_lvl1_skill1_new'] = [
        load_image('resource/skill1_lv1.png'),
        load_image('resource/skill1_lv1_2.png'),
        load_image('resource/skill1_lv1_3.png'),
        load_image('resource/skill1_lv1_4.png')
    ]

    # --- 스킬 Lvl 2-2 이펙트  ---
    _images['skill_lvl2_anim'] = [load_image(f'resource/lvl2-{i}.png') for i in range(1, 13)]

    #보류중인 이펙트
    _images['skill1_new_sheet'] = load_image('resource/skill1_sheet.png')
    _images['knight_lvl3_skill2_new'] = [
        load_image('resource/66680.png'),
        load_image('resource/66681.png'),
        load_image('resource/66682.png'),
        load_image('resource/66683.png'),
        load_image('resource/66684.png'),
        load_image('resource/66685.png'),
        load_image('resource/66686.png'),
        load_image('resource/66687.png'),
        load_image('resource/66688.png'),
        load_image('resource/66697.png'),
        load_image('resource/66698.png'),
        load_image('resource/66699.png'),
        load_image('resource/66700.png'),
        load_image('resource/66701.png'),
    ]


    _images['skill_lvl2_R_anim'] = [
        load_image('resource/15931.png'), load_image('resource/15932.png'),
        load_image('resource/15933.png'), load_image('resource/15934.png')
    ]
    _images['skill_lvl2_U_anim'] = [
        load_image('resource/15931_U.png'), load_image('resource/15932_U.png'),
        load_image('resource/15933_U.png'), load_image('resource/15934_U.png')
    ]
    _images['skill_lvl3_R_anim'] = [
        load_image('resource/75639.png'), load_image('resource/75645.png'),
        load_image('resource/75653.png'), load_image('resource/75655.png'),
        load_image('resource/75661.png'), load_image('resource/75667.png')
    ]
    _images['skill_lvl3_U_anim'] = [
        load_image('resource/75639_U.png'), load_image('resource/75645_U.png'),
        load_image('resource/75653_U.png'), load_image('resource/75655_U.png'),
        load_image('resource/75661_U.png'), load_image('resource/75667_U.png')
    ]
    # 오크 1
    _images['orc1_idle'] = load_image('resource/orc1_idle_with_shadow.png')
    _images['orc1_run'] = load_image('resource/orc1_run_with_shadow.png')
    _images['orc1_attack'] = load_image('resource/orc1_attack_with_shadow.png')
    _images['orc1_hurt'] = load_image('resource/orc1_hurt_with_shadow.png')
    _images['orc1_dead'] = load_image('resource/orc1_death_with_shadow.png')
    # 오크 2
    _images['orc2_idle'] = load_image('resource/orc2_idle_with_shadow.png')
    _images['orc2_run'] = load_image('resource/orc2_run_with_shadow.png')
    _images['orc2_attack'] = load_image('resource/orc2_attack_with_shadow.png')
    _images['orc2_hurt'] = load_image('resource/orc2_hurt_with_shadow.png')
    _images['orc2_dead'] = load_image('resource/orc2_death_with_shadow.png')
    # 오크 3
    _images['orc3_idle'] = load_image('resource/orc3_idle_with_shadow.png')
    _images['orc3_run'] = load_image('resource/orc3_run_with_shadow.png')
    _images['orc3_attack'] = load_image('resource/orc3_attack_with_shadow.png')
    _images['orc3_hurt'] = load_image('resource/orc3_hurt_with_shadow.png')
    _images['orc3_dead'] = load_image('resource/orc3_death_with_shadow.png')

    # 슬라임 1
    _images['slime1_idle'] = load_image('resource/Slime1_Idle_with_shadow.png')
    _images['slime1_run'] = load_image('resource/Slime1_Run_with_shadow.png')
    _images['slime1_attack'] = load_image('resource/Slime1_Attack_with_shadow.png')
    _images['slime1_hurt'] = load_image('resource/Slime1_Hurt_with_shadow.png')
    _images['slime1_dead'] = load_image('resource/Slime1_Death_with_shadow.png')
    # 슬라임 2
    _images['slime2_idle'] = load_image('resource/Slime2_Idle_with_shadow.png')
    _images['slime2_run'] = load_image('resource/Slime2_Run_with_shadow.png')
    _images['slime2_attack'] = load_image('resource/Slime2_Attack_with_shadow.png')
    _images['slime2_hurt'] = load_image('resource/Slime2_Hurt_with_shadow.png')
    _images['slime2_dead'] = load_image('resource/Slime2_Death_with_shadow.png')
    # 슬라임 3
    _images['slime3_idle'] = load_image('resource/Slime3_Idle_with_shadow.png')
    _images['slime3_run'] = load_image('resource/Slime3_Run_with_shadow.png')
    _images['slime3_attack'] = load_image('resource/Slime3_Attack_with_shadow.png')
    _images['slime3_hurt'] = load_image('resource/Slime3_Hurt_with_shadow.png')
    _images['slime3_dead'] = load_image('resource/Slime3_Death_with_shadow.png')
    #엔피씨
    _images['npc_old_woman'] = load_image('resource/Old_woman_idle.png')
    _images['npc_old_man'] = load_image('resource/Old_man_idle.png')
    _images['npc_man'] = load_image('resource/Man_idle.png')
    _images['npc_boy'] = load_image('resource/Boy_idle.png')
    #포탈
    _images['portal'] = load_image('resource/battle_filed_portal.png')
    _images['boss_portal'] = load_image('resource/boss_portal.png')
    _images['boss_load_portal'] = load_image('resource/boss_load_portal.png')
    _images['village_portal'] = load_image('resource/village_portal.png')
    #보스
    _images['boss_body'] = load_image('resource/body.png')
    _images['boss_arm_l'] = load_image('resource/l_hand.png')
    _images['boss_arm_r'] = load_image('resource/r_hand.png')
    _images['boss_skill_icon'] = load_image('resource/boss_skill_icon.png')
    _images['boss_skill_effect'] = load_image('resource/58590.png')
    _images['boss_skill2_icon'] = load_image('resource/boss_skill_icon2.png')
    _images['boss_skill2_effect'] = load_image('resource/boss_skill2.png')

    _images['princess_sheet'] = load_image('resource/princess_sheet.png')
    _images['cage'] = load_image('resource/cage.png')

    _images['boss_clear_portal'] = load_image('resource/clear_portal.png')
    _images['game_clear_screen'] = load_image('resource/game_clear.png')


    _images['boss_skill3_icon'] = load_image('resource/boss_skill3_icon.png')
    _images['boss_charge_anim'] = []
    for i in range(1, 9):
        _images['boss_charge_anim'].append(load_image(f'resource/{i:03d}.png'))

    _images['boss_fire_anim'] = []
    for i in range(1, 37):
        _images['boss_fire_anim'].append(load_image(f'resource/{i:02d}.png'))

    _images['quest_board'] = load_image('resource/quest.png')
    _images['dialogue_bg'] = load_image('resource/quest_space.png')

    #퀘스트
    _images['quest_start'] = load_image('resource/quest_start.png')
    _images['quest_ing'] = load_image('resource/quest_ing.png')
    _images['quest_end'] = load_image('resource/quest_end.png')

    # --- 폰트 ---
    _fonts['default'] =  load_font('resource/malgunbd.ttf', 20)
    #레벨업 이펙트
    _images['level_up_effect'] = [
        load_image('resource/level_up_1.png'),
        load_image('resource/level_up_2.png'),
        load_image('resource/level_up_3.png'),
        load_image('resource/level_up_4.png'),
        load_image('resource/level_up_5.png')
    ]
    _images['start_button'] = load_image('resource/start_button.png')

    #SOund!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    _music['menu_bgm'] = load_music('Sound/메인화면소리.mp3')
    _music['village_bgm'] = load_music('Sound/마을소리.mp3')
    _music['battle_bgm'] = load_music('Sound/전장소리.mp3')
    _music['boss_path_bgm'] = load_music('Sound/보스길소리.mp3')
    _music['boss_room_bgm'] = load_music('Sound/보스방소리.mp3')
    _music['clear_bgm'] = load_music('Sound/클리어화면소리.mp3')

    #effect sound!!!!
    _sounds['orc_death'] = load_wav('Sound/오크죽는소리.wav')
    _sounds['slime_death'] = load_wav('Sound/슬라임죽는소리.wav')
    _sounds['item_pickup'] = load_wav('Sound/아이템줍기소리.wav')
    _sounds['level_up'] = load_wav('Sound/레벨업_소리.wav')
    _sounds['boss_thunder'] = load_wav('Sound/보스_번개소리.wav')
    _sounds['boss_laser'] = load_wav('Sound/보스_레이져소리.wav')
    _sounds['boss_homing'] = load_wav('Sound/보스_유도스킬소리.wav')
    _sounds['p_skill2_slash'] = load_wav('Sound/플레이어_skill2.wav')
    _sounds['p_skill2_bomb'] = load_wav('Sound/플레이어_skill2_bomb.wav')

    _sounds['p_skill1_lv1'] = load_wav('Sound/랩1_skill1.wav')
    _sounds['p_skill1_lv2'] = load_wav('Sound/랩2_skill1.wav')
    _sounds['p_skill1_lv3'] = load_wav('Sound/랩3_skill1.wav')
    _sounds['p_skill3'] = load_wav('Sound/스킬3.wav')

    _sounds['orc_death'].set_volume(30)
    _sounds['slime_death'].set_volume(30)
    _sounds['boss_thunder'].set_volume(80)
    _sounds['boss_laser'].set_volume(50)
    _sounds['boss_homing'].set_volume(80)
    _sounds['p_skill2_slash'].set_volume(90)
    _sounds['p_skill2_bomb'].set_volume(90)
    _sounds['p_skill1_lv1'].set_volume(60)
    _sounds['p_skill1_lv2'].set_volume(70)
    _sounds['p_skill1_lv3'].set_volume(60)
    _sounds['p_skill3'].set_volume(80)

    for music in _music.values():
        music.set_volume(64)



def get_image(key):
    return _images.get(key)


def get_font(key='default'):
    return _fonts.get(key)

def get_music(key):
    return _music.get(key)

def get_sound(key):
    return _sounds.get(key)