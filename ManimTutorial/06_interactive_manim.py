# Varniex - CodingManim 06: Interactive Manim
# YouTube Video: https://youtu.be/cm8eK1Mtn2U

from manimlib import *


LEFT_BUTTON = 1
RIGHT_BUTTON = 4


class InteractiveManim(InteractiveScene):
    def construct(self):
        square = Square()
        self.play(ShowCreation(square))
        self.wait()

        text = Text("This is a Square")
        text.next_to(square, DOWN, buff=0.5)
        self.play(Write(text))
        self.wait()


class CustomizeMouseInput(InteractiveScene):
    def consturct(self):
        # this is necessary to enable embed mode
        pass

    def on_mouse_press(self, point, button, mods):
        if button == LEFT_BUTTON:
            self.add(Dot(point))
        else:
            square = Square(side_length=1)
            square.set_color(RED_B, opacity=1)
            square.move_to(point)
            self.add(square)

    def on_mouse_drag(self, point, d_point, buttons, mods):
        self.add(Dot(point))

    def on_mouse_release(self, point, button, mods):
        last_mobject = self.mobjects[-1]
        self.play(last_mobject.animate.set_width(2).set_color(BLUE))


class CustomizeKeyboardInput(InteractiveScene):
    def construct(self):
        pass

    def on_key_press(self, symbol, mods):
        char = chr(symbol)

        if char == " ":
            self.text = Text("write_your_text_here")
            self.play(Write(self.text))

    def on_key_release(self, symbol, mods):
        char = chr(symbol)

        if char == " ":
            new_text = Text("transformed_text")
            self.play(TransformMatchingStrings(self.text, new_text))
            self.wait(2)
            self.play(FadeOut(new_text))
