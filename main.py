import pygame as pg
import sys , os 
import state_manager as sm
import settings as st
import victory
import battle as btle

while True:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if sm.state == sm.STATE_MAIN_MENU and ev.type == pg.KEYDOWN:
            sm.switch_state(sm.STATE_SELECT)
        for e in sm.ui_elements:
            e.handle_event(ev)
            
        if victory.show_victory_screen:
            for b in victory.victory_buttons:
                b.handle_event(ev)


    st.BLINK_TIMER += st.clock.get_time()
    if st.BLINK_TIMER >= st.BLINK_INTERVAL:
        st.BLINK_TIMER = 0
        st.SHOW_TEXT = not st.SHOW_TEXT

    if sm.state == sm.STATE_MAIN_MENU:
        st.SCREEN.blit(st.BG_MENU, (0, 0))
    elif sm.state == sm.STATE_SELECT:
        st.SCREEN.blit(st.BG_SELECT, (0, 0))
    elif sm.state == sm.STATE_BATTLE:
        st.SCREEN.blit(st.BG_FIGHT, (0, 0))

    if sm.state == sm.STATE_MAIN_MENU and st.SHOW_TEXT:
        t = st.TITLE_FONT.render("Tap any key to start", True, st.TEXT_COLOR)
        st.SCREEN.blit(t, t.get_rect(center=(st.WIDTH//2,st.HEIGHT - 260)))
    elif sm.state == sm.STATE_SELECT:
        title = st.TITLE_FONT.render(f"{sm.current_player} - Select Your Hero", True, (255, 200, 0))
        st.SCREEN.blit(title, title.get_rect(center=(st.WIDTH//2, 100)))
        for c in sm.ui_elements:
            c.draw(st.SCREEN)
    elif sm.state == sm.STATE_BATTLE:
        btle.draw_battle()

    if victory.show_victory_screen:
        o = pg.Surface((st.WIDTH, st.HEIGHT), pg.SRCALPHA)
        o.fill((0, 0, 0, 200))
        st.SCREEN.blit(o, (0, 0)) 

        msg = st.UI_FONT.render(f" {victory.winner_name} Wins!", True, st.TEXT_COLOR)
        st.SCREEN.blit(msg, msg.get_rect(center=(st.WIDTH//2, st.HEIGHT//2 - 30)))
        for b in victory.victory_buttons:
            b.draw(st.SCREEN)

    pg.display.flip()
    st.clock.tick(st.FPS)