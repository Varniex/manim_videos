from manim_imports import *


class Marbles(VGroup):
    def __init__(
        self,
        n: int = None,
        n_rows: int = 10,
        n_cols: int = 10,
        radius: float = 0.2,
        buff: float = None,
        primary_color: str = RED_B,
        secondary_color: str = CYAN,
        **kwargs,
    ):
        n = randint(n_rows * n_cols + 1) if n is None else n
        dots = [Dot(radius=radius) for _ in range(n_rows * n_cols)]
        super().__init__(*dots, **kwargs)
        self.arrange_in_grid(n_rows, n_cols, buff=buff)
        self.pc = primary_color
        colors = [primary_color] * n + [secondary_color] * (n_rows * n_cols - n)
        shuffle(colors)

        self.set_color_by_gradient(*colors)
        self.set_n(n)

    def set_n(self, n: int):
        self.n = n
        return self

    def pick_random_marble(self) -> Dot:
        marble = self.submobjects[randint(len(self.submobjects))]
        if marble.get_color() == self.pc:
            self.set_n(self.get_n() - 1)
        self.remove(marble)
        return marble

    def get_n(self) -> int:
        return self.n


class DescribeProblem(Scene):
    def construct(self):
        marbles = Marbles(radius=0.15, primary_color=WHITE, secondary_color=WHITE)
        self.play(GrowFromPoint(marbles, OUT))
        self.wait()

        pick1 = marbles[randint(100)]

        info = TexText(
            r"Out of $100$ balls,\\$n$ are red balls,\\and rest are green,\\ where\\$n \in [0, 100]$\\is uniformly chosen\\at random.",
            t2c={"red": RED_B, "green": TEAL_B},
        )
        info.to_edge(LEFT, buff=0.5)
        n1 = randint(100, size=50)
        n2 = set(range(100)) - set(n1)
        self.play(
            Write(info[:26]),
            *[marbles[i].animate.set_color(RED_B) for i in n1],
        )
        self.play(*[marbles[i].animate.set_color(WHITE) for i in n1])
        nl = NumberLine(x_range=(0, 100, 10), width=6, include_numbers=True)
        nl.rotate(PI / 2).to_edge(RIGHT, buff=1)

        n_tracker = ValueTracker(len(n1))
        n_indicate = Tex(r"n \ \blacktriangleright")
        n_indicate.scale(0.8)
        n_indicate.next_to(nl, LEFT, buff=0.2)
        n_indicate.f_always.set_y(lambda: nl.n2p(n_tracker.get_value())[1])

        marbles.n = n_tracker.get_value()
        marbles.pn = n_tracker.get_value()

        def change_marbles(m):
            m.n = n = int(n_tracker.get_value())
            if m.n != m.pn:
                m.pn = m.n
                colors = [RED_B] * n + [TEAL_B] * (100 - n)
                shuffle(colors)
                m.set_color_by_gradient(*colors)

        self.play(
            Write(info[26:]),
            *[marbles[i].animate.set_color(TEAL_B) for i in n2],
            ShowCreation(nl),
            Write(n_indicate),
        )
        self.wait()

        marbles.add_updater(change_marbles)
        self.add(marbles)
        for i in randint(100, size=5):
            self.play(n_tracker.animate.set_value(i))
            self.wait()

        self.play(
            *[m.animate.set_color(WHITE) for m in marbles],
            FadeOutToPoint(nl, 7 * RIGHT),
            Uncreate(n_indicate),
        )

        self.play(pick1.animate.move_to(4.5 * RIGHT))
        self.wait()
        self.play(pick1.animate.set_color(RED_B))
        self.wait()

        # adding trajectory
        trajectory = Line(
            pick1.get_center(), pick1.get_center() + 3.5 * RIGHT, path_arc=-PI / 2
        )
        self.play(MoveAlongPath(pick1, trajectory))
        self.wait()
        marbles.remove(pick1)

        pick2 = marbles[randint(99)]
        self.play(pick2.animate.move_to(4.5 * RIGHT))
        self.wait()

        self.play(FadeOut(info), marbles.animate.to_edge(LEFT, buff=1))

        red = pick2.copy().set_color(RED_B)
        red.next_to(pick2, DL, buff=0.5)

        green = red.copy().set_color(TEAL_B)
        green.next_to(red, DOWN, buff=0.5)

        ques = Text(
            "Is the second ball more\nlikely to be red or green\nor both are equally likely?",
            t2c={"red": RED_B, "green": TEAL_B, "both": CYAN},
        )
        ques.next_to(pick2, UP, buff=-0.2).shift(1.5 * RIGHT)

        self.play(TransformFromCopy(pick2, red))
        self.play(ReplacementTransform(pick2, green))
        self.play(Write(ques))
        self.wait()
        self.play(Indicate(red), Indicate(green))
        self.wait()

        self.play(*[FadeOut(m) for m in self.mobjects])

        txt = Text("Probability Puzzle", font="Lobster Two")
        txt.set_color_by_gradient(CYAN, RED_B)
        txt.set_width(8)
        self.play(GrowFromPoint(txt, 2 * DOWN))
        self.wait()

        txt.target = txt.generate_target()
        txt.target.set_width(5).to_edge(UP, buff=0.5)

        author = Text("~ by Daniel Litt")
        author.set_width(2.5)
        author.next_to(txt.target, DOWN, buff=0.2).align_to(txt.target, RIGHT)

        img = ImageMobject("daniel_litt_prob")
        img.set_width(9).move_to(0.75 * DOWN)
        bg = SurroundingRectangle(img, stroke_color=WHITE, stroke_width=8, buff=0)

        self.play(MoveToTarget(txt), ShowCreation(img), ShowCreation(bg))
        self.play(Write(author))
        self.wait(2)


