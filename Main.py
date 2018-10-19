import math
from Visualisation import *

lif = 100

class Wave:
    def __init__(self, number, qty = 0, type = 0, density = 0.5):
        self.enemies = []
        self.number = number
        self.qty = qty
        self.type = type
        self.density = density
        self.spawned = 0
        self.gcd = 0

    def print(self, cell):
        for enemy in self.enemies:
            print('|', self.number, enemy.wave_rank, enemy.hp, enemy.effects.__len__(), enemy.get_pos(road_g), enemy.enemy_angle(cell))

    def update(self):
        count = 0
        self.init()
        if not self.enemies:
            return True
        for enemy in self.enemies:
            if not enemy.update():
                del self.enemies[count]
            count += 1
        return False

    def init(self):
        if self.spawned < self.qty:
            if self.gcd == 0:
                self.enemies.append(Regular(self.spawned))
                self.gcd = self.density*self.enemies[0].speed*tickrate - 1
                self.spawned += 1
            else:
                self.gcd -= 1




class Enemy:        # Parent for enemy type classes
    pos = 0         # ++ in every loop

    def __init__(self, hp, speed, wave_rank):
        self.effects = []  # Clear array for effects
        self.hp = hp
        self.speed = speed
        self.wave_rank = wave_rank

    def get_pos(self, road):    # Enemy.pos convert to Cartesian  TODO: catch error out of index for end of a road
        half = self.pos/2
        whole = math.floor(half)
        if road[whole][1] == road[whole + 1][1]:        # If Δ in horizontal direction
            if road[whole][0] < road[whole + 1][0]:     # If direction of  is positive
                return [road[whole][0] + (self.pos - 2*whole),
                        road[whole][1]]
            else:                                       # Direction of Δ is negative
                return [road[whole][0] - (self.pos - 2*whole),
                        road[whole][1]]
        else:                                           # Δ in vertical direction
            if road[whole][1] < road[whole + 1][1]:     # If Δ > 0
                return [road[whole][0],
                        road[whole][1] + (self.pos - 2*whole)]
            else:                                       # Δ < 0
                return [road[whole][0],
                        road[whole][1] - (self.pos - 2*whole)]

    def enemy_angle(self, cell):       # Get enemy angle from 0 relative to tower
        # Compute position differences
        dx = cell.pos[0] - self.get_pos(road_g)[0]
        dy = -(cell.pos[1] - self.get_pos(road_g)[1])
        if dx == 0:
            if dy > 0:
                return 270
            else:
                return 90
        atan = math.degrees(math.atan(dy/dx))
        if dx < 0:
            return atan
        else:
            return atan - 180

    def addeff(self, effect):
        # Function for addition of effects
        self.effects.append(effect)

    def update(self):
        global lif
        # Update for effects
        j = 0
        for effect in self.effects:
            if effect.update():
                del self.effects[j]
        j += 1
        self.pos += self.speed/tickrate
        if self.pos >= (len(road_g) - 1) * 2:
            lif -= 1
            print()
            return False
        return not self.hp <= 0


class Regular(Enemy):
    # Regular enemy has 100 hp and 1 speed
    def __init__(self, wave_rank=-1):
        Enemy.__init__(self, 100, 1, wave_rank)


class Bullet:                   # Bullet effect for shots   # TODO: Make parent class
    def __init__(self, dmg, t, host):
        # Duration input in secs converted to ticks
        self.dmg = dmg
        self.t = t * tickrate
        self.host = host        # Enemy object, on which effect is applied

    def update(self):
        self.t -= 1     # Lower remaining time of effect
        if self.t <= 0:     # If time has passed
            self.host.hp -= self.dmg    # Execute effect's effect
            # Return True if Bullet needs to be deleted
            return True
        return False


