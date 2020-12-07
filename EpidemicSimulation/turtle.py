import random
from enum import Enum
from math import sin, cos, pi

from config import *


class TurtleState(Enum):
    SUSCEPTIBLE = TURTLE_COLOR_SUSCEPTIBLE
    EXPOSED = TURTLE_COLOR_EXPOSED
    INFECTED = TURTLE_COLOR_INFECTED
    REMOVED = TURTLE_COLOR_REMOVED
    VACCINATED = TURTLE_COLOR_VACCINATED


class Turtle:
    def __init__(self, pos_x, pos_y, angle, velocity, state=TurtleState.SUSCEPTIBLE, vaccination_readiness=True,
                 responds_to_vaccination=True):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.angle = angle
        self.velocity = velocity
        self.state = state
        self.vaccination_readiness = vaccination_readiness
        self.responds_to_vaccination = responds_to_vaccination

        self.ticks_until_infectious = INCUBATION_PERIOD
        self.ticks_until_removed = DURATION_OF_INFECTION

    def update(self):
        self.angle += MAX_WIGGLE_ANGLE / 360 * random.random()
        self.angle -= MAX_WIGGLE_ANGLE / 360 * random.random()

        self.angle %= 2 * pi

        self.pos_x += cos(self.angle) * self.velocity
        self.pos_y += sin(self.angle) * self.velocity

        self.pos_x %= WIDTH
        self.pos_y %= HEIGHT

        if self.state == TurtleState.EXPOSED:
            self.ticks_until_infectious -= 1

            if self.ticks_until_infectious <= 0:
                self.state = TurtleState.INFECTED

        elif self.state == TurtleState.INFECTED:
            self.ticks_until_removed -= 1

            if self.ticks_until_removed <= 0:
                self.state = TurtleState.REMOVED

    def __str__(self):
        return 'x: ' + str(self.pos_x) + ' y: ' + str(self.pos_y)
