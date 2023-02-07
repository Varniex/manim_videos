# Double Pendulum Chaos

from manim_imports import *
from manimation.double_pendulum import DoublePendulum


class DoublePendulumChaos(Scene):
    CONFIG = {
        "num": 10,  # number of Double Pendulums
        "colors": VIBGYOR
    }

    def construct(self):
        self.colors = it.cycle(self.colors)
        dps = VGroup(*[
            DoublePendulum(
                theta1=PI / 2 + i / (2 * self.num) * DEGREES,
                theta2=PI / 2 + i / (2 * self.num) * DEGREES,
                bob1_config={"color": color},
                bob2_config={"color": color},
                show_trail=False,
            )
            for i in range(self.num)
            if (color := next(self.colors))
        ])

        for dp in dps:
            self.add(dp)
            dp.start_swinging()
        self.wait(15)

        for dp in dps:
            dp.remove(
                dp.pendulum2.rod,
                dp.pendulum1.rod,
                dp.pendulum1.bob,
            )
        self.wait(5)
