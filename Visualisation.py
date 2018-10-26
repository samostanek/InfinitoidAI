import pygame as pg
import cmath, math

screen = 0
size = 800

def graphics_init():
    global screen
    pg.init()
    screen = pg.display.set_mode((size, size))

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
        k2 = 2*k
        cpos = list(map(lambda x: (x - 0.5) * k, cell.pos))
        pg.draw.rect(screen, (100, 100, 255), pg.Rect(cpos[0], cpos[1], k2, k2))
        pg.draw.rect(screen, (0, 0, 0), pg.Rect(cpos[0], cpos[1], k2, k2), int(k/16))
        if cell.tower:
            cdclr = cell.tower.cd/(math.floor(gamestat['tickrate']/cell.tower.atspd - 1))*255
            pg.draw.circle(screen, (cdclr, 255-cdclr, 0), (int(cell.pos[0]*k + 0.5*k), int(cell.pos[1]*k + 0.5*k)), int(k/4))
            pg.draw.circle(screen, (0, 0, 0), (int(cell.pos[0]*k + 0.5*k), int(cell.pos[1]*k + 0.5*k)), int(k*cell.tower.child.rng), int(k/16))

    pg.display.flip()
    screen.fill((255, 255, 255))

def shootrender(cell, enemy, road_g, k=30):
    pg.draw.aaline(screen, (0, 0, 0), (int(cell.pos[0]*k + 0.5*k), int(cell.pos[1]*k + 0.5*k)), (int(enemy.get_pos(road_g)[0]*k + 0.5*k), int(enemy.get_pos(road_g)[1]*k + 0.5*k)))
