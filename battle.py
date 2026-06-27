import pygame as pg
import os
import settings as st
import state_manager as sm
import heros
import victory

max_healths = {}
battle = None
battle_images = {}

def load_animation_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path), key=lambda x: int(x.split(".")[0])):
        if filename.endswith(".png"):
            path = os.path.join(folder_path, filename)
            frames.append(pg.image.load(path).convert_alpha())
    return frames

class Battle:
    def __init__(self, hero1, hero2):
        self.hero1 = hero1
        self.hero2 = hero2
        self.history = []

def setup_battle():
    global battle, max_healths, battle_images
    h1, h2 = [heros.Hero(n, heros.HERO_DATA[n]['hp'], heros.HERO_DATA[n]['attack']) for n in (sm.selected["Player 2"], sm.selected["Player 1"])]
    max_healths = {h1.name: h1.health, h2.name: h2.health}
    battle = Battle(h1, h2)
    victory.winner_name = None
    battle_images = {}

    hero_list = [(h1, True), (h2, False)]
    for hero, flip in hero_list:
        name = hero.name
        battle_images[name] = {}
        for action in ["idle", "walk", "attack"]:
            folder = os.path.join(st.ASSET_DIR, "sprites", name.lower(), action)
            frames = load_animation_frames(folder)
            battle_images[name][action] = frames
        battle_images[name]["flipped"] = flip
    return []

def draw_battle():
    h1, h2 = battle.hero1, battle.hero2
    st.SCREEN.blit(st.BG_FIGHT, (0, 0))
    st.SCREEN.blit(st.UI_FONT.render("player 1", True, st.TEXT_COLOR), (120, 80))
    st.SCREEN.blit(st.UI_FONT.render("player 2", True, st.TEXT_COLOR), (580, 80))

    def hp_bar(hero, x):
        r = hero.health / max_healths[hero.name]
        pg.draw.rect(st.SCREEN, st.ACCENT_COLOR, (x, 120, 300 * r, 25))
        pg.draw.rect(st.SCREEN, st.TEXT_COLOR, (x, 120, 300, 25), 2)

    hp_bar(h1, 120)
    hp_bar(h2, st.WIDTH - 420)

    keys = pg.key.get_pressed()

    # Player 1 controls
    if keys[pg.K_RIGHT]:
        heros.player_states["Player 1"]["x"] += 2
        heros.player_states["Player 1"]["action"] = "walk"
    elif keys[pg.K_LEFT]:
        heros.player_states["Player 1"]["x"] -= 2
        heros.player_states["Player 1"]["action"] = "walk"
    elif keys[pg.K_RETURN]:
        heros.player_states["Player 1"]["action"] = "attack"
    else:
        heros.player_states["Player 1"]["action"] = "idle"
    if keys[pg.K_UP] and not heros.player_states["Player 1"]["is_jumping"]:
        heros.player_states["Player 1"]["vy"] = st.JUMP_STRENGTH
        heros.player_states["Player 1"]["is_jumping"] = True

    # Player 2 controls
    if keys[pg.K_d]:
        heros.player_states["Player 2"]["x"] += 2
        heros.player_states["Player 2"]["action"] = "walk"
    elif keys[pg.K_a]:
        heros.player_states["Player 2"]["x"] -= 2
        heros.player_states["Player 2"]["action"] = "walk"
    elif keys[pg.K_SPACE]:
        heros.player_states["Player 2"]["action"] = "attack"
    else:
        heros.player_states["Player 2"]["action"] = "idle"
    if keys[pg.K_w] and not heros.player_states["Player 2"]["is_jumping"]:
        heros.player_states["Player 2"]["vy"] = st.JUMP_STRENGTH
        heros.player_states["Player 2"]["is_jumping"] = True

    for p in heros.player_states:
        heros.player_states[p]["vy"] += st.GRAVITY
        heros.player_states[p]["y"] += heros.player_states[p]["vy"]
        if heros.player_states[p]["y"] >= st.GROUND_Y:
            heros.player_states[p]["y"] = st.GROUND_Y
            heros.player_states[p]["vy"] = 0
            heros.player_states[p]["is_jumping"] = False
        heros.player_states[p]["x"] = max(0, min(heros.player_states[p]["x"], st.WIDTH - 100))

    # Draw heroes
    for idx, (player, hero) in enumerate([("Player 1", h1), ("Player 2", h2)]):
        state = heros.player_states[player]
        action = state["action"]
        frames = battle_images[hero.name][action]
        speed = st.frame_speed.get(action, 100)
        frame_idx = (pg.time.get_ticks() // speed) % len(frames)

        img = frames[frame_idx] if frames else None
        if img and battle_images[hero.name]["flipped"]:
            img = pg.transform.flip(img, True, False)
        if img:
            st.SCREEN.blit(pg.transform.smoothscale(img, (100, 100)), (state["x"], state["y"]))

    # Show battle history
    y = 200
    for a, d, dmg in battle.history[-8:]:
        t = f"{a} hit {d} for {dmg}"
        st.SCREEN.blit(st.UI_FONT.render(t, True, st.TEXT_COLOR), (st.WIDTH // 2 - st.UI_FONT.size(t)[0] // 2, y))
        y += 30

    for b in sm.ui_elements:
        b.draw(st.SCREEN)

    # Collision and attacks
    rect1 = pg.Rect(heros.player_states["Player 1"]["x"], heros.player_states["Player 1"]["y"], 50, 50)
    rect2 = pg.Rect(heros.player_states["Player 2"]["x"], heros.player_states["Player 2"]["y"], 50, 50)
    now = pg.time.get_ticks()

    if rect1.colliderect(rect2):
        if heros.player_states["Player 1"]["x"] < heros.player_states["Player 2"]["x"]:
            heros.player_states["Player 1"]["x"] -= 5
            heros.player_states["Player 2"]["x"] += 5
        else:
            heros.player_states["Player 1"]["x"] += 5
            heros.player_states["Player 2"]["x"] -= 5

    if h1.is_alive() and h2.is_alive():
        if heros.player_states["Player 1"]["action"] == "attack":
            hitbox1 = pg.Rect(heros.player_states["Player 1"]["x"] + 50, heros.player_states["Player 1"]["y"], 50, 100)
            if hitbox1.colliderect(rect2) and now - heros.player_states["Player 1"].get("attack_cooldown", 0) > st.ATTACK_COOLDOWN_TIME:
                heros.player_states["Player 1"]["attack_cooldown"] = now
                h2.take_damage(h1.attack)
                battle.history.append((h1.name, h2.name, h1.attack))

        if heros.player_states["Player 2"]["action"] == "attack":
            hitbox2 = pg.Rect(heros.player_states["Player 2"]["x"] - 50, heros.player_states["Player 2"]["y"], 50, 100)
            if hitbox2.colliderect(rect1) and now - heros.player_states["Player 2"].get("attack_cooldown", 0) > st.ATTACK_COOLDOWN_TIME:
                heros.player_states["Player 2"]["attack_cooldown"] = now
                h1.take_damage(h2.attack)
                battle.history.append((h2.name, h1.name, h2.attack))
    else:
        if not victory.winner_name:
            victory.winner_name = h1.name if h1.is_alive() else h2.name
            victory.show_victory()
