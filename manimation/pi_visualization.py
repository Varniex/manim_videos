# Pi Visualization
# Numberphile Video: https://youtu.be/NPoj8lk9Fo4
# Martin Krzywinski and Cristian Ilies Vasile: http://mkweb.bcgsc.ca/pi/art/
#
#
# Working of the formation of this code to make this Visualization:
# Step 1: Every digit of pi is connected to its next digit. Bezier curves are used
# to connect the corresponding numbered arcs.
# For ex: pi = 3.141 So, the bezier curve starts from the 3rd arc and ends on 1st arc.
# Next curve would start from 1st arc and goes to 4th arc

from manim import *
from mpmath import mp


# from https://stackoverflow.com/a/13316984
def get_n_digits_of_pi(n):
    mp.dps = n
    return [3] + [int(i) for i in list(str(mp.pi))[2:]]


class PiCircle(Scene):
    def construct(self):
        # some constants
        colors = [DARK_BROWN, ORANGE, PURPLE, LIGHT_PINK,
                  TEAL, BLUE, BLUE_E, BLUE_B, GREEN_E, GREEN_B]
        num_of_arcs = 10  # obviously
        offset = 5 * DEGREES  # space b/w two arcs
        radius = 3.5
        arc_length = (TAU / num_of_arcs) - offset
        pi_circle = VGroup()  # did this just to group everything

        pi = Tex("\\pi", font_size=72)
        pi_circle.add(pi)

        # position of numbers
        num_points = [
            np.array([(radius + 0.7) * np.sin(s),
                      (radius + 0.7) * np.cos(s), 0])
            for s in np.linspace(offset / 2 + arc_length / 2, TAU - arc_length / 2 - offset / 2, num_of_arcs)
        ]

        nums = VGroup(*[
            Tex(str(i), font_size=36) for i in range(num_of_arcs)
        ])

        for i, num in enumerate(nums):
            num.move_to(num_points[i])
        pi_circle.add(nums)

        # arc's start and end points as a tuple
        arcs_point = [
            (
                np.array([(radius + 0.3) * np.sin(s),
                          (radius + 0.3) * np.cos(s), 0]),
                np.array([(radius + 0.3) * np.sin(e),
                          (radius + 0.3) * np.cos(e), 0])
            )
            for s, e in zip(
                np.linspace(offset / 2, TAU - arc_length - offset / 2, num_of_arcs),
                np.linspace(arc_length + offset / 2, TAU - offset / 2, num_of_arcs)
            )
        ]

        arcs = VGroup(*[
            ArcBetweenPoints(
                p[0], p[1],
                color=colors[i],
                angle=-arc_length,
                stroke_width=20
            )
            for i, p in enumerate(arcs_point)
        ])
        pi_circle.add(arcs)

        # defining the start point of the bezier curves so they won't touch the arcs
        curve_points = [
            np.array([radius * np.sin(s), radius * np.cos(s), 0])
            for s in np.linspace(offset / 2, TAU - arc_length - offset / 2, num_of_arcs),
        ]

        # Step 2:
        # The position of the starting point of the bezier curve is same as the
        # position of the number in the digits of pi.
        # For ex: pi = 3.141
        # First curve starts from position one of 3rd arc and ends at position 2 of 1st arc.
        # Next curve starts from the point from previous curve ends and goes to 3rd position of
        # 4th arc.

        # I'm using SmallDot() or Dot() so that it is easily rotated to mark the position where the curve would end.
        curve_dots = [Dot(p) for p in curve_points]
        curve_dots1 = curve_dots.copy()
        curve_pointer = [0] * len(curve_dots)

        n = 3150  # number of digits of pi used
        pi_n = get_n_digits_of_pi(n)
        path = VGroup(stroke_width=2, stroke_opacity=0.05)  # another combination is 1, 0.1
        paths = VGroup()  # group of bezier curves
        len_of_arc = 360 / num_of_arcs - offset / DEGREES # length of arc in degrees

        for i in range(n - 1):
            new_path = path.copy()
            new_path.set_color_by_gradient([colors[pi_n[i]]])

            # hint for future reference
            # p0 = start point (current numbered arc)
            # p1 = end point (next numbered arc)
            # h = handle point (ORIGIN)

            # TODO: make better code

            p0 = curve_dots1[pi_n[i]].get_center()
            curve_pointer[pi_n[i + 1]] = -(0.01 * (i + 1) % len_of_arc) * DEGREES
            curve_dots1[pi_n[i + 1]] = curve_dots[pi_n[i + 1]].copy().rotate(
                curve_pointer[pi_n[i + 1]],
                about_point=ORIGIN
            )

            p1 = curve_dots1[pi_n[i + 1]].get_center()
            h = ORIGIN

            # here comes a little cheating
            # eliminating all curves which starts and ends at same numbered arcs
            # and which crosse ORIGIN.
            # TODO: think of a right way to bend the curve around ORIGIN more efficiently

            if pi_n[i] != pi_n[i + 1]:
                points = [bezier([p0, h, p1])(t) for t in np.linspace(0, 1, 3)]

                if round(points[1][0], ndigits=1) == 0.0 and round(points[1][1], ndigits=1) == 0.0:
                    points = [ORIGIN]
                new_path.set_points_smoothly(points)
            pi_circle.add(new_path)
            paths.add(new_path)

        # Here comes the amazing part: Animaaattiooooooon!!
        frame = self.camera.frame
        frame.set_width(2 * pi_circle.get_width())

        self.play(
            AnimationGroup(
                ShowCreation(arcs),
                Write(nums),
                lag_ratio=0.2
            ),
            run_time=5,
            rate_func=linear,
        )
        self.play(Write(pi), run_time=2)
        self.play(ShowCreation(paths), run_time=20, rate_func=linear)
        self.play(frame.animate.set_width(2 * pi.get_width()), run_time=3)
        self.wait()
