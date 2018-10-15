import math

coins = 200
road_g = [[5, 3], [7, 3], [7, 5], [7, 7], [5, 7], [3, 7], [3, 5], [3, 3], [5, 3]]
cells = []
waves = []
tickrate: int = 100

class Wave:
    def __init__(self, enemies, number):
        self.enemies = enemies
        self.number = number


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
            if atan < 0:
                return 360 - atan
            else:
                return atan
        else:
            return 180 + atan

    def addeff(self, effect):
        # Function for addition of effects
        self.effects.append(effect)

    def update(self):
        # Update for effects
        j = 0
        for effect in self.effects:
            if effect.update(self):
                del self.effects[j]
        j += 1


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

    def dist(self, enemy):
        enpos = enemy.get_pos(road_g)
        return math.sqrt((self.cell.pos[0] - enpos[0])**2 + (self.cell.pos[1] - enpos[1])**2)

    def shoot(self, enemy):
        enemy.addeff(Bullet(self.child.dmg, self.dist(enemy)/self.child.prspd, enemy))

    def rotate_and_shoot(self, angl, enemy):     # Rotate tower by given amount
        if math.fabs(angl) < self.child.rtspd / tickrate:   # If angl is less than tick rotation speed
            self.child.rtangl += angl   # Rotate rest of the way
            self.shoot(enemy)     # Shoot the enemy
        else:
            if angl == 0:   # Raise exception if angle to rotate is 0
                raise ValueError('Rotation Δ zero!')
                pass
            # Else if angl is positive, rotate by max speed to + else to -
            self.child.rtangl += self.child.rtspd / tickrate if angl > 0 else -(self.child.rtspd / tickrate)

    def in_range(self, enemy):
        return self.dist(enemy) <= self.child.rng

    def target_first(self, waves):
        target = Regular(10000)
        for wave in waves:
            for enemy in wave.enemies:
                if self.in_range(enemy) and  enemy.wave_rank < target.wave_rank:
                    target = enemy


class Basic(Tower):        # Tower in cell
    rng = 4         # Basic tower properties
    dmg = 10
    atspd = 5
    rtspd = 100
    rtangl = 0
    prspd = 4

    def __init__(self, cell):
        Tower.__init__(self, self, cell)


class Cell:
    # Class for place, where tower can stand
    def __init__(self, pos, upgrades=0):
        self.pos = pos
        self.upgrades = upgrades
        self.tower = 0

    def build_tower_basic(self):
        self.tower = Basic(self)


    def __init__(self, cell):
        Tower.__init__(self, self, cell)

    def rta(self, enangl):      # Tower-enemy rotate Δ function  TODO: Optimalizuj
        if self.rtangl < enangl:    # If angle to enemy is higher than tower's
            if self.rtangl - enangl > 180:
                return 360 - (self.rtangl - enangl)
            else:
                return enangl - self.rtangl
        elif self.rtangl == enangl:     # Else if they are the same, return 0
            return 0
        else:   # Else tower's angle is higher than to enemy
            if self.rtangl - enangl < -180:
                return 360 + self.rtangl - enangl
            else:
                return self.rtangl - enangl


for i in range(1, 6):
    cells.append(Cell([1, 2*i+1]))
    cells.append(Cell([5, 2*i + 2]))

def update():
    for cell in cells:
        if cell.tower != 0:
            target = cell.tower.target_first()
            cell.tower.rotate_and_shoot(cell.tower.rta(target), cell.tower.target_first(target))


c = Cell([5, 5])
c.build_tower_basic()
waves.append(Wave([Regular(0), Regular(1), Regular(2), Regular(3)], 0))