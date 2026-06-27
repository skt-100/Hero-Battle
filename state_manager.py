import pygame as pg
import settings as st
import battle as b
import hero_card as hc
import heros

pg.init()

#تعيين رقم لكل حالة 
STATE_MAIN_MENU = 0
STATE_SELECT = 1
STATE_BATTLE = 2

#تهيئة الحالات 
state = STATE_MAIN_MENU
selected = {"Player 1": None, "Player 2": None}
current_player = "Player 1"
ui_elements = []
battle = None
max_healths = None
battle_images = []

#تأثير الانتقال بين الحالات 
def fade_transition():
    fade = pg.Surface((st.WIDTH,st.HEIGHT)); fade.fill((0,0,0))
    for a in range(0, 255, 10):
        fade.set_alpha(a); st.SCREEN.blit(st.SCREEN.copy(), (0, 0)); st.SCREEN.blit(fade, (0, 0))
        pg.display.update(); pg.time.delay(15)


# التبديل بين الحالات 
def switch_state(new_state):
    global state, ui_elements, current_player, winner_name
    fade_transition()
    state = new_state
    ui_elements.clear()
    if state == STATE_MAIN_MENU:
        current_player, winner_name = "Player 1", None
        selected.update({"Player 1": None, "Player 2": None})
    elif state == STATE_SELECT:
        ui_elements[:] = hc.build_select()
    elif state == STATE_BATTLE:
        ui_elements[:] = b.setup_battle()
        heros.player_states = {
        "Player 1": {"x": 100, "y": 510, "vy": 0, "is_jumping": False,"attack_cooldown":0, "action": "idle"},
        "Player 2": {"x": st.WIDTH - 200, "y": 510, "vy": 0, "is_jumping": False,"attack_cooldown":0, "action": "idle"}
        }

