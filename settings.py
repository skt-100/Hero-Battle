import pygame as pg
import os 

#تهيئة pygame
pg.init()

#اعدادات المسارات 
BASE_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(BASE_DIR, "assets")
SPRITE_DIR = os.path.join(ASSET_DIR, "sprites")
CARD_DIR = os.path.join(ASSET_DIR, "cards")
FONT_FILE = os.path.join(ASSET_DIR, "fonts", "press_start.ttf")

#اعدادات النافذة 
WIDTH, HEIGHT = 1000, 800
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
clock,FPS = pg.time.Clock(),120
#اعدادات الخلفية 
BG_MENU = pg.transform.scale(pg.image.load(os.path.join(ASSET_DIR, "menu_background.png")), (WIDTH,HEIGHT ))
BG_SELECT = pg.transform.scale(pg.image.load(os.path.join(ASSET_DIR, "select_background.png")), (WIDTH, HEIGHT))
BG_FIGHT = pg.transform.scale(pg.image.load(os.path.join(ASSET_DIR, "figh_background.png")), (WIDTH, HEIGHT))

# أعدادات الخط
ACCENT_COLOR, TEXT_COLOR, BUTTON_COLOR = (255, 50, 50), (255, 230, 230), (100, 0, 0)
UI_FONT = pg.font.Font(FONT_FILE, 14)
TITLE_FONT = pg.font.Font(FONT_FILE, 30)
#اعدادات التوقيت 
ATTACK_COOLDOWN_TIME = 500 #ميليي ثانية
# اعدادات القفز
GRAVITY = 0.5
JUMP_STRENGTH = -15
GROUND_Y = 510
#اعدادات الفريمات 
frame_speed = {
    "idle": 100,
    "walk": 100,
    "attack": 40
}

#اعدادات الوميض الخاصة ب tap any key to start
BLINK_TIMER = 0
SHOW_TEXT = True
BLINK_INTERVAL = 500
