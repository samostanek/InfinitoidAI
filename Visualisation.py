import pygame as pg

screen = 0


def graphics_init():
    global screen
    pg.init()
    screen = pg.display.set_mode((400, 300))


def render(gamestat, k=30):
    # Gamestat dictionary keys: cs - coins, rg - road_g, wsg - waves_g, clsg - cells_g, tickrate, currt - current tick
    pg.init()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    pg.draw.aalines(screen, (0, 255, 0), False, list(map(lambda x: tuple(map(lambda y: (y+0.5)*k, x)), gamestat['rg'])))

    for wave in gamestat['wsg']:
        for e in wave.enemies:
            epos = e.get_pos(gamestat['rg'])
            pg.draw.rect(screen, (255, 0, 0), pg.Rect(epos[0]*k, epos[1]*k, k-5, k-5))

    for cell in gamestat['clsg']:
        pg.draw.rect(screen, (0, 0, 255), pg.Rect(cell.pos[0] * k, cell.pos[1] * k, k - 5, k - 5))

    pg.display.flip()
    screen.fill((255, 255, 255))
