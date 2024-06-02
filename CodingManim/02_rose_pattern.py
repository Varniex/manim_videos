# Varniex - CodingManim 02: The Magic Of Updaters
# YouTube Video: https://youtu.be/3Duf3g_Wkqs

from manimlib import *
from numpy import cos, sin, arange


def get_rose_pattern(k, colors=[BLUE, WHITE, BLUE]):
    return RosePattern(k=k).set_color_by_gradient(*colors)


class DynamismToObjects(Scene):
    def construct(self):
        sq = Square()
        sq.set_fill(TEAL, opacity=0.5)
        sq.move_to(2.5*LEFT)

        circle = Circle()
        circle.set_fill(RED, opacity=0.5)

        self.play(DrawBorderThenFill(sq))

        self.play(sq.animate.move_to(ORIGIN))
        # or self.play(sq.animate.shift(2.5 * RIGHT))
        self.play(sq.animate.rotate(45 * DEGREES))
        self.play(sq.animate.scale(2))

        self.play(sq.animate.become(circle))


class UpdaterTemplate(Scene):
    def construct(self):
        mobject = Circle()

        def update_mobject(mob, dt):
            # define some set of rules
            ...

        mobject.add_updater(update_mobject)
        self.wait()


class UpdaterExample(Scene):
    def construct(self):
        sq = Square().set_fill(TEAL, 0.5)
        sq.to_edge(LEFT, buff=1)
        sq.rotate(45 * DEGREES)

        def update_square(s):
            s.shift(0.05 * RIGHT)
            s.rotate(-2 * DEGREES)

        self.play(ShowCreation(sq))
        sq.add_updater(update_square)
        self.wait(5)


class UpdaterExample2(Scene):
    def construct(self):
        sq = Square()
        sq.set_fill(TEAL, 0.5)
        sq.to_edge(LEFT, buff=1)
        sq.rotate(45 * DEGREES)

        circle = Circle().set_fill(RED, 0.5)
        circle.next_to(sq, DOWN, buff=0.5)

        def update_square(s):
            s.shift(0.05 * RIGHT)
            # s.rotate(-2 * DEGREES)
            s.set_width(abs(2 * sin(self.time)))

        self.play(ShowCreation(sq), FadeIn(circle))
        sq.add_updater(update_square)
        circle.always.next_to(sq, DOWN, buff=0.5)
        circle.f_always.set_width(sq.get_width)

        self.wait(10)


class BouncingBall(Scene):
    def construct(self):
        width = 12
        height = 6
        box = Rectangle(width=width, height=height)
        box.set_stroke(width=8)

        ball = Dot(radius=0.15)
        ball.vx, ball.vy = 0.05, 0.05

        def update_circle(c):
            right_point = c.get_right()[0]
            left_point = c.get_left()[0]
            top_point = c.get_top()[1]
            bottom_point = c.get_bottom()[1]

            if right_point >= width/2 or left_point <= -width/2:
                c.vx *= -1
            if top_point >= height/2 or bottom_point <= -height/2:
                c.vy *= -1

            c.shift(c.vx * RIGHT + c.vy * UP)

        self.play(ShowCreation(ball), ShowCreation(box))
        ball.add_updater(update_circle)
        self.wait(5)


class RosePattern(VMobject):
    def __init__(self, radius: float = 2, k: float = 3, theta_range=TAU, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.k = k

        step_size = 0.05
        theta = arange(0, theta_range + step_size, step_size)

        points = [
            [
                radius * cos(k * t) * cos(t),
                radius * cos(k * t) * sin(t),
                0
            ] for t in theta
        ]

        self.set_points_smoothly(points)


class ShowingRosePattern(Scene):
    def construct(self):

        rose = RosePattern(k=10)

        self.play(ShowCreation(rose), run_time=5)
        self.wait()


class AnimatingWithUpdateFunc(Scene):
    def construct(self):
        rose = get_rose_pattern(k=0)
        rose.k = 0

        self.play(ShowCreation(rose))

        def update_pattern(pat, dt):
            pat.k += dt
            new_pat = get_rose_pattern(k=pat.k)
            pat.become(new_pat)

        rose.add_updater(update_pattern)
        self.wait(10)


class AnimatingWithValueTracker(Scene):
    def construct(self):
        track_k = ValueTracker(0)
        rose = get_rose_pattern(k=track_k.get_value())

        self.play(ShowCreation(rose))

        def update_pattern(pat):
            new_pat = get_rose_pattern(k=track_k.get_value())
            pat.become(new_pat)

        rose.add_updater(update_pattern)
        self.play(
            track_k.animate.set_value(10),
            run_time=5
        )


class AnimatingWithValueTracker2(Scene):
    def construct(self):
        track_k = ValueTracker(0)
        rose = get_rose_pattern(k=track_k.get_value())

        self.play(ShowCreation(rose))

        # UpdateFromFunc is same as f_always
        self.play(
            UpdateFromFunc(
                rose, lambda pat: pat.become(
                    get_rose_pattern(k=track_k.get_value())
                )
            ),
            track_k.animate.set_value(10),
            run_time=5
        )


class AnimatingWithForLoop(Scene):
    def construct(self):
        rose = get_rose_pattern(k=0)
        self.play(ShowCreation(rose))

        k_increment = 0.01

        for k in arange(0, 10, k_increment):
            self.play(
                rose.animate.become(get_rose_pattern(k)),
                run_time=k_increment
            )


class RosePatternNutshell(Scene):
    def construct(self):
        grps = VGroup()  # as there are going to be groups of Texs and RosePatterns
        texs = VGroup()
        patterns = VGroup()
        num = 7  # intended to be a square
        offset = 2.3  # controls the spacing between the elements

        frame = self.camera.frame

        for n in range(num + 1):
            for d in range(num + 1):
                if n == 0 and d == 0:
                    tex = Tex("k = \\displaystyle\\frac{n}{d}", font_size=25)
                    grps.add(tex)
                    texs.add(tex)
                if n == 0 and d != 0:
                    tex = Tex(f"d = {d}", font_size=25)
                    grps.add(tex)
                    texs.add(tex)
                if n != 0 and d == 0:
                    tex = Tex(f"n = {n}", font_size=25)
                    grps.add(tex)
                    texs.add(tex)
                if n != 0 and d != 0:
                    pattern = RosePattern(
                        k=n / d,
                        radius=frame.get_width() / (2 * offset * (num + 1)),
                        theta_range=TAU * num
                    )
                    grps.add(pattern)
                    patterns.add(pattern)

        colors = [ORANGE, TEAL, BLUE, GREEN, RED, MAROON, PINK]

        grps.arrange_in_grid(fill_rows_first=False)
        patterns.set_color_by_gradient(*colors)
        texs.set_color_by_gradient(*colors)

        self.play(*[Write(tex) for tex in texs])
        self.play(
            *[ShowCreation(pattern) for pattern in patterns],
            run_time=8,
            rate_func=linear
        )
        self.wait()
