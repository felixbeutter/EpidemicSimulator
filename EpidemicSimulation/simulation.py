import glob
import math
import os
from random import random

import pygame

from config import *
from graphics import Window, plot_results, convert_frames_to_video
from turtle import Turtle, TurtleState

"""
    initialization
"""

# initialize pygame
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

pygame.init()
clock = pygame.time.Clock()

# Create simulation gui
window = Window(
    title='Epidemic Simulator',
    display_size=(WIDTH * PATCH_WIDTH, HEIGHT * PATCH_WIDTH),
    patch_width=PATCH_WIDTH,
    turtle_diameter=TURTLE_DIAMETER,
    background_color=BACKGROUND_COLOR
)

# create and configure turtles
turtles = []

for i in range(NUM_TURTLES):
    turtles.append(Turtle(
        pos_x=random() * WIDTH,
        pos_y=random() * HEIGHT,
        angle=2 * math.pi * random(),
        velocity=TURTLE_VELOCITY,
        state=TurtleState.INFECTED if i < INITIAL_INFECTED_TURTLES else TurtleState.SUSCEPTIBLE,
        vaccination_readiness=True if random() * 100 < VACCINATION_READINESS else False,
        responds_to_vaccination=True if random() * 100 < VACCINATION_EFFECTIVENESS else False
    ))

# adjust duration of infection for infected turtles, so that not all of the initial infected one are recovered at the
# same time
for turtle in turtles:
    if turtle.state == TurtleState.INFECTED:
        turtle.ticks_until_removed = int(random() * DURATION_OF_INFECTION)

# global variables definition
results = []  # each tick, the fraction of susceptible, infected, etc. turtles is save for evaluation
vaccinations = False
num_to_vaccinate = 0  # number of turtle# s to vaccinate next tick

tick = 0

"""
    simulation loop
"""
while True:
    # add current turtle fractions to results list for evaluation
    # fractions are sorted by 'susceptible', 'infected', 'vaccinated' and 'removed'
    fractions = []

    for state in [TurtleState.SUSCEPTIBLE, TurtleState.EXPOSED, TurtleState.INFECTED, TurtleState.VACCINATED,
                  TurtleState.REMOVED]:
        fractions.append([t for t in turtles if t.state == state])

    results.append([len(fraction) for fraction in fractions])

    # break simulation loop if no turtle is infected or exposed anymore
    if len(fractions[1]) + len(fractions[2]) == 0:
        break

    # update each turtle's position, angle and state
    for turtle in turtles:
        turtle.update()

    # vaccinate turtles
    if vaccinations:
        vaccinable_turtles = [i for i, turtle in enumerate(turtles) if
                              turtle.state == TurtleState.SUSCEPTIBLE and turtle.vaccination_readiness]
        num_to_vaccinate += VACCINATIONS_PER_TICK

        for i in range(min(int(num_to_vaccinate // 1), len(vaccinable_turtles))):
            turtles[vaccinable_turtles[i]].state = TurtleState.VACCINATED

        num_to_vaccinate %= 1

    else:
        # check if start condition for vaccinations is met
        if len(fractions[2]) / len(turtles) * 100 > VACCINATION_START:
            vaccinations = True

    # determine infection process (which turtles are infected by which turtles)
    sorted_turtles_by_x = sorted(turtles, key=lambda t: t.pos_x)
    sorted_turtles_by_y = sorted(turtles, key=lambda t: t.pos_y)

    for turtle in fractions[2]:
        if random() * 100 > INFECTIOUS_TICK_PROB:
            continue

        # determine turtle neighbors in infection radius depending on x-pos
        x_neighbours = []

        x_index = sorted_turtles_by_x.index(turtle)
        i = x_index - 1

        while i >= 0:
            if abs(sorted_turtles_by_x[i].pos_x - turtle.pos_x) > INFECTION_RADIUS:
                break

            x_neighbours.append(sorted_turtles_by_x[i])
            i -= 1

        i = x_index + 1

        while i < len(turtles):
            if abs(sorted_turtles_by_x[i].pos_x - turtle.pos_x) > INFECTION_RADIUS:
                break

            x_neighbours.append(sorted_turtles_by_x[i])
            i += 1

        # determine turtle neighbors in infection radius depending on y-pos
        y_neighbours = []

        y_index = sorted_turtles_by_y.index(turtle)
        i = y_index - 1

        while i >= 0:
            if abs(sorted_turtles_by_y[i].pos_y - turtle.pos_y) > INFECTION_RADIUS:
                break

            y_neighbours.append(sorted_turtles_by_y[i])
            i -= 1

        i = y_index + 1

        while i < len(turtles):
            if abs(sorted_turtles_by_y[i].pos_y - turtle.pos_y) > INFECTION_RADIUS:
                break

            y_neighbours.append(sorted_turtles_by_y[i])
            i += 1

        # filter actual neighbors by determining the intersection of x and y neighbours
        neighbours = set(x_neighbours).intersection(set(y_neighbours))

        # filter neighbours which are not in the infection radius
        turtles_in_infection_radius = []

        for neighbour in neighbours:
            distance = math.sqrt((neighbour.pos_x - turtle.pos_x) ** 2 + (neighbour.pos_y - turtle.pos_y) ** 2)
            too_far = distance > INFECTION_RADIUS

            if not too_far:
                if neighbour.state == TurtleState.SUSCEPTIBLE or \
                        (neighbour.state == TurtleState.VACCINATED and not neighbour.responds_to_vaccination):
                    turtles_in_infection_radius.append(neighbour)

        # infect susceptible turtles in infection radius by given probability
        for exposed_turtle in turtles_in_infection_radius:
            if random() * 100 < INFECTION_PROB:
                exposed_turtle.state = TurtleState.EXPOSED

    # update gui
    window.update(turtles)

    # exit if window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # print stats
    if tick % 10 == 0:
        print('\nDAY:', int(tick / 10) + 1)
        print('susceptible:', len(fractions[0]), ', exposed:', len(fractions[1]), ', infected:', len(fractions[2]),
              ', vaccinated:', len(fractions[3]), ', removed:', len(fractions[4]))

    clock.tick(MAX_SIMULATION_FPS)
    tick += 1

pygame.quit()

# write results (plot and possibly video) to file
try:
    os.mkdir('results')
except FileExistsError:
    files = glob.glob('results/*')

    for file in files:
        os.remove(file)
finally:
    if SAVE_SIMULATION_AS_VIDEO:
        convert_frames_to_video()

    plot_results(results)
