# Varniex - CodingManim 04: Generating Text in Manim
# YouTube Video: https://youtu.be/vphwF6eMPYE

from manimlib import *


class ImageSVGExample(Scene):
    def construct(self):
        img = ImageMobject("car")
        # img = SVGMobject("car") for 'car.svg' file
        img.set_width(4)
        self.play(FadeIn(img))

        img.move_to(2 * RIGHT)
        img.rotate(45 * DEGREES)
        img.scale(0.5)


class MarkupTextExample(Scene):
    def construct(self):
        mtext = VGroup(
            MarkupText("<span>This is MarkupText</span>."),
            MarkupText("This is <i>italic</i>."),
            MarkupText("And this is <b>bold</b>."),
        ).arrange(DOWN, buff=0.5)

        self.play(Write(mtext))
        self.wait()


class ColorizingText(Scene):
    def construct(self):
        eq = Tex(
            r"R_{\mu\nu} - {1 \over 2} Rg_{\mu\nu} + \Lambda g_{\mu\nu} = {8 \pi G \over c^4}T_{\mu\nu}",
            tex_to_color_map={"G": PINK},
            isolate=[r"R_{\mu\nu}", r"\Lambda"],
        )
        self.play(Write(eq))
        self.play(eq[0].animate.set_color(TEAL))
        self.play(eq[r"\Lambda"].animate.set_color(BLUE))
        self.play(eq.animate.set_color_by_gradient(RED, PINK, YELLOW, BLUE))


class TextExample(Scene):
    def construct(self):
        text_example = VGroup(
            Text("This example is written in font 'Consolas'.", font="Consolas"),
            Text(
                "With the help of Text class, we can assign "
                "different\n\ncolors to different words."
            ),
            Text(
                "For example:\n\nThis is Yellow color,\n\nand "
                "this should render as Blue color.",
                t2c={"Yellow": YELLOW, "Blue": BLUE},
            ),
            Text(
                "Not only colors, but it also changes the style "
                "of the words.\n\nThis is italic, and this is Bold",
                t2s={"italic": ITALIC},
                t2w={"Bold": BOLD},
            ),
            Text(
                "Even we can write different words with different fonts like:\n\n"
                "Consolas, Arial, Cambria, Gabriola",
                t2f={
                    "Consolas": "Consolas",
                    "Arial": "Arial",
                    "Cambria": "Cambria",
                    "Gabriola": "Gabriola",
                },
            ),
        ).set_width(FRAME_WIDTH / 1.5)

        for text in text_example:
            self.play(Write(text))
            self.wait()
            self.play(Uncreate(text))
