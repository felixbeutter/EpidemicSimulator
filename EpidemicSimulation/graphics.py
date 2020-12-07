import os
import re
import glob
import cv2
import shutil
import pygame
import matplotlib.pyplot as plt

from config import *


def plot_results(results):
    print('Generating plot and writing it to file...', end=' ')

    plt.plot(results)
    plt.xlabel('Days')
    plt.ylabel('Fraction of all turtles (in %)')

    ax = plt.gca()

    lines = ax.get_lines()
    lines[0].set_color('#007AB8')
    lines[1].set_color('#FFB30F')
    lines[2].set_color('#FF4000')
    lines[3].set_color('#63B42D')
    lines[4].set_color('#808080')
    plt.legend(lines, ['Susceptible', 'Exposed', 'Infected', 'Vaccinated', 'Removed'])

    positions, _ = plt.xticks()
    plt.xticks(positions[1:][:-1], [int(position) // 10 for position in positions][1:][:-1])

    positions, _ = plt.yticks()
    plt.yticks(positions[1:][:-1], [int((int(position) / NUM_TURTLES) * 100) for position in positions][1:][:-1])

    plt.savefig('results/plot.png', dpi=300)
    print('done')

    plt.show()


def convert_frames_to_video():
    print('Generating video of simulation, this may take a while...', end=' ')
    frame_files = [file for file in os.listdir('tmp') if file.startswith('frame')]

    # sort file names by alphabetical and numerical order
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    sorted_frame_files = sorted(frame_files, key=alphanum_key)

    # define video properties (width, height, etc.)
    first_frame_file = cv2.imread(os.path.join('tmp', sorted_frame_files[0]))
    height, width, layers = first_frame_file.shape

    # generate video and write it to file
    video = cv2.VideoWriter('results/simulation.mp4', cv2.VideoWriter_fourcc(*'mp4v'), VIDEO_FPS, (width, height))

    for file in sorted_frame_files:
        video.write(cv2.imread(os.path.join('tmp', file)))

    cv2.destroyAllWindows()
    video.release()

    # delete tmp folder containing individual frames
    shutil.rmtree('tmp', ignore_errors=True)
    print('done')


class Window:
    def __init__(self, title, display_size, patch_width, turtle_diameter, background_color):
        self.patch_width = patch_width
        self.turtle_diameter = turtle_diameter
        self.background_color = background_color

        pygame.display.set_caption(title)

        self.display = pygame.display.set_mode(display_size)
        self.display.fill(background_color)

        # if video generation is enabled, create 'tmp' directory to save individual frames to
        if SAVE_SIMULATION_AS_VIDEO:
            self.frame = 0

            try:
                os.mkdir('tmp')
            except FileExistsError:
                files = glob.glob('tmp/*')

                for file in files:
                    os.remove(file)

    def draw_turtle(self, turtle):
        x, y = turtle.pos_x, turtle.pos_y
        pygame.draw.circle(self.display, turtle.state.value, (x * self.patch_width, y * self.patch_width),
                           self.turtle_diameter / 2)

    def update(self, turtles):
        self.display.fill(self.background_color)

        for turtle in turtles:
            self.draw_turtle(turtle)

        pygame.display.flip()

        # if video generation is enabled, save screenshot to 'tmp' directory
        if SAVE_SIMULATION_AS_VIDEO:
            pygame.image.save(self.display, 'tmp/frame_' + str(self.frame) + '.png')
            self.frame += 1
