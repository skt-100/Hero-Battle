import pygame as pg
import os 
import settings as st


#تهيئة pygame
pg.init()
#كلاس التحكم في الزر
class Button:
    #خصائص الزر
    def __init__(self, text, pos, size, callback):
        self.text, self.rect, self.callback = text, pg.Rect(pos, size), callback
    #رسم الزر 
    def draw(self, surf):
        pg.draw.rect(surf, st.BUTTON_COLOR, self.rect, border_radius=8) # خصائسص المستطيل الخاص بالزر
        lbl = st.UI_FONT.render(self.text, True, st.TEXT_COLOR) # خصائص النص الموجود بالزر
        surf.blit(lbl, lbl.get_rect(center=self.rect.center)) # رسم الزر داخل النص
    def handle_event(self, ev):
        if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1 and self.rect.collidepoint(ev.pos):
            self.callback()