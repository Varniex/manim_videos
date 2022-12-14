# Times Table
# Mathologer's video: https://youtu.be/qhbuKbxJsk8

from manim import *


class TimesTable(VMobject):
    CONFIG = {
        "m": 2,  # multiplication factor
        "n": 200,  # number of lines
        "stroke_width": 1.5,  # stroke width of lines, circle
        "radius": 2.5,  # radius of circle
        "colors": [BLUE_D, WHITE, BLUE_D]  # color of lines
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.circle = Circle(
            radius=self.radius,
            stroke_width=self.stroke_width * 2
        )
        self.lines = self.get_lines()

        self.add(self.lines, self.circle)

    def get_lines(self):
        r = self.radius
        cos = np.cos
        sin = np.sin
        m = self.m
        return VGroup(*[
            Line(
                (r * cos(theta), r * sin(theta), 0),
                (r * cos(m * theta), r * sin(m * theta), 0),
                stroke_width=self.stroke_width
            )
            for theta in np.linspace(0, TAU, self.n)
        ]).set_color_by_gradient(*self.colors)


class TimesTableScene(Scene):
    def construct(self):
        max_factor = 10
        axes = Axes()
        axes.set_height(self.camera.get_frame_height())
        labels = axes.get_axis_labels()

        text, factor = factor_is = VGroup(
            TexText("Factor = "),
            DecimalNumber(0, num_decimal_places=0, font_size=30)
        )
        factor_is.arrange(RIGHT)
        factor_is.move_to(np.array([4, 3, 0]))

        self.play(
            ShowCreation(axes),
            Write(labels),
            Write(factor_is)
        )

        factor_tracker = ValueTracker()
        f_always(factor.set_value, factor_tracker.get_value)

        def create_and_remove_lines(lines):
            self.play(*[
                ShowCreation(line) for line in lines
            ], rate_func=linear)
            self.wait()
            self.remove(*[line for line in lines])

        self.table = TimesTable(m=0)
        self.play(ShowCreation(self.table.circle))
        create_and_remove_lines(self.table.lines)

        for i in range(2, max_factor):
            factor_tracker.set_value(i)
            self.table = TimesTable(m=i)
            create_and_remove_lines(self.table.lines)

        self.add(self.table)

        def update_table(table):
            new_table = TimesTable(m=factor_tracker.get_value())
            table.become(new_table)

        factor.num_decimal_places = 2

        self.table.add_updater(update_table)
        self.play(
            factor_tracker.animate.set_value(0),
            run_time=max_factor * 1.5,
            rate_func=linear
        )
        self.wait()
        self.play(*[Uncreate(m) for m in self.mobjects])
