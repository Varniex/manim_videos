# Dragon Fractal

from manim import *


class DragonFractal(Scene):
    CONFIG = {
        "colors": [RED, ORANGE, GREEN_B, BLUE_D, BLUE, VIOLET]
    }

    def construct(self):
        self.colors.reverse()
        self.colors = it.cycle(self.colors)

        line = Line(DOWN, UP)
        self.offset = 1.4

        self.dragon = VMobject()
        self.dragon.set_stroke(width=20)
        self.dragon.set_points(line.get_points())
        self.dragon.set_color(next(self.colors))

        self.frame = self.camera.frame
        self.frame.set_height(self.dragon.get_height() * self.offset)
        self.frame.move_to(self.dragon.get_center())

        self.last_point = self.dragon.get_last_point()

        self.play(ShowCreation(self.dragon.copy()))

        for _ in range(22):
            self.copy_and_rotate()
        self.wait()

    def copy_and_rotate(self):
        dragon = self.dragon.copy()
        dragon.set_color(next(self.colors))
        dragon.generate_target()
        dragon.target.rotate(PI / 2, about_point=self.last_point)

        self.bring_to_back(dragon)
        self.dragon.set_points(
            np.vstack((self.dragon.get_points(), dragon.target.get_points()))
        )

        self.play(
            MoveToTarget(dragon, path_arc=PI / 2),
            self.frame.set_height, self.dragon.get_height() * self.offset,
            self.frame.move_to, self.dragon.get_center(),
            run_time=1.5,
            rate_func=linear,
        )

        self.last_point = self.dragon.get_points()[len(self.dragon.get_points()) // 2]