class Simulation(Scene):
    def construct(self):
        marbles = Marbles(n=60)
        pick_color = "CYAN"
        while pick_color != marbles.pc:
            pick_color = marbles[n := randint(100)].get_color()

        marbles.save_state()
        marbles.set_color(WHITE)
        self.play(GrowFromCenter(marbles))
        self.wait()

        self.play(marbles[n].animate.move_to(5 * RIGHT).set_color(RED_B))
        self.play(Restore(marbles), marbles[n].animate.move_to(5 * RIGHT))
        self.wait()
        self.play(FadeOut(marbles))
        self.wait()

        txt = Text("Let's do the Simulation!", font="Lobster Two")
        txt.set_width(8)
        txt.set_color_by_gradient(CYAN, WHITE, VIOLET)
        self.play(Write(txt))
        self.play(ApplyWave(txt, amplitude=0.5))
        self.wait()
        self.play(Uncreate(txt))
        self.wait()

        self.simulate()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.simulate(randomize=True)
        self.wait()

    def simulate(self, randomize: bool = False):
        if randomize:
            all_marbles = VGroup(Marbles() for _ in range(101))
        else:
            all_marbles = VGroup(Marbles(n=i) for i in range(101))

        all_marbles.arrange_in_grid(n_cols=17, buff=0.2)
        all_marbles.set_width(FRAME_WIDTH / 1.05)
        all_marbles.arrange_in_grid(n_cols=17, buff=0.2)
        all_marbles.set_width(FRAME_WIDTH / 1.05)
        all_marbles.to_edge(UP, buff=0.75)

        self.play(ShowCreation(all_marbles), run_time=2)
        self.wait()

        total_samples = TexText("Total Samples = 101")
        total_samples.next_to(all_marbles, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        red_more = TexText("Samples having more red balls = 50")
        red_more.next_to(total_samples, DOWN, buff=0.5)
        red_more.align_to(total_samples, LEFT)
        red_samples_count = red_more.make_number_changeable("50")
        red_samples_count.set_value(sum(m.n > 50 for m in all_marbles))

        self.play(Write(total_samples), Write(red_more))
        self.wait()

        for m in all_marbles:
            ma = m.pick_random_marble()
            if ma.get_color() == RED_B:
                m.fade_it = False
            else:
                m.fade_it = True

        total_samples_count = total_samples.make_number_changeable("101")
        total_samples_desc = TexText(r"$\rightarrow$ \ the first drawn ball is red.")
        total_samples_desc.next_to(total_samples_count, RIGHT, buff=0.15)

        self.play(
            *[m.animate.set_opacity(0.35) for m in all_marbles if m.fade_it],
            Write(total_samples_desc),
            total_samples_count.animate.set_value(
                (r1 := sum(not m.fade_it for m in all_marbles))
            ),
            red_samples_count.animate.set_value(
                sum(m.n > len(m) / 2 for m in all_marbles if not m.fade_it)
            ),
        )
        self.wait()
        all_marbles.save_state()
        self.play(
            *[
                FlashAround(m)
                for m in all_marbles
                if not m.fade_it and m.n > len(m) / 2
            ],
            run_time=5,
        )
        self.wait()
        self.play(
            *[
                m.animate.set_opacity(0.5)
                for m in all_marbles
                if not m.fade_it and m.n > len(m) / 2
            ],
            run_time=2,
        )
        self.wait()
        self.play(Restore(all_marbles))

        for m in all_marbles:
            if not m.fade_it:
                ma = m.pick_random_marble()
                if ma.get_color() == RED_B:
                    m.fade_it = False
                else:
                    m.fade_it = True

        self.play(*[m.animate.set_opacity(0.35) for m in all_marbles if m.fade_it])

        final_samples_txt = Text(
            f"Total samples where red second ball is drawn = {(r2:=sum(not m.fade_it for m in all_marbles))}"
        )
        final_samples_txt.match_y(red_more).align_to(total_samples, LEFT)
        self.play(TransformMatchingTex(red_more, final_samples_txt))
        self.wait()
        self.play(
            *[FadeOutToPoint(i, BOTTOM) for i in [total_samples, total_samples_desc]],
            TransformMatchingTex(
                final_samples_txt,
                TexText(
                    f"Probability that second ball is red  \\approx \\ {r2/r1:0.4f}"
                )
                .move_to(final_samples_txt)
                .shift(0.4 * UP),
            ),
        )
        self.wait()


class SimulatingGraph(Scene):
    def construct(self):
        # add axes
        txt = Text(
            "Probability of drawing a second red ball\ngiven that first drawn ball is red."
        ).to_edge(UP, buff=0.5)
        txt.set_color_by_gradient(CYAN, WHITE, VIOLET)
        txt.shift(0.75 * RIGHT)

        axes = Axes(
            x_range=(0, 1100, 100),
            y_range=(0, 1.1, 0.1),
            axis_config=dict(include_tip=True, include_numbers=True),
            y_axis_config=dict(decimal_number_config={"num_decimal_places": 1}),
            height=7,
            width=10,
        )
        self.play(Write(axes), GrowFromCenter(txt), run_time=2)
        self.wait()

        dot = Dot(axes.c2p(0, 0.67))
        trail = TracingTail(
            dot, time_traced=10, stroke_opacity=1, stroke_width=4, stroke_color=CYAN
        )

        mean, mnum = self.get_number_track("Mean")
        ma, manum = self.get_number_track("Max")
        mi, minum = self.get_number_track("Min")

        stats = []
        mnum.f_always.set_value(lambda: np.mean(stats) if stats else 0.00)
        manum.f_always.set_value(lambda: np.max(stats) if stats else 0.00)
        minum.f_always.set_value(lambda: np.min(stats) if stats else 0.00)

        stats_tex = VGroup(mean, mi, ma).arrange(RIGHT, buff=1)
        stats_tex.shift(DOWN)

        self.add(trail)
        self.play(ShowCreation(dot), Write(stats_tex))

        for i in range(1000):
            balls = array(
                [shuffled([0] * (100 - i) + [1] * i) for i in randint(101, size=100)]
            )
            pick1 = balls[:, randint(100, size=balls.shape[0])].diagonal()
            r1 = pick1.sum()

            sample1 = balls[pick1 == 1]
            r2 = sample1[:, randint(100, size=r1)].diagonal().sum()

            stats.append(r2 / r1)
            if not i % 10:
                self.play(
                    dot.animate.move_to(axes.c2p(i + 1, np.mean(stats[-10:]))),
                    run_time=0.05,
                )
        self.wait()

    @staticmethod
    def get_number_track(txt: str):
        tex = TexText(f"{txt}: 0.00")
        num = tex.make_number_changeable("0.00")
        return tex, num


class ConditionalProbab(Scene):
    def construct(self):
        txt = Title("Conditional Probability")
        txt.set_color_by_gradient(VIOLET, WHITE, VIOLET)
        self.play(ShowCreation(txt))
        self.wait()

        color_map = {"A": RED_B, "B": CYAN}

        # adding events desc
        events_desc = (
            VGroup(
                TexText(
                    f"$P({i}) \\rightarrow \ $ probability of occuring event ${i}$",
                    t2c=color_map,
                )
                for i in ["A", "B"]
            )
            .arrange(DOWN, buff=0.5)
            .next_to(txt, DOWN, buff=0.8)
        )
        self.play(Write(events_desc))
        self.wait()

        # adding cond
        cond_txt = Tex(r"P(A|B) = \frac{P(A\cap B)}{P(B)}", t2c=color_map)
        cond_txt.next_to(events_desc, DOWN, buff=1.5)
        self.play(Write(cond_txt))
        self.wait()

        # adding descs
        given_txt = TexText("Probability of $A$ given $B$", t2c=color_map)
        given_txt.set_width(3).rotate(PI / 8)
        given_txt.next_to(cond_txt, UL, buff=-0.35)

        and_txt = TexText("Probability of $A$ and $B$", t2c=color_map)
        and_txt.set_width(3).rotate(-PI / 8)
        and_txt.next_to(cond_txt, UR, buff=-0.15)

        self.play(*[Write(i) for i in [given_txt, and_txt]])
        self.wait()


class AnalyticalSolution(Scene):
    def construct(self):
        n2 = VGroup(Marbles(n=i, n_rows=1, n_cols=2) for i in range(3))
        n2[1].set_color_by_gradient(RED_B, CYAN)
        n2.arrange(RIGHT, buff=2.2).shift(0.15 * RIGHT)
        self.play(ShowCreation(n2))
        self.wait()
        self.play(n2.animate.to_edge(UP, buff=1.5))

        marbles_txt = VGroup(Text(i) for i in ["BB", "RB", "RR"])
        n_txt = VGroup(Tex(f"n = {i}") for i in range(3))
        for m, n, nt in zip(marbles_txt, n2, n_txt):
            m.next_to(n, UP, buff=0.5)
            nt.next_to(n, DOWN, buff=0.35)

        n2_txt = Tex("N = 2")
        n2_txt.next_to(n2, LEFT, buff=1.5)
        self.play(Write(n2_txt), Write(marbles_txt), Write(n_txt))
        self.wait()

        pni = Tex(r"P(n_i = n) = \frac{1}{N+1} = \frac{1}{3}")
        ppr1 = Tex(
            r"P(r_1  \ | \ n_i) = \frac{n}{N} \ ; \ \ \ \ P(r_1 \cap r_2 \ | \ n_i) = \frac{n}{N} \cdot \frac{n-1}{N-1}"
        )
        ppr1.next_to(pni, DOWN, buff=0.65)
        pni_desc = TexText(
            "$n_i$ denotes the event of selecting a set with $n$ red balls."
        ).next_to(pni, DOWN, buff=2.25)
        self.play(Write(pni[:-4]))
        self.wait()
        self.play(Write(pni[-4:]), Write(pni_desc), Write(ppr1))
        self.wait()
        self.play(FadeOut(pni), Uncreate(pni_desc), Uncreate(ppr1))

        pr1 = Tex("P(r_1)")
        pr1.next_to(n2_txt, DOWN, buff=1.6)

        pr1_ni = VGroup(Tex(f"P(r_1 | n_{i})P(n_{i})") for i in range(3))

        equals_plus = VGroup(Tex("="), Tex("+"), Tex("+"), Tex("="))
        equals_plus.arrange(RIGHT, buff=2.9).match_y(pr1)
        equals_plus.shift(0.1 * RIGHT)

        for p, n in zip(pr1_ni, n_txt):
            p.next_to(n, DOWN, buff=1).align_to(pr1, DOWN).scale(0.75)

        self.play(*[Write(i) for i in [pr1, pr1_ni, equals_plus[:-1]]])
        self.wait()

        # picking first ball
        self.play(*[m[0].animate.set_opacity(0.35) for m in n2])

        # adding checkpoint
        pr1_ni_ans = VGroup(
            Tex(r"\frac{1}{3}\cdot\frac{0}{2}"),
            Tex(r"\frac{1}{3}\cdot\frac{1}{2}"),
            Tex(r"\frac{1}{3}\cdot\frac{2}{2}"),
        )
        for p, pni in zip(pr1_ni_ans, pr1_ni):
            p.move_to(pni)
        self.play(FadeOut(pr1_ni))

        self.play(
            LaggedStart(*[Write(m[4:]) for m in pr1_ni_ans], lag_ratio=1),
            run_time=5,
        )
        self.wait()
        self.play(*[Write(m[:4]) for m in pr1_ni_ans], run_time=2)
        self.wait()
        ignore = VGroup(marbles_txt[0], n_txt[0], pr1_ni_ans[0], n2[0])

        self.play(
            *[m.animate.set_opacity(0.25) for m in ignore.add(equals_plus[1])],
            Write(Cross(ignore.remove(equals_plus[1]), stroke_width=[2, 6, 2])),
        )

        pr1_ans = Tex(r"\frac{1}{2}").next_to(equals_plus, RIGHT, buff=0.5)
        self.play(Write(equals_plus[-1:]), Write(pr1_ans))
        self.wait()

        pr1r2 = Tex(r"P(r_1 \cap r_2)")
        pr1r2.next_to(pr1, DOWN, buff=1).scale(0.9).shift(0.15 * LEFT)
        pr1r2_ni = VGroup(
            Tex(f"P(r_1 \\cap r_ 2 | n_{i})P(n_{i})") for i in range(1, 3)
        )
        pr1r2_ni.arrange(RIGHT, buff=1).next_to(pr1r2, buff=1)

        equals_plus_1 = equals_plus.copy().match_y(pr1r2)
        equals_plus_1.shift(0.2 * RIGHT)
        equals_plus_1[1].set_opacity(1).shift(1.7 * RIGHT)
        equals_plus_1[2].set_opacity(0)
        equals_plus_1[-1].next_to(equals_plus[-1], DOWN, buff=1.3)

        self.play(*[Write(i) for i in [pr1r2, equals_plus_1[:-1], pr1r2_ni]])

        pr1r2_ni_ans = VGroup(
            Tex(r"\frac{1}{3} \cdot \frac{1}{2} \frac{0}{1}"),
            Tex(r"\frac{1}{3} \cdot \frac{2}{2} \frac{1}{1}"),
        )

        for p1, p2 in zip(pr1r2_ni, pr1r2_ni_ans):
            p2.move_to(p1)

        self.play(
            *[Write(p2[4:]) for p2 in pr1r2_ni_ans],
            FadeOut(pr1r2_ni),
        )
        self.wait()
        self.play(*[Write(p[:4]) for p in pr1r2_ni_ans])
        self.wait()
        pr1r2_ans = Tex(r"\frac{1}{3}")
        pr1r2_ans.next_to(pr1_ans, DOWN, buff=0.4)
        self.play(Write(equals_plus_1[-1]), Write(pr1r2_ans))
        self.wait()

        final_ans = Tex(
            r"P(r_2 | r_1) = \frac{P(r_1 \cap r_2)}{P(r_1)} = \frac{2}{3} \approx 0.67"
        )
        final_ans.to_edge(DOWN, buff=0.5).align_to(pr1r2, LEFT).shift(0.2 * RIGHT)
        self.play(Write(final_ans[:-9]))
        self.wait()
        self.play(Write(final_ans[-9:]))
        self.wait()

        self.play(*[FadeOut(m) for m in self.mobjects])

        title = TexText(
            r"For general $N$: $P(n_i) = \displaystyle\frac{1}{N+1}$"
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait()

        # pr1s
        fpr1 = Tex(
            R"""
            \begin{aligned}
            P(r_1) &= \sum_{i=0}^{N}P(r_1 | n_i)P(n_i) = \sum_i \frac{n}{N} \cdot \frac{1}{N+1} \\
            P(r_1) &= \frac{1}{N(N+1)} \sum_i n \\
            P(r_1) &= \frac{1}{2}
            \end{aligned}
        """,
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(fpr1))
        self.wait()

        fpr1_f = Tex(r"P(r_1) = \frac{1}{2}").next_to(title, DOWN, buff=0.5)
        self.play(TransformMatchingTex(fpr1, fpr1_f))
        self.wait()

        # add fpr2
        fpr2 = Tex(
            r"""
            \begin{aligned}
            P(r_2 \cap r_1) &= \sum_{i=1}^{N} P(r_1 \cap r_2 | n_i) P(n_i) = \sum_i \frac{n - 1}{N-1} \cdot \frac{n}{N} \cdot \frac{1}{N+1} \\
            P(r_2 \cap r_1) &= \frac{1}{N(N+1)(N-1)}\sum_i n^2 - n = \frac{1}{3}
            \end{aligned}
        """
        ).next_to(fpr1_f, DOWN, buff=0.5)
        self.play(Write(fpr2))
        self.wait()

        fpr2_f = Tex(r"P(r_2 \cap r_1) = \frac{1}{3}")
        fpr2_f.next_to(fpr1_f, DOWN, buff=0.5)

        self.play(TransformMatchingTex(fpr2, fpr2_f))
        self.wait()

        final_ans.next_to(fpr2_f, DOWN, buff=0.8)
        self.play(Write(final_ans))
        self.wait()
