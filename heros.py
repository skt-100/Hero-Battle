import settings as st
import state_manager as sm
import hero_card as hc

#منطق البطل 
class Hero:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0


#بيانات الابطال 
HERO_DATA = {
    "Skeleton": {"hp": 8,
                 "attack": 2, 
                 "file": "skeleton.png"},

    "Goblin":   {"hp": 6,
                "attack": 2, 
                "file": "goblin.png"},
                
    "Mushroom": {"hp": 8,
                 "attack": 1,
                 "file": "mushroom.png"},
}

#حالة البطل 
player_states = {
    "Player 1": {"x": 100, "y": 510, "vy": 0, "is_jumping": False,"attack_cooldown":0, "action": "idle"},
    "Player 2": {"x": st.WIDTH - 200, "y": 510, "vy": 0, "is_jumping": False,"attack_cooldown":0, "action": "idle"}
}

# اختيار البطل
def choose_hero(name):
    sm.selected[sm.current_player] = name
    if sm.current_player == "Player 1":
        sm.current_player = "Player 2"
        sm.ui_elements[:] = hc.build_select()
    else:
        sm.switch_state(sm.STATE_BATTLE)
