# Varniex - CodingManim 01: Getting Started with the Basics
# YouTube Video: https://youtu.be/E8BgxjKfxcI

# Importing the ManimGL library
from manimlib import *


class MakingSquare(Scene):
    def construct(self):
        # Instantiating the variable
        sq = VMobject()

        # defining the coords of the points
        points = [
            [1, 1, 0],
            [1, -1, 0],
            [-1, -1, 0],
            [-1, 1, 0],
        ]

        # To help in visualization in the Canvas
        dots = VGroup(*[Dot(p) for p in points])
        self.add(dots)

        sq.set_points_as_corners(points)
        self.play(ShowCreation(sq), run_time=2)

        # To make a closed square, we need to add this point as the fifth element
        sq.add_points_as_corners([[1, 1, 0]])
        sq.make_smooth()

        # Experiment more. Go creative!!

        #   .set_points_as_corners
        # + .make_smooth
        # = .set_points_smoothly
