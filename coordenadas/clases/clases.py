import numpy as np
UNIT_TIME = 1


class Ship:
    def __init__(self, env, name, pos, vel, speed, destiny):
        self.env = env
        self.pos = pos
        self.name = name
        self.vel = vel
        self.speed = speed
        self.destiny = destiny
        self.action = env.process(self.drive())
        self.steps = []

    def drive(self):
        while True:
            print(f"{self.name}, posicion: {self.pos}; Tiempo simulacion {self.env.now}")
            self.steps.append(self.pos)
            yield self.env.process(self.update_pos(UNIT_TIME))

    def update_pos(self, time):
        yield self.env.timeout(time)
        self.pos += self.speed*self.vel
        if np.linalg.norm(self.pos - self.destiny) < 0.1:
            self.pos = self.destiny


class Port:
    def __init__(self, env, pos, capacity):
        self.pos = pos
        self.env = env
        self.capacity = capacity

    def start(self):
        yield 1
