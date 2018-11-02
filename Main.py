import time
import subprocess
from Visualisation import *

lif = 100


class Wave:
    def __init__(self, number, multi, eqty=0, wtype=0, density=0.5):
        self.enemies = []
        self.number = number
        self.qty = eqty
        self.type = wtype
        self.density = density
        self.multi = multi
        self.spawned = 0
        self.gcd = 0

    def print(self):
        print('|', 'N:' + str(self.number), '(' + str(len(self.enemies)) + '/' + str(self.qty) + ')')

    def update(self):
        count = 0
        self.init()
        if not self.enemies and self.spawned == self.qty:
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
                self.gcd = self.density*tickrate/self.enemies[0].speed - 1
                self.spawned += 1
            else:
                self.gcd -= 1


class Enemy:        # Parent for enemy type classes
    pos = 0         # ++ in every loop

    def __init__(self, hp, speed, wave_rank):
        self.effects = []  # Clear array for effects
        self.hp = hp
        self.maxhp = hp
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
        global lif, coins
        # Update for effects
        for j in range(len(self.effects) - 1, -1, -1):
            if self.effects[j].update():
                del self.effects[j]
        self.pos += self.speed/tickrate
        if self.pos >= (len(road_g) - 1) * 2:
            lif -= 1
            return False
        if self.hp <= 0:
            coins += 5
            return False
        return True


class Regular(Enemy):
    # Regular enemy has 100 hp and 1 speed
    def __init__(self, wave_rank=-1):
        Enemy.__init__(self, 100*multiply, 1, wave_rank)


class Bullet:                   # Bullet effect for shots   # TODO: Make parent class
    def __init__(self, dmg, duration, host):
        # Duration input in secs converted to ticks
        self.dmg = dmg
        self.t = duration * tickrate
        self.host = host        # Enemy object, on which effect is applied

    def update(self):
        global damageDealt
        self.t -= 1     # Lower remaining time of effect
        if self.t <= 0:     # If time has passed
            self.host.hp -= self.dmg   # Execute effect's effect
            damageDealt += self.dmg
            # Return True if Bullet needs to be deleted
            return True
        return False


class Tower:
    def __init__(self, child, cell):
        self.child = child
        self.cell = cell
        self.incd = math.floor(tickrate/self.child.atspd - 1)
        self.cd = 0
        self.rdsht = 0

    def dist(self, enemy):
        enpos = enemy.get_pos(road_g)
        return math.sqrt((self.cell.pos[0] - enpos[0])**2 + (self.cell.pos[1] - enpos[1])**2)

    def shoot(self, enemy):
        self.rdsht = enemy
        enemy.addeff(Bullet(self.child.dmg, self.dist(enemy)/self.child.prspd, enemy))

    def rotate_and_shoot(self, angl, enemy):     # Rotate tower by given amount
        if math.fabs(angl) < self.child.rtspd / tickrate:   # If angl is less than tick rotation speed
            self.child.rtangl += angl   # Rotate rest of the way
            if self.cd <= 0:
                self.shoot(enemy)     # Shoot the enemy
                self.cd = self.incd
            else:
                self.cd -= 1
        else:
            if angl == 0:   # Raise exception if angle to rotate is 0
                raise ValueError('Rotation Δ zero!')
                pass
            # Else if angl is positive, rotate by max speed to + else to -
            self.child.rtangl += self.child.rtspd / tickrate if angl > 0 else -(self.child.rtspd / tickrate)
            if self.cd > 0:
                self.cd -= 1

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
        target = 0
        choose = False
        for wave in waves:
            for enemy in wave.enemies:
                if self.in_range(enemy) and (not target or enemy.wave_rank < target.wave_rank):
                    target = enemy
        return target


class Basic(Tower):        # Tower in cell
    rng = 6         # Basic tower properties
    dmg = 70
    atspd = 3
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

    def update(self):
        if self.tower:
            target = self.tower.target_first(waves_g)
            if target != 0:
                self.tower.rotate_and_shoot(self.tower.rta(target.enemy_angle(self)), target)
            elif self.tower.cd > 0:
                self.tower.cd -= 1

    def print(self):
        if self.tower != 0:
            print('|', self.pos, math.floor(self.tower.cd), math.floor(self.tower.child.rtangl))


