# Hilbert Curve
# Inspired by TheCodingTrain:
# Coding in the Cabana 3: Hilbert Curve: https://youtu.be/dSK-MW-zuAc

from manim import *


class HilbertCurve(VMobject):
    CONFIG = {
        "order": 1,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.order == 1:
            path_points = [UL, DL, DR, UR]
        else:
            curves = VGroup()
            for i in range(4):
                order = self.order - 1
                curve = HilbertCurve(order=order)

                if i == 0:
                    curve.rotate(PI / 2)
                    curve.flip(axis=RIGHT)
                elif i == 1:
                    curve.rotate(-PI / 2)
                    curve.flip(axis=RIGHT)
                curves.add(curve)
            curves.arrange_in_grid(buff=1)

            # Rearrange curves
            curves = VGroup(curves[0], curves[2], curves[3], curves[1])

            # taking only corner points and the last point from the curves
            path_points = [
                p for curve in curves for i, p in enumerate(curve.get_points())
                if (i % 3 == 0 or i % (len(curve.get_points()) - 1) == 0)
            ]
        self.set_points_as_corners(path_points)


class HilbertCurveScene(Scene):
    def construct(self):
        n = 8  # order of the curve
        offset = 1.1  # offset wrt height of the camera frame
        colors = VIBGYOR
        frame = self.camera.frame

        old_hilbert = HilbertCurve(order=1)
        old_hilbert.set_height(frame.get_height() / offset)

        final_hilbert = HilbertCurve(order=n)
        colors = color_gradient(colors, len(final_hilbert.get_points()))

        order_is = text, number = VGroup(
            TexText("Order = ", font_size=48),
            Integer(1, font_size=36)
        )
        order_is.arrange(RIGHT)
        order_is.to_corner(UL, buff=0.5)
        self.play(Write(order_is))

        order_tracker = ValueTracker()
        f_always(number.set_value, order_tracker.get_value)

        for i in range(2, n + 2):
            order_tracker.set_value(i - 1)
            old_hilbert.set_color_by_gradient(colors[:len(old_hilbert.get_points())])

            self.play(
                ShowCreation(old_hilbert),
                run_time=i,
                rate_func=linear
            )
            self.wait()

            if i == n + 1:
                break

            # removing the old_hilbert
            self.mobjects.pop(1)

            if i == n:
                new_hilbert = final_hilbert
            else:
                new_hilbert = HilbertCurve(order=order_tracker.get_value() + 1)
            new_hilbert.set_height(frame.get_height() / offset)

            self.play(
                old_hilbert.rotate, PI / 2,
                old_hilbert.set_points, new_hilbert.get_points()[:len(old_hilbert.get_points())]
            )

            old_hilbert = new_hilbert
