# Varniex - CodingManim: Installation and Testing of Manim
# YouTube Video: https://youtu.be/FlFEpb5GlZk

# Importing the ManimGL library
from manimlib import *


class SquareToCircle(Scene):
    def construct(self):
        # This is where the magic lies!
        # Defining the square
        sq = Square()
        sq.set_fill(TEAL, 0.5)  # giving the color and opacity
        sq.rotate(45 * DEGREES)

        # self.add(sq)

        # `play` method gives the animation with run_time (default to 1 sec)
        self.play(DrawBorderThenFill(sq), run_time=1)

        circle = Circle()
        circle.set_fill(BLUE, 0.5)

        self.play(Transform(sq, circle))
