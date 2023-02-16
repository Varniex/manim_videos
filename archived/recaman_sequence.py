# Recaman Sequence
#
# Inspired By:
#       Numberphile video: https://youtu.be/FGC5TdIiT9U
#       Coding Train: Coding Challenge #110.1 -- https://youtu.be/DhFZfzOvNTU

from manim_imports import *


class RecamanSequence(Scene):
    CONFIG = {
        "n": 100,  # number of iterations
    }

    def construct(self):
        count = 0
        visited = [0] + [None] * self.n
        arcs = VGroup()

        self.index = 0  # acts as a pointer
        max_width = max(self.index, 3)  # to set the frame width

        for i in range(self.n):
            index = self.index - count

            if index < 0 or index in visited:
                index = self.index + count

            # defining the start and end of the arc
            start = np.array([visited[count], 0, 0])
            end = np.array([index, 0, 0])

            # defining the angle of arc (i.e., whether it would be an upward arc or downward arc)
            angle = PI if count % 2 else -PI

            if index < visited[count]:
                angle *= -1

            arc = ArcBetweenPoints(start, end, angle)
            arcs.add(arc)

            # updating variables
            self.index = index
            count += 1
            visited[count] = self.index

        # setting the colors of the arcs
        VIBGYOR.reverse()
        arcs.set_color_by_gradient(*VIBGYOR)

        frame = self.camera.frame

        # rendering the sequence
        for i, arc in enumerate(arcs):
            max_width = max(max_width, max(visited[:i + 2]))

            # as the frame width changes, the arcs starts to look thinner, so increasing
            # the stroke width of all arcs as frame width increases.
            arcs.set_stroke(width=arcs.get_stroke_width() * 1.028)

            self.play(
                ShowCreation(arc),
                frame.set_width, max_width,
                frame.move_to, max_width / 2 * RIGHT,
                rate_func=linear,
                run_time=0.25
            )


if __name__ == "__main__":
    render_scene(RecamanSequence)
