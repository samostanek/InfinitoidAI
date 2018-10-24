import pygame as pg
import cmath

screen = 0


def graphics_init():
    global screen
    pg.init()
    screen = pg.display.set_mode((400, 300))

def render(gamestat, k=30):
    # Gamestat dictionary keys: cs - coins, rg - road_g, wsg - waves_g, clsg - cells_g, tickrate, currt - current tick
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    pg.draw.aalines(screen, (0, 255, 0), False, list(map(lambda x: tuple(map(lambda y: (y+0.5)*k, x)), gamestat['rg'])))

    for wave in gamestat['wsg']:
        for e in wave.enemies:
            epos = e.get_pos(gamestat['rg'])
            clr = (e.hp / e.maxhp) * 255
            pg.draw.circle(screen, (clr, 0, 0), (int(epos[0] * k + 0.5 * k), int(epos[1] * k + 0.5 * k)),
                           int(k / 4))

    for cell in gamestat['clsg']:
        pg.draw.rect(screen, (100, 100, 255), pg.Rect(cell.pos[0] * k, cell.pos[1] * k, k, k))
        pg.draw.rect(screen, (0, 0, 0), pg.Rect(cell.pos[0] * k, cell.pos[1] * k, k, k), int(k/16))
        if cell.tower:
            pg.draw.circle(screen, (255, 0, 255), (int(cell.pos[0]*k + 0.5*k), int(cell.pos[1]*k + 0.5*k)), int(k/4))

    pg.display.flip()
    screen.fill((255, 255, 255))
