# Pendulum Chaos

from manim import *


class Pendulum(VMobject):
    CONFIG = {
        "g": 9.8,  # acceleration due to gravity
        "origin": ORIGIN,  # hinge location
        "theta": 0,  # initial angle from the vertical
        "omega": 0,  # initial angular velocity
        "rod_config": {
            "length": 2,
            "color": WHITE,
            "stroke_width": 1.5,
        },
        "bob_config": {
            "mass": 0.1,
            "radius": 0.1,
            "color": BLUE,
            "fill_opacity": 1,
        },
        "speed": 0.8,  # speed of the simulation
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        digest_config(self, kwargs)

        bob_position = self.get_bob_position()

        self.rod = Line(
            self.origin,
            bob_position,
            **self.rod_config
        )

        self.bob = Circle(**self.bob_config)
        self.bob.move_to(bob_position)

        self.pendulum = VGroup(self.rod, self.bob)
        self.add(self.rod, self.bob)

    def get_length(self):
        return self.rod_config["length"]

    def get_bob_position(self):
        length = self.get_length()

        x = self.origin[0] - length * np.sin(self.theta)
        y = self.origin[1] - length * np.cos(self.theta)
        return np.array([x, y, 0])

    def _update_pos(self, theta):
        self.theta = theta
        theta = -(theta + PI / 2) % TAU
        self.rod.set_angle(theta)
        self.bob.move_to(self.rod.get_last_point())

    def start_swinging(self):
        self.add_updater(self.update_pendulum)

    def stop_swinging(self):
        self.remove_updater(self.update_pendulum)

    @staticmethod
    def update_pendulum(self, dt):
        theta = self.theta
        length = self.get_length()

        alpha = - self.g * np.sin(theta) / length  # angular acceleration

        self.omega += self.speed * dt * alpha
        self.theta += self.speed * dt * self.omega
        self._update_pos(self.theta)


class PendulumChaos(Scene):
    CONFIG = {
        "num": 1,  # number of pendulums
        "wait_time": 10,  # time of simulation
    }

    def construct(self):
        colors = it.cycle([ORANGE, BLUE, YELLOW, GREEN, RED_B])

        self.pends = VGroup(*[
            Pendulum(
                theta=PI / 2,
                rod_config={"length": i},
                bob_config={"color": next(colors)},
                speed=0.85,
            ) for i in reversed(np.linspace(1.5, 3, self.num))
        ])

        self.play(
            *[ShowCreation(pend) for pend in self.pends]
        )
        self.wait()

        for pend in self.pends:
            pend.start_swinging()
        self.wait(self.wait_time)


class PendulumChaos10(PendulumChaos):
    CONFIG = {
        "num": 10
    }

    def construct(self):
        super().construct()

        for pend in self.pends:
            pend.remove(pend.rod)
        self.wait(self.wait_time)
