"""
    Parameter configuration for the simulation
"""

"""
    Size of the simulated world
"""
WIDTH, HEIGHT = 10, 10  # in patches
PATCH_WIDTH = 100  # in pixels

"""
    Color properties (colors are defined through (R, G, B) tuples)
"""
BACKGROUND_COLOR = (0, 0, 0)
TURTLE_COLOR_SUSCEPTIBLE = (0, 122, 184)
TURTLE_COLOR_EXPOSED = (255, 179, 15)
TURTLE_COLOR_INFECTED = (255, 64, 0)
TURTLE_COLOR_VACCINATED = (99, 180, 45)
TURTLE_COLOR_REMOVED = (128, 128, 128)

"""
    Turtle properties
"""
TURTLE_DIAMETER = 5  # in pixels
TURTLE_VELOCITY = .01  # in patches per tick
MAX_WIGGLE_ANGLE = 180  # in degree per tick
NUM_TURTLES = 10000

"""
    Characteristics of the infection process
"""
INFECTION_PROB = 5  # in percent
INFECTION_RADIUS = .1  # in patches
DURATION_OF_INFECTION = 200  # in ticks
INITIAL_INFECTED_TURTLES = 40
INFECTIOUS_TICK_PROB = 5  # in percent
INCUBATION_PERIOD = 50  # in ticks

"""
    Vaccination simulation properties
"""
VACCINATION_START = 0  # in percent of infected turtles
VACCINATIONS_PER_TICK = 1.25  # in turtles
VACCINATION_EFFECTIVENESS = 95  # in percent
VACCINATION_READINESS = 60  # in percent

"""
    Graphics properties
"""
MAX_SIMULATION_FPS = 0  # set 0 for fastest simulation
SAVE_SIMULATION_AS_VIDEO = True  # write video of simulation to file
VIDEO_FPS = 60  # frames per second for video encoding
