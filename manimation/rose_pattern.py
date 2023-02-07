# Rose Pattern
# Wikipedia: https://en.wikipedia.org/wiki/Rose_(mathematics)

from manim_imports import *

class RosePattern(VMobject):
    CONFIG = {
        "k": 3,  # n / d
        "step_size": 0.05,  # step change in polar angle
        "theta": 2 * PI,
        "radius": 2,  # amplitude
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        theta = np.arange(0, self.theta + self.step_size, self.step_size)

        # Equations:
        # x = a * cos(k * theta) * cos(theta)
        # y = a * cos(k * theta) * sin(theta)
        points = [
            np.array([
                self.radius * np.cos(self.k * t) * np.cos(t),
                self.radius * np.cos(self.k * t) * np.sin(t),
                0
            ]) for t in theta
        ]
        self.set_points_smoothly(points)

class DrawRosePattern(Scene):
    CONFIG = {
        "k": 10
    }

    def construct(self):
        pattern = RosePattern(k=self.k)
        pattern.set_color_by_gradient([WHITE, BLUE_D, WHITE])
        self.play(
            ShowCreation(pattern),
            run_time=5,
            rate_func=linear
        )
        self.wait()

class RosePatternNutshell(Scene):
    CONFIG = {
        "num": 7,  # intended to be a square
        "offset": 2.3,  # controls the spacing between the elements
    }

    def construct(self):
        grps = VGroup()  # as there are going to be groups of Texs and RosePatterns
        texs = VGroup()
        patterns = VGroup()

        frame = self.camera.frame

        for n in range(self.num + 1):
            for d in range(self.num + 1):
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
                        radius=frame.get_width() / (2 * self.offset * (self.num + 1)),
                        theta=2 * self.num * PI
                    )
                    grps.add(pattern)
                    patterns.add(pattern)

        colors = [ORANGE, TEAL, BLUE, GREEN, RED, MAROON, VIOLET, PINK]

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

if __name__ == '__main__':
    render_scene(RosePatternNutshell)
