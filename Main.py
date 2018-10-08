coins = 200
road = []
cells = []


class Enemy:
    pos = [1.5, 0.5]

    def __init__(self, hp, speed):
        self.hp = hp
        self.speed = speed


class Regular(Enemy):
    def __init__(self):
        Enemy.__init__(self, 100, 0.5)


class Cell:
    def __init__(self, pos, upgrades=0):
        self.pos = pos
        self.upgrades = upgrades
        self.tower = 0


class Basic:
    rng = 2
    dmg = 10
    atspd = 5
    rtspd = 90
    prspd = 1


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
    cells.append(Cell([0.5, i+0.5]))
    cells.append(Cell([2.5, i + 0.5]))
