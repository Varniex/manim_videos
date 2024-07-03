# Varniex - CodingManim 03: Mastering the Graphs & Coordinate System
# YouTube Video: https://youtu.be/KFsYpc_pgh4


from manim_imports import *
from numpy import sin, cos, tan


def get_slope_of_tangent(t, graph):
    p0 = graph.get_function()(t)
    p1 = graph.get_function()(t + EPSILON)
    return tan(angle_of_vector([EPSILON, p1 - p0]))


class RosePatternWithParametricCurve(ParametricCurve):
    def __init__(
        self,
        radius: float = 2,
        k: float = 10,
        theta_range: float = TAU,
        step_size: float = 0.05,
        **kwargs,
    ):
        self.radius = radius
        self.k = k
        super().__init__(
            t_func=lambda t: [
                radius * cos(k * t) * cos(t),
                radius * cos(k * t) * sin(t),
                0,
            ],
            t_range=(0, theta_range + step_size, step_size),
            **kwargs,
        )


class ParametricCurveExample(Scene):
    def construct(self):
        step_func = ParametricCurve(
            lambda t: [t, 0 if t < 0 else 1, 0],
            t_range=[-5, 5, 0.1],
            discontinuities=[0],
        )
        self.play(ShowCreation(step_func))


class ParametricSinCurve(Scene):
    def construct(self):
        sin_curve = ParametricCurve(
            t_func=lambda t: [t, sin(t), 0], t_range=[-PI, PI, 0.1]
        )
        sin_curve.set_color(YELLOW)
        self.play(ShowCreation(sin_curve))


class GroupingObjects(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        hexagon = RegularPolygon(6)
        star = Star(5).scale(0.7)

        shapes = VMobject()
        shapes.add(circle, square, hexagon, star)
        shapes.scale(0.75)
        shapes.set_stroke(WHITE)
        shapes.set_color_by_gradient(BLUE, RED, YELLOW, PINK)

        self.play(ShowCreation(shapes))

        # VGroup
        shapes_vgroup = VGroup(circle, square, hexagon, star)
        shapes_vgroup.arrange(RIGHT, buff=2)
        shapes_vgroup.set_stroke(YELLOW, width=8)


class FunctionGraphExample(Scene):
    def construct(self):
        sin_curve = FunctionGraph(sin).set_color(BLUE)
        cos_curve = FunctionGraph(cos).set_color(RED)
        parabola = FunctionGraph(lambda x: x**2).set_color(YELLOW)
        cubic = FunctionGraph(lambda x: x**3).set_color(PINK)
        relu = FunctionGraph(lambda x: max(0, x)).set_color(TEAL)

        self.play(ShowCreation(sin_curve))
        self.play(ReplacementTransform(sin_curve, cos_curve))
        self.play(ReplacementTransform(cos_curve, parabola))
        self.play(ReplacementTransform(parabola, cubic))
        self.play(ReplacementTransform(cubic, relu))


class IntroToAxes(Scene):
    def construct(self):
        axes = Axes(
            x_range=(-5, 5, 1), y_range=(-3, 3, 1), axis_config=dict(include_tip=True)
        )
        axes.add_coordinate_labels()
        axes_labels = axes.get_axis_labels()
        self.play(ShowCreation(axes), Write(axes_labels))

        sin_curve = axes.get_graph(sin)
        sin_curve.set_color(YELLOW)
        self.play(ShowCreation(sin_curve))


class DistanceTimeGraph(Scene):
    def construct(self):
        axes = Axes(
            x_range=(0, 7, 1),
            y_range=(0, 25, 3),
            height=6,
            axis_config=dict(include_tip=True),
        )
        axes.add_coordinate_labels()
        axes_labels = axes.get_axis_labels("t", "x(t)")
        self.play(ShowCreation(axes), Write(axes_labels))

        dist_graph = axes.get_graph(
            function=lambda t: t**2 if t < 3 else 6 * t - 9, x_range=(0, 5)
        ).set_color(BLUE)
        self.play(ShowCreation(dist_graph))

        tangent = axes.get_tangent_line(2.5, dist_graph)
        self.play(ShowCreation(tangent))

        vel_graph = axes.get_graph(
            lambda t: 2 * t if t < 3 else 6, x_range=(0, 5)
        ).set_color(RED)
        self.play(ShowCreation(vel_graph))

        dist_label = axes.get_graph_label(dist_graph, "x(t)")
        vel_label = axes.get_graph_label(vel_graph, "v(t)")
        self.play(
            Write(dist_label),
            Write(vel_label),
            FadeOut(axes_labels[1]),
            FadeOut(tangent),
        )

        ## Code to sweep tangent from t = 0 to t = 5 secs

        # very helpful to access dot coords at any time (t).
        # dot coords: (time coord, slope of tangent at that time)
        def get_dot_coords():
            return axes.c2p(
                t := t_coord.get_value(), get_slope_of_tangent(t, dist_graph)
            )

        # time coordinate tracker
        t_coord = ValueTracker(0)
        tangent = always_redraw(
            lambda: axes.get_tangent_line(t_coord.get_value(), dist_graph, length=2)
        )

        dot = Dot(fill_color=YELLOW)
        dot.f_always.move_to(get_dot_coords)

        h_line = always_redraw(lambda: axes.get_h_line(dot.get_center()))
        v_line = always_redraw(lambda: axes.get_v_line(dot.get_center()))

        self.add(h_line, v_line)
        self.play(ShowCreation(dot), ShowCreation(tangent))
        self.wait()
        self.play(
            t_coord.animate.set_value(5),
            run_time=5,
            rate_func=there_and_back,
        )

        area = axes.get_area_under_graph(
            graph=vel_graph, x_range=(2, 4), fill_color=RED  # fill_opacity=0.5
        )
        self.play(ShowCreation(area))
        self.wait()
