import pygame as pg
import settings as st
import os
import state_manager as sm
import heros

#كلاس الخاص ببطاقات الابطال
class HeroCard:
    # خصائص كل بطاقة 
    def __init__(self, name, image_path, pos, callback, disabled=False):
        self.name, self.callback, self.disabled = name, callback, disabled
        self.image = pg.transform.smoothscale(pg.image.load(image_path).convert_alpha(), (400, 400))
        self.rect = self.image.get_rect(topleft=pos)
    # من اجل رسم البطاقة مع المستطيل الخاص بها
    def draw(self, surf):
        surf.blit(self.image, self.rect)
    
        if self.disabled:
            text = pg.font.Font(os.path.join(st.ASSET_DIR, "fonts/press_start.ttf"), 30).render("Taken", True, st.ACCENT_COLOR)
            surf.blit(text, text.get_rect(midtop=(self.rect.centerx, self.rect.top + 20)))
    def handle_event(self, ev):
        if not self.disabled and ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1 and self.rect.collidepoint(ev.pos):
            self.callback(self.name)


def build_select():
    taken = sm.selected["Player 1"]
    hero_files = {"Goblin": "goblin_card.png", "Mushroom": "mushroom_card.png", "Skeleton": "skeleton_card.png"}
    return [HeroCard(n, os.path.join(st.ASSET_DIR, "cards", f), ((st.WIDTH - 3 * 270 - 2 * 60) // 2 + i * 280, 300), heros.choose_hero, n == taken and sm.current_player == "Player 2") for i, (n, f) in enumerate(hero_files.items())]
