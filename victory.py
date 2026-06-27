import state_manager as sm
import button as btn
import settings as st
import heros as h

#تهيئة واجهة الفوز
show_victory_screen = False
victory_buttons = []

# بيانات واجهة الفوز
winner_name = None
winner_time = 0 

#اخفاء واجهة الفوز
def hide_victory():
    global show_victory_screen, victory_buttons
    show_victory_screen = False
    victory_buttons.clear()

# اظهار واجهة الفوز
def show_victory():
   
    global show_victory_screen, victory_buttons
    show_victory_screen = True
    victory_buttons = []

    # دالة زر ال main menu
    def to_main_menu():
        sm.switch_state(sm.STATE_MAIN_MENU)
        hide_victory()
    # دالة زر ال replay
    def replay():
        sm.switch_state(sm.STATE_BATTLE)
        hide_victory()

    # رسم الازرار 
    b1 = btn.Button("Replay", (st.WIDTH//2 - 170, st.HEIGHT//2 + 60), (140, 40), replay)
    b2 = btn.Button("Main Menu", (st.WIDTH//2 + 30, st.HEIGHT//2 + 60), (180, 40), to_main_menu)
    victory_buttons.extend([b1, b2])