def build_tower(pos, ttype=Basic):
    global coins
    built = False
    if coins >= 50:
        for cell in cells_g:
            if cell.pos == pos:
                cell.tower = ttype(cell)
                coins -= 50
                print('Done!')
                built = True
        if not built:
            print('No cell!')
    else:
        print('No money - no honey!')


def update():
    wave_gen()
    for cell in cells_g:
        cell.update()
    count = 0
    for wave in waves_g:
        if wave.update():
            del waves_g[count]
        count += 1
    if lif <= 0:
        return True
    return False


def gu():
    time.sleep(0.005)
    ticktime = time.time()
    global currtick, end, t, coins, road_g, waves_g, cells_g, tickrate
    print('-------------')
    print('#' + str(currtick))
    if update():
        end = True
    print('|Towers:')
    for cell in cells_g:
        cell.print()
    print('|Waves:')
    for wave in waves_g:
        wave.print()
    print('|Life:', lif)
    print('|Coins:', coins)

    render({'cs': coins, 'rg': road_g, 'wsg': waves_g, 'clsg': cells_g, 'tickrate': tickrate, 'currt': currtick})
    p.stdin.write(str(coins).encode())

    t += time.time() - ticktime
    currtick += 1


def wave_gen():
    global wavenum, wcd, multiply
    if wcd == 0:
        waves_g.append(Wave(wavenum, multiply, qty, 0))
        wavenum += 1
        wcd = waverate
        multiply += multiplier
    else:
        wcd -= 1


coins = 200
road_g = [[7, 3], [9, 3], [11, 3], [11, 5], [11, 7], [11, 9], [9, 9], [7, 9], [7, 11], [7, 13],
          [9, 13], [11, 13], [13, 13], [15, 13], [15, 11], [15, 9], [15, 7], [17, 7], [19, 7], [19, 9],
          [19, 11], [19, 13], [19, 15], [19, 17], [17, 17], [15, 17], [13, 17], [11, 17], [9, 17], [7, 17],
          [5, 17], [3, 17], [3, 15], [3, 13], [3, 11], [3, 9], [3, 7], [3, 5], [5, 5]]
waves_g = []
cells_g = [Cell([13, 1]), Cell([3, 3]), Cell([5, 3]), Cell([1, 5]), Cell([7, 5]),
           Cell([9, 5]), Cell([17, 5]), Cell([13, 7]), Cell([21, 7]), Cell([5, 7]),
           Cell([7, 7]), Cell([9, 7]), Cell([1, 9]), Cell([5, 9]), Cell([13, 9]),
           Cell([17, 9]), Cell([5, 11]), Cell([9, 11]), Cell([11, 11]), Cell([13, 11]),
           Cell([17, 11]), Cell([1, 13]), Cell([5, 13]), Cell([17, 13]), Cell([5, 15]),
           Cell([7, 15]), Cell([9, 15]), Cell([11, 15]), Cell([13, 15]), Cell([15, 15]),
           Cell([17, 15]), Cell([21, 15]), Cell([1, 17]), Cell([5, 19]), Cell([11, 19]), Cell([17, 19])]
t = 0
multiply = 1
multiplier = float(input('Multiplier:')) - 1
tickrate = 100
waverate = tickrate*30
wcd = 0
wavenum = 0
currtick = 0
passrate = 0
inp = 0
qty = int(input("Number of enemies in the wave:"))
end = False
damageDealt = 0

graphics_init()
p = subprocess.Popen(["java", "-jar", "Visualisation.jar"], stdin=subprocess.PIPE)

while True:
    inp = input('>').split()
    cmd = inp[0]
    if cmd == 'pass':
        for i in range(0, int(inp[1])):
            gu()
            if end:
                break
    elif cmd == 'end':
        while not end:
            gu()
    elif cmd == 'build':
        build_tower([int(inp[1]), int(inp[2])])
    elif cmd == 'money':
        print(coins)
    if end:
        break
    if currtick != 0:
        print()
        print('Got waves:', wavenum)
        print('Damage dealt:', damageDealt)
        print('Time:', math.floor(t))
        print('Timerate', math.floor(currtick/t))
        print()
