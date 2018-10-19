import pygame as pg

screen = 0


def graphics_init():
    global screen
    pg.init()
    screen = pg.display.set_mode((400, 300))


def render(gamestat, k=10):
    # Gamestat dictionary keys: cs - coins, rg - road_g, wsg - waves_g, clsg - cells_g, tickrate, currt - current tick
    pg.init()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    for rdc in gamestat['rg']:
        pg.draw.rect(screen, (0, 255, 0), pg.Rect(rdc[0]*k, rdc[1]*k, k, k))
    for wave in gamestat['wsg']:
        for e in wave.enemies:
            epos = e.get_pos()
            pg.draw.rect(screen, (0, 255, 0), pg.Rect(epos[0]*k, epos[1]*k, k-5, k-5))
    pg.draw.rect(screen, (0, 128, 255), pg.Rect(30, 30, 60, 60))
    pg.display.flip()
