import math

coins = 200
road_g = [[5, 3], [7, 3], [7, 5], [7, 7], [5, 7], [3, 7], [3, 5], [3, 3], [5, 3]]
cells = []


class Enemy:
    pos = 0   # ++ in every loop

    def __init__(self, hp, speed):
        self.hp = hp
        self.speed = speed

    def get_pos(self, road):
        half = self.pos/2
        whole = math.floor(half)
        if road[whole][1] == road[whole + 1][1]:
            if road[whole][0] < road[whole + 1][0]:
                return [road[whole][0] + (self.pos - 2*whole),    # Ak to nepojde asi je chyba tu
                        road[whole][1]]
            else:
                return [road[whole][0] - (self.pos - 2*whole),
                        road[whole][1]]
        else:
            if road[whole][1] < road[whole + 1][1]:
                return [road[whole][0],
                        road[whole][1] + (self.pos - 2*whole)]
            else:
                return [road[whole][0],
                        road[whole][1] - (self.pos - 2*whole)]


class Regular(Enemy):
    def __init__(self):
        Enemy.__init__(self, 100, 1)


class Cell:
    def __init__(self, pos, upgrades=0):
        self.pos = pos
        self.upgrades = upgrades
        self.tower = 0


class Basic:
    rng = 4
    dmg = 10
    atspd = 5
    rtspd = 90
    rtangl = 0
    prspd = 4

    @staticmethod
    def enemy_angle(enemy, cell):
        dx = cell.pos[0] - enemy.get_pos(road_g)[0]
        dy = cell.pos[1] - enemy.get_pos(road_g)[1]
        if dx == 0:
            if dy > 0:
                return 270
            else:
                return 90
        atan = math.degrees(math.atan(dy/dx))
        if dx < 0:
            if atan < 0:
                return 360 + atan
            else:
                return atan
        else:
            return 180 + atan

    def rtt(self, enangl):      # TODO: Optimalizuj
        if self.rtangl > enangl:
            if self.rtangl - enangl > 180:
                return 360 - (self.rtangl - enangl)
            else:
                return enangl - self.rtangl
        elif self.rtangl == enangl:
            return 0
        else:
            if self.rtangl - enangl < -180:
                return 360 + self.rtangl - enangl
            else:
                return self.rtangl - enangl


class Bullet:
    def __init__(self, dmg, t, host):
        self.dmg = dmg
        self.t = t
        self.host = host

    def update(self):
        self.t -= 1     # TODO: Set time delta based on tick time length
        if self.t <= 0:
            self.host.hp -= self.dmg
            return True
        return False
    # Return True if Bullet needs to be deleted


for i in range(1, 6):
    cells.append(Cell([1, 2*i+1]))
    cells.append(Cell([5, 2*i + 2]))


c = Cell([5, 5])
c.tower = Basic()
e = Regular()

for i in range(0, 15):
    e.pos = i
    print(e. get_pos(road_g))
    print(c.tower.rtt(Basic.enemy_angle(e, c)))
    print("")
