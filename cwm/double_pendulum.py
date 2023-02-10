# Double Pendulum
#
# Note: The code below is really scrappy!
#
# The Coding Train's Double Pendulum: https://youtu.be/uWzPe_S-RVE
# myPhysicsLab Double Pendulum: https://www.myphysicslab.com/pendulum/double-pendulum-en.html

from manim_imports import *
from manimation.pendulum_chaos import Pendulum


class DoublePendulum(VMobject):
    CONFIG = {
        "g": 9.8,
        "origin": ORIGIN,
        "theta1": 0,
        "theta2": 0,
        "omega1": 0,
        "omega2": 0,

        "rod1_config": {
            "length": 2,
            "color": WHITE,
            "stroke_width": 1.5,
        },
        "rod2_config": {
            "length": 2,
            "color": WHITE,
            "stroke_width": 1.5,
        },
        "bob1_config": {
            "mass": 0.1,
            "radius": 0.1,
            "color": WHITE,
            "fill_opacity": 1
        },
        "bob2_config": {
            "mass": 0.1,
            "radius": 0.1,
            "color": WHITE,
            "fill_opacity": 1
        },
        "speed": 1,
        "show_trail": True,
        "trail_length": 30,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pendulum1 = Pendulum(
            origin=self.origin,
            theta=self.theta1,
            omega=self.omega1,
            rod_config=self.rod1_config,
            bob_config=self.bob1_config,
        )
        self.pendulum2 = Pendulum(
            origin=self.pendulum1.bob.get_center(),
            theta=self.theta2,
            omega=self.omega2,
            rod_config=self.rod2_config,
            bob_config=self.bob2_config,
        )

        self.dp = VGroup(self.pendulum2, self.pendulum1)
        self.add(
            self.pendulum2.rod,
            self.pendulum2.bob,
            self.pendulum1.rod,
            self.pendulum1.bob,
        )

        if self.show_trail:
            self.path = VGroup(color=self.bob2_config["color"])
            self.trail_path = []
            self.add(self.path)

    def start_swinging(self):
        self.add_updater(self.update_pendulum)

    def stop_swinging(self):
        self.remove_updater(self.update_pendulum)

    def _update_pos(self, theta1, theta2):
        self.theta1 = theta1
        self.theta2 = theta2

        self.pendulum1._update_pos(theta1)

        # TODO: think of a smarter way
        self.pendulum2.theta = theta2
        bob2_pos = self.pendulum2.get_bob_position()

        self.pendulum2.rod.put_start_and_end_on(
            self.pendulum1.bob.get_center(), bob2_pos)
        self.pendulum2.bob.move_to(bob2_pos)

        return bob2_pos

    @staticmethod
    def update_pendulum(self, dt):
        m1 = self.bob1_config["mass"]
        m2 = self.bob2_config["mass"]
        l1 = self.rod1_config["length"]
        l2 = self.rod2_config["length"]
        cos = np.cos
        sin = np.sin

        # the formulas below for angular accelerations are taken from myPhysicsLab
        # myPhysicsLab Double Pendulum: https://www.myphysicslab.com/pendulum/double-pendulum-en.html

        num1 = -self.g * (2 * m1 * m2) * sin(self.theta1)
        num2 = -m2 * self.g * sin(self.theta1 - 2 * self.theta2)
        num3 = -2 * sin(self.theta1 - self.theta2) * m2 * \
            (self.omega1 ** 2 * l2 + self.omega1 **
             2 * l1 * cos(self.theta1 - self.theta2))

        den = l1 * (2 * m1 + m2 - m2 * cos(2 * self.theta1 - 2 * self.theta2))

        alpha1 = (num1 + num2 + num3) / den  # angular acceleration

        num1 = 2 * sin(self.theta1 - self.theta2)
        num2 = self.omega1 ** 2 * l2 * (m1 + m2)
        num3 = self.g * (m1 + m2) * cos(self.theta1) + \
            self.omega2 ** 2 * l2 * m2 * cos(self.theta1 - self.theta2)

        den = l2 * (2 * m1 + m2 - m2 * cos(2 * self.theta1 - 2 * self.theta2))

        alpha2 = (num1 * (num2 + num3)) / den

        self.omega1 += self.speed * dt * alpha1
        self.omega2 += self.speed * dt * alpha2
        self.theta1 += dt * self.omega1
        self.theta2 += dt * self.omega2

        bob2_pos = self._update_pos(self.theta1, self.theta2)

        # tracing the lower bob
        if self.show_trail:
            self.trail_path.append(bob2_pos)
            if len(self.trail_path) > self.trail_length:
                self.trail_path.pop(0)
            self.path.set_points_smoothly(self.trail_path)


class DoublePendulumScene(Scene):
    def construct(self):
        dp = DoublePendulum(
            theta1=PI / 2,
            theta2=PI / 2,
            rod1_config={"length": 1},
            rod2_config={"length": 0.9},
            bob1_config={"mass": 1, "color": BLUE},
            bob2_config={"mass": 0.9, "color": BLUE},
            trail_length=np.inf
        )

        self.add(dp)
        dp.path.set_color_by_gradient([WHITE, BLUE_D, WHITE])
        dp.start_swinging()
        self.wait(50)
        dp.stop_swinging()
        self.wait()
