coins = 200


class Enemy:
    pos = [1.5, 0.5]

    def __init__(self, hp, speed):
        self.hp = hp
        self.speed = speed


class Regular(Enemy):
    def __init__(self):
        Enemy.__init__(self, 100, 0.5)

