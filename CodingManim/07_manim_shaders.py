# Varniex - CodingManim 07: Manim - Shaders Integration
# YouTube Video: https://youtu.be/hdg69DV5yII

from manim_imports import *


class ShaderDemonstration(ShaderScene):
    """
    To refresh the canvas, execute the either command:

    1. `self.refresh_shader()` -> update the recent changes.
    2. `self.refresh_and_hold()` -> update changes in a loop.

    in the IPython console.

    => Press <spacebar> (when Manim Window is focused)
       to exit from the 'wait' loop.
    """

    shader_folder = "my_first_shader"

    def construct(self):
        # This is necessary to enable embed mode
        # or use self.embed()
        pass
