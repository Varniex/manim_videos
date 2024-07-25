# Varniex - CodingManim 05: Strange Attractors & Euler Angles
# YouTube Video: https://youtu.be/7-vAV9OZxLY

from manim_imports import *
from numpy import sin, cos, array
from scipy.integrate import solve_ivp


class MakingSpiral(Scene):
    def construct(self):
        spiral = ParametricCurve(
            t_func=lambda t: [sin(t), t / 7, cos(t)], t_range=[-2 * TAU, 2 * TAU, 0.01]
        )
        spiral.set_flat_stroke(False)
        self.play(Write(spiral))


class LorenzAttractorScene(Scene):
    pos = array([0.1, 0, 0])  # initial position
    num_points = int(1e4)
    sim_time = 50  # simulation time
    constants = (10, 28, 8 / 3)

    def construct(self):
        self.frame.reorient(45, 60, 0)

        lorenz_curve = self.get_lorenz_curve()
        lorenz_curve.set_width(FRAME_WIDTH / 2.5).center()
        lorenz_curve.set_color_by_gradient(DARK_BLUE, WHITE, DARK_BLUE)
        self.play(ShowCreation(lorenz_curve), run_time=self.sim_time)

    def get_lorenz_curve(self):
        pts = np.empty((self.num_points, 3))
        x, y, z = pts[0] = self.pos
        dt = self.sim_time / self.num_points

        for i in range(1, self.num_points):
            x_dot, y_dot, z_dot = self.update_curve(pos=(x, y, z))
            x += x_dot * dt
            y += y_dot * dt
            z += z_dot * dt
            pts[i] = array([x, y, z])

        curve = ParametricCurve(
            t_func=lambda i: pts[i], t_range=[0, self.num_points - 1, 1]
        ).set_flat_stroke(False)
        return curve

    def update_curve(self, t=None, pos=None):
        x, y, z = pos
        a, b, c = self.constants
        x_dot = a * (y - x)
        y_dot = x * (b - z) - y
        z_dot = x * y - c * z
        return array([x_dot, y_dot, z_dot])


class ImprovedLorenzAttractorScene(LorenzAttractorScene):
    def get_lorenz_curve(self):
        dt = self.sim_time / self.num_points

        solution = solve_ivp(
            fun=self.update_curve,
            t_span=(0.0, self.sim_time),
            y0=self.pos,
            dense_output=True,
        )

        curve = ParametricCurve(
            t_func=lambda t: solution.sol(t), t_range=(0, self.sim_time, dt)
        ).set_flat_stroke(False)
        return curve
