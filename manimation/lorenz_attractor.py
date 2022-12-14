# Lorenz Attractor
# Wikipedia: https://en.wikipedia.org/wiki/Lorenz_system

from manim import *
from scipy.integrate import odeint


class LorenzSystem(VMobject):
    CONFIG = {
        "sigma": 10.0,
        "rho": 28.0,
        "beta": 8.0 / 3.0,
        "position": np.array([0.1, 0, 0]),  # initial conditions
        "max_time": 50.0,  # max simulation time
        "speed": 2,  # speed of the simulation
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        t_range = np.arange(0.0, self.speed * self.max_time, 0.01)
        self.positions = odeint(self.update_position, self.position, t_range)  # from wikipedia
        self.set_points_smoothly(self.positions)

    def update_position(self, position, t):
        x, y, z = position

        x_dot = self.sigma * (y - x)
        y_dot = x * (self.rho - z) - y
        z_dot = x * y - self.beta * z

        return np.array([x_dot, y_dot, z_dot])

    def get_positions(self):
        return self.positions


class LorenzAttractor(Scene):
    def construct(self):
        max_time = 40.0
        colors = [WHITE, BLUE_D, WHITE]

        lorenz = LorenzSystem(max_time=max_time)
        lorenz.set_color_by_gradient(colors)
        lorenz.set_width(FRAME_WIDTH / 2.5)

        frame = self.camera.frame
        frame.move_to(lorenz.get_center())
        frame.set_euler_angles(theta=45 * DEGREES, phi=55 * DEGREES)
        frame.save_state()

        self.play(
            ShowCreation(lorenz),
            frame.animate.increment_theta(-500 * DEGREES),
            run_time=max_time,
            rate_func=linear
        )
        self.play(
            frame.animate.restore(),
            run_time=4,
            rate_func=smooth
        )
        self.wait()