class Tower:
    def __init__(self, child, cell):
        self.child = child
        self.cell = cell
        self.cd = 0

    def dist(self, enemy):
        enpos = enemy.get_pos(road_g)
        return math.sqrt((self.cell.pos[0] - enpos[0])**2 + (self.cell.pos[1] - enpos[1])**2)

    def shoot(self, enemy):
        enemy.addeff(Bullet(self.child.dmg, self.dist(enemy)/self.child.prspd, enemy))

    def rotate_and_shoot(self, angl, enemy):     # Rotate tower by given amount
        if math.fabs(angl) < self.child.rtspd / tickrate:   # If angl is less than tick rotation speed
            self.child.rtangl += angl   # Rotate rest of the way
            if self.cd <= 0:
                self.shoot(enemy)     # Shoot the enemy
                self.cd = tickrate/self.child.atspd - 1
            else:
                self.cd -= 1
        else:
            if angl == 0:   # Raise exception if angle to rotate is 0
                raise ValueError('Rotation Δ zero!')
                pass
            # Else if angl is positive, rotate by max speed to + else to -
            self.child.rtangl += self.child.rtspd / tickrate if angl > 0 else -(self.child.rtspd / tickrate)

    def rta(self, enangl):      # Tower-enemy rotate Δ function  TODO: Optimalizuj
        if self.child.rtangl < enangl:    # If angle to enemy is higher than tower's
            if self.child.rtangl - enangl > 180:
                return 360 - (self.child.rtangl - enangl)
            else:
                return enangl - self.child.rtangl
        elif self.child.rtangl == enangl:     # Else if they are the same, return 0
            return 0
        else:   # Else tower's angle is higher than to enemy
            if self.child.rtangl - enangl < -180:
                return 360 + self.child.rtangl - enangl
            else:
                return enangl - self.child.rtangl

    def in_range(self, enemy):
        return self.dist(enemy) <= self.child.rng

    def target_first(self, waves):      # TODO: Multiplication of wave and enemy ranks or something like that
        target = Regular(10000)
        for wave in waves:
            for enemy in wave.enemies:
                if self.in_range(enemy) and enemy.wave_rank < target.wave_rank:
                    target = enemy
        return target


class Basic(Tower):        # Tower in cell
    rng = 4         # Basic tower properties
    dmg = 10
    atspd = 10
    rtspd = 100
    rtangl = 0
    prspd = 10

    def __init__(self, cell):
        Tower.__init__(self, self, cell)


class Cell:
    # Class for place, where tower can stand
    def __init__(self, pos, upgrades=0):
        self.pos = pos
        self.upgrades = upgrades
        self.tower: Tower = 0

    def build_tower_basic(self):
        self.tower = Basic(self)

    def update(self):
        if self.tower != 0:
            target = self.tower.target_first(waves_g)
            print('|', self.tower.rta(target.enemy_angle(self)))
            self.tower.rotate_and_shoot(self.tower.rta(target.enemy_angle(self)), target)


def update():
    count = 0
    for cell in cells_g:
        cell.update()
    for wave in waves_g:
        if wave.update():
            del waves_g[count]
        count += 1
    if not waves_g:
        return True
    return False


coins = 200
road_g = [[5, 3], [7, 3], [7, 5], [7, 7], [5, 7], [3, 7], [3, 5], [3, 3]]
waves_g = []
cells_g = [Cell([5, 5])]
tickrate: int = 100
currtick = 0

graphics_init()

for i in range(1, 6):
    cells_g.append(Cell([1, 2*i+1]))
    cells_g.append(Cell([5, 2*i + 2]))

cells_g[0].build_tower_basic()
waves_g.append(Wave(0, 10, 0, 0.5))
print("")

while True:
    render({'cs': coins, 'rg': road_g, 'wsg': waves_g, 'clsg': cells_g, 'tickrate': tickrate, 'currt': currtick})
    if currtick == 200:
        print('')
    print('-------------')
    print('#' + str(currtick))
    if update():
        break
    waves_g[0].print(cells_g[0])
    print('| Life:', lif)
    currtick += 1 
