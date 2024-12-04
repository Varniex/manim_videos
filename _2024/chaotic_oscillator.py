from manim_imports import *


def get_oscillator_points(
    pos: np.ndarray,
    k: float = 1,
    gamma: float = 0,
    beta: float = 0,
    f0: float = 0,
    omega: float = 0,
    t=0,
    n_steps: int = 1,
) -> np.ndarray:
    dt = 1 / 60
    x, v, _ = pos[:, 0], pos[:, 1], pos[:, 2]
    for _ in range(n_steps):
        dx = v
        dv = -k * x - gamma * v - beta * x**3 + f0 * cos(omega * t)

        x += dx * dt
        v += dv * dt

    return pos


# from https://github.com/3b1b/videos
class Spring(VMobject):
    def __init__(
        self,
        mobject: Mobject,
        base_point,
        edge=ORIGIN,
        stroke_color=WHITE,
        stroke_width=2,
        twist_rate=8.0,
        n_twists=8,
        radius=0.1,
        lead_length=0.25,
        **kwargs,
    ):
        super().__init__(**kwargs)

        helix = ParametricCurve(
            lambda t: [
                radius * math.cos(TAU * t),
                radius * math.sin(TAU * t),
                t / twist_rate,
            ],
            t_range=(0, n_twists, 0.01),
        )
        helix.rotate(PI / 2, UP)

        self.start_new_path(helix.get_start() + lead_length * LEFT)
        self.add_line_to(helix.get_start())
        self.append_vectorized_mobject(helix)
        self.add_line_to(helix.get_end() + lead_length * RIGHT)

        self.set_stroke(color=stroke_color, width=stroke_width)
        self.set_flat_stroke(False)

        reference_points = self.get_points().copy()
        width = self.get_width()
        self.add_updater(lambda m: m.set_points(reference_points))
        self.add_updater(
            lambda m: m.stretch(
                get_norm(base_point - mobject.get_edge_center(edge)) / width, 0
            )
        )
        self.add_updater(
            lambda m: m.put_start_and_end_on(base_point, mobject.get_edge_center(edge))
        )

    def get_length(self):
        return get_norm(self.get_end() - self.get_start())


class DuffingOscillator(VGroup):
    def __init__(
        self,
        m: float = 1,
        l0: float = 1,
        k: float = 1,
        gamma: float = 0,
        beta: float = 0,
        external_force=None,
        vel: float = 0,
        pos: float = 2,
        color: str = CYAN,
        side_length: float = 0.5,
        edge: np.ndarray = LEFT,
        base: np.ndarray = ORIGIN,
        spring_kwargs: dict = {},
        **kwargs,
    ):
        self.m = m
        self.l0 = l0
        self.k = k
        self.beta = beta
        self.gamma = gamma
        self.vel = vel

        self.mass = Square(side_length=side_length)
        self.mass.set_fill(color, 1)
        self.mass.move_to((pos + side_length / 2) * RIGHT + base)

        self.spring = Spring(self.mass, base, edge, **spring_kwargs)
        self.external_force = external_force

        super().__init__(self.spring, self.mass, **kwargs)
        self.add_to_back(self.spring)

    def reset_velocity(self):
        self.vel = 0

    def get_pos(self):
        return self.l0

    def get_momentum(self):
        return self.m * self.vel

    def get_force(self):
        dl = self.get_pos()
        spring_force = -self.k * dl
        damp_force = -self.gamma * self.vel
        perturbed_force = -self.beta * dl**3
        net_force = spring_force + damp_force + perturbed_force
        if self.external_force is not None:
            net_force += self.external_force()
        return net_force

    def get_acceleration(self):
        return self.get_force() / self.m

    def update_position(self, dt):
        self.vel += self.get_acceleration() * dt
        self.l0 += self.vel * dt
        self.mass.shift(self.vel * RIGHT * dt)

    def set_k(self, k):
        self.k = k
        return self

    def set_gamma(self, gamma):
        self.gamma = gamma
        return self

    def set_beta(self, beta):
        self.beta = beta
        return self

    def set_external_force(self, force):
        self.external_force = force
        return self

    def get_ke(self):
        return self.m * self.vel**2 / 2

    def get_pe(self):
        return (self.k * self.get_pos() ** 2 + self.beta * self.get_pos() ** 4 / 2) / 2

    def get_te(self):
        return self.get_ke() + self.get_pe()

    def start_simulation(self):
        self.mass.add_updater(lambda m, dt: self.update_position(dt))

    def stop_simulation(self):
        self.mass.clear_updaters()


class EarthTunnel(Scene):
    def construct(self):
        radius = 2.5
        earth = always_rotate(
            TexturedSurface(
                Sphere(radius=radius - 0.1).rotate(-50 * DEGREES, axis=RIGHT),
                "earth_texture",
                "earth_night_texture",
            ),
            80 * DEGREES,
            axis=UP,
        )
        self.play(GrowFromCenter(earth))
        self.wait(2)

        tunnel = Line(UP * radius, DOWN * radius, stroke_width=48)
        tunnel.set_color_by_gradient(BLACK)
        tunnel.save_state()
        tunnel.set_stroke(width=200)

        ball = Dot(fill_color=YELLOW_B)
        ball.set_width(0.2)
        ball.next_to(tunnel, UL, buff=0.1).shift(0.1 * DOWN)

        fr = self.frame
        fr.save_state()
        self.play(fr.animate.move_to(ball).set_width(2))
        self.wait()

        ques = Text(
            "What would happen if you fell\ninto the tunnel through the diameter?"
        ).fix_in_frame()
        ques.to_edge(UP, buff=1)
        ball.save_state()
        self.play(
            LaggedStart(FadeIn(tunnel), Write(ques), lag_ratio=0.5),
            rate_func=linear,
        )
        earth_update = earth.updaters[0]
        earth.clear_updaters()

        self.wait()
        self.play(Uncreate(ques))
        self.wait()
        earth.add_updater(earth_update)
        self.wait()
        self.play(
            Restore(tunnel),
            Restore(fr),
            ball.animate.move_to(2.5 * DOWN),
            rate_func=smooth,
            run_time=5,
        )
        self.wait()

        earth_cross_section = VGroup(
            Circle(radius=i, fill_opacity=0, stroke_opacity=1, stroke_width=4)
            for i in arange(0, radius, 0.005)
        )
        earth_cross_section.set_color_by_gradient(NAVY_BLUE, DARK_BLUE, BLUE)
        self.play(FadeOut(tunnel), FadeOut(ball), Write(earth_cross_section))
        self.remove(earth)
        self.wait()
        ball.become(Dot(radius=0.1).move_to(3.5 * DOWN).set_color(YELLOW))

        circle_outline = DashedVMobject(Circle(stroke_color=WHITE), num_dashes=35)
        circle_outline.set_stroke(width=5)
        always_rotate(circle_outline)
        circle_outline.f_always.set_width(lambda: 2 * get_norm(ball.get_center()))

        abcd = VGroup(Tex(s) for s in "ABCD")
        abcd.set_color(INDIGO)
        abcd.arrange(DOWN, buff=1)

        self.play(fr.animate.shift(3.5 * LEFT))
        self.wait()

        gs = VGroup(Tex(f"g_{s}") for s in "0ABCD")
        gs.arrange(RIGHT, buff=0.8)
        gs.to_edge(LEFT, buff=-2.5)
        self.bring_to_front(abcd)
        self.play(ShowCreation(abcd))
        self.wait()
        self.play(TransformFromCopy(abcd, gs))
        self.wait()

        is_equals = VGroup(Tex(r"\overset{?}{=}") for _ in range(4))
        is_equals.arrange(RIGHT, buff=1)
        is_equals.next_to(gs[0], RIGHT, buff=0.2).shift(0.15 * UP)

        not_equals = VGroup(Tex(r"\ne") for _ in range(4))
        not_equals.arrange(RIGHT, buff=1)
        not_equals.next_to(gs[0], RIGHT, buff=0.2)
        self.play(Write(is_equals))
        self.wait()

        self.play(TransformMatchingShapes(is_equals, not_equals))
        self.wait()

        func_g = Tex("g(r)")
        func_g.move_to(gs[0])
        equals = Tex("= \ ?")
        equals.next_to(func_g, RIGHT, buff=0.25)

        circle_r = Circle(stroke_color=WHITE)
        circle_r.set_fill(INDIGO, opacity=0.75)
        circle_r.scale(1.5)

        arrow_r = Line(ORIGIN, 1 * UR).add_tip(width=0.2, length=0.25)
        r_txt = Tex("r").rotate(45 * DEGREES)
        r_txt.next_to(arrow_r, UL, buff=-0.45)
        d2r = Tex(r"\frac{d^2r}{dt^2}")
        d2r.next_to(equals[0], RIGHT, buff=0.25).shift(0.08 * UP)

        self.play(
            Write(circle_r),
            Write(r_txt),
            Write(arrow_r),
            FadeOut(abcd),
            TransformMatchingShapes(gs, func_g),
            TransformMatchingShapes(not_equals, equals),
        )
        self.play(
            FadeOut(r_txt),
            Rotating(arrow_r, -TAU),
            TransformMatchingShapes(equals[1], d2r),
        )
        self.wait()

        self.play(Uncreate(arrow_r), Uncreate(circle_r))
        self.wait()

        self.play(fr.animate.move_to(2 * RIGHT))
        self.wait()

        for layer in earth_cross_section:
            layer.add_updater(
                lambda x: (
                    x.set_opacity(0.005)
                    if get_norm(ball.get_center()) < x.get_radius()
                    else x.set_opacity(1)
                )
            )

        self.play(ShowCreation(circle_outline), ShowCreation(ball))
        self.wait(2)

        grav_form = VGroup(
            Tex(r"F = -\frac{GMm}{r^2}"),
            Tex(r"mg = -\frac{GMm}{r^2}"),
            Tex(r"g(r) = -\frac{GM}{r^2}"),
        )
        grav_form.to_edge(RIGHT, buff=0.25)
        self.play(Write(grav_form[0]))
        self.wait()
        self.play(TransformMatchingTex(grav_form[0], grav_form[1]))
        self.wait()
        self.play(TransformMatchingTex(grav_form[1], grav_form[2]))
        self.wait()

        r_ge_R = Tex("r > R")
        r_ge_R.next_to(grav_form, RIGHT, buff=0.5)
        self.play(Write(r_ge_R))
        self.wait()

        self.play(ball.animate.move_to(DOWN))
        self.wait(2)

        mdash = Tex(r"m'")
        mdash.next_to(grav_form, UL, buff=1.5).shift(RIGHT)
        ar = Arrow(mdash.get_corner(DL), ORIGIN, buff=0.2, path_arc=PI / 4)
        ar.set_color(YELLOW)

        grav_form1 = Tex(r"g(r) = -\frac{Gm'}{r^2}")
        grav_form1.next_to(grav_form, DOWN, buff=1)
        self.play(Write(grav_form1), Write(mdash), Write(ar))
        self.play(ball.animate.move_to(ORIGIN + 0.1 * UP))
        self.wait()

        ball.vel = 0
        ball.y = radius
        ball.move_to(radius * UP)

        def update_ball(b, dt):
            b.vel += -b.y * dt
            b.y += b.vel * dt
            b.move_to(b.y * UP)

        ball.add_updater(update_ball)

        r_le_R = Tex("r < R")
        r_le_R.next_to(grav_form1, RIGHT, buff=0.85)
        self.play(Write(r_le_R))
        self.wait(2)
        self.play(
            grav_form1.animate.next_to(earth_cross_section, RIGHT, buff=1.5),
            FadeOut(grav_form),
            FadeOut(ar),
            FadeOut(r_ge_R),
            FadeOut(r_le_R),
            FadeOut(mdash),
        )
        self.wait()

        m_dash_form = VGroup(
            Tex(r"m' = \rho V"),
            Tex(r"m' = \rho \cdot \frac{4}{3}\pi r^3"),
            Tex(r"m' = \frac{M}{\frac{4}{3}\pi R^3} \cdot \frac{4}{3}\pi r^3"),
            Tex(r"m' = \frac{Mr^3}{R^3}"),
        )
        m_dash_form.next_to(grav_form1, DOWN, buff=0.5)
        self.play(Write(m_dash_form[0]))
        self.wait()
        self.play(TransformMatchingTex(m_dash_form[0], m_dash_form[1]))
        self.wait()
        self.play(TransformMatchingTex(m_dash_form[1], m_dash_form[2]))
        self.wait()
        self.play(TransformMatchingTex(m_dash_form[2], m_dash_form[3]))
        self.wait()

        grav_form2 = Tex(r"g(r) = -\frac{GMr}{R^3}")
        grav_form2.move_to(grav_form1)
        self.play(TransformMatchingParts(grav_form1, grav_form2), Uncreate(m_dash_form))
        self.wait()

        self.play(fr.animate.move_to(4 * LEFT))
        self.wait()

        grav_form3 = grav_form2.copy()[4:]
        grav_form3.next_to(d2r, buff=0.25)
        self.play(Write(grav_form3))
        self.wait()

        self.play(FadeOut(func_g), FadeOut(equals[0]))
        self.wait()

        diff_eq = VGroup(d2r, grav_form3)
        self.play(diff_eq.animate.to_edge(UP, buff=1).shift(LEFT))
        self.wait(2)

        sol_eq = VGroup(
            Tex(r"r(t) \propto \sin(\omega t) \text{ or} \cos(\omega t)"),
            TexText(r"where $\omega = \sqrt{\displaystyle\frac{GM}{R^3}}$"),
        )
        sol_eq.arrange(DOWN, buff=0.5)
        sol_eq.next_to(diff_eq, DOWN, buff=0.75)
        sol_eq.align_to(diff_eq, LEFT)
        self.play(Write(sol_eq[0][:5]), run_time=2)
        self.wait()
        self.play(Write(sol_eq[0][5:]), run_time=2)
        self.play(Write(sol_eq[1]))
        self.wait()

        self.play(fr.animate.move_to(4 * RIGHT), FadeOut(grav_form2))
        self.wait()

        axes = Axes(
            x_range=(0, TAU, 1),
            y_range=(-(radius + 1), radius + 1, 1),
            axis_config=dict(include_tip=True),
        )
        axes.next_to(earth_cross_section, RIGHT, buff=1)
        labels = axes.get_axis_labels(r"t", "r(t)")
        labels[0].next_to(axes.x_axis, RIGHT, buff=0).shift(0.15 * LEFT + 0.5 * DOWN)
        labels[1].next_to(axes.y_axis, UP, buff=0).shift(0.75 * LEFT + 0.5 * DOWN)
        self.play(ShowCreation(axes), Write(labels))

        self.wait_until(lambda: ball.get_y() > radius - 0.1)

        plot = VMobject()
        plot.set_opacity(0)
        self.delta = axes.c2p(0, 0)[0]
        plot.start_new_path(array([self.delta, ball.get_y(), 0]))

        def update_plot(p, dt):
            self.delta += dt / 2
            p.add_points_as_corners([array([self.delta, ball.get_y(), 0])])

        plot.add_updater(update_plot)
        plot.set_stroke(color=YELLOW_B, opacity=1)
        self.add(plot)
        self.wait(15)
        plot.clear_updaters()
        self.wait(2)


class OscillatorVectorField(Scene):
    def construct(self):
        fr = self.frame
        fr.set_width(25)

        pts = uniform(-0.01, 0.01, (int(1e6), 3))
        pts[:, 2] = 0
        dots = DotCloud(pts).set_color(CYAN)
        dots.set_radius(0.07)

        dots.f_always.set_points(
            lambda: get_oscillator_points(
                dots.get_points(), -1, 0.1, 0.25, 2.5, 2, self.time, n_steps=8
            )
        )

        field = self.get_field_vector(width=fr.get_width(), height=fr.get_height())

        self.add(dots)
        self.wait(40)
        self.bring_to_back(field)
        self.play(ShowCreation(field))
        self.wait(20)

        txt = Title("The Duffing Oscillator")
        txt.scale(2).set_color_by_gradient(CYAN, RED_B)
        eq = Tex(r"\ddot{x} + kx + \gamma \dot{x} + \beta x^3 = F_0\cos{\omega t}")
        eq.scale(2)

        self.play(FadeOut(dots), FadeOut(field), FadeIn(txt), FadeIn(eq), run_time=5)
        self.wait(2)
        self.play(
            Write(
                TexText(r"Equation of SHM: \\ $\ddot{x} + kx = 0$")
                .scale(1.5)
                .next_to(eq, DOWN, buff=2)
            )
        )
        self.wait()

    def get_field(
        self,
        pos: np.ndarray,
        k: float = 1,
        gamma: float = 0,
        beta: float = 0,
        f0: float = 0,
        omega: float = 0,
    ) -> np.ndarray:
        if pos.ndim == 1:
            pos = pos.reshape(-1, 3)
        x, v = pos[:, 0], pos[:, 1]
        dx = v
        dv = -k * x - gamma * v - beta * x**3 + f0 * cos(omega * self.time)
        return array([dx, dv]).T

    def get_field_vector(
        self,
        k=-1,
        gamma=0.1,
        beta=0.25,
        f0=2.5,
        omega=2,
        opacity=0.75,
        width=FRAME_WIDTH,
        height=FRAME_HEIGHT,
    ):
        return always_redraw(
            lambda: VectorField(
                lambda pos: self.get_field(
                    pos, k=k, gamma=gamma, beta=beta, f0=f0, omega=omega
                ),
                Axes(
                    x_range=(-width / 2, width / 2, 1),
                    y_range=(-height / 2, height / 2, 1),
                ),
                color_map=self.color_func,
            ).set_stroke(opacity=opacity)
        )

    @staticmethod
    def color_func(length):
        length = length.reshape(-1, 1)
        lmax = np.max(length)
        lmin = np.min(length)
        length = (length - lmin) / (lmax - lmin + 1e-8)
        return np.sqrt(
            interpolate(color_to_rgb(RED) ** 2, color_to_rgb(DARK_BLUE) ** 2, length)
        )


class PhaseSpaceDiagram(OscillatorVectorField):
    def construct(self):
        txt = Title("Simple Harmonic Motion").fix_in_frame()
        txt.set_color_by_gradient(DARK_BLUE, WHITE, DARK_BLUE)
        self.play(Write(txt))
        self.wait()

        sm = DuffingOscillator(k=1, pos=2, l0=0.5, base=LEFT)
        self.play(FadeIn(sm))
        self.wait()

        k_txt = Tex("k").next_to(sm.spring, UP, buff=0.25)
        m_txt = Tex("m = 1").next_to(sm.mass, UR, buff=0.25)
        v_txt = Tex(r"\overset{v}{\leftarrow}").next_to(sm.mass, UP, buff=0.25)

        self.play(Write(k_txt), Write(m_txt))
        self.play(FadeOut(m_txt), TransformMatchingTex(k_txt, v_txt))
        sm.start_simulation()
        self.play(FadeOut(v_txt))
        self.wait(10)

        eq1 = Tex(r"\ddot{x} = -kx")
        eq1.move_to(1.5 * DOWN)
        self.play(Write(eq1))
        self.wait(2)

        fr = self.frame
        self.play(fr.animate.move_to(4.5 * RIGHT))

        plane = NumberPlane(
            x_range=(-8, 8, 2), y_range=(-4, 4, 2), axis_config=dict(include_tip=True)
        )
        plane.fix_in_frame()
        plane.set_width(8).to_edge(RIGHT, buff=1)
        self.play(Write(plane))
        self.wait()

        dot = Dot().fix_in_frame()
        dot.f_always.move_to(lambda: plane.c2p(8 * sm.get_pos(), 4 * sm.get_momentum()))
        self.play(Write(dot))
        self.wait(2)

        trail = TracingTail(dot, 7, 4, stroke_opacity=1, stroke_color=YELLOW)
        trail.fix_in_frame()
        self.bring_to_back(trail)
        self.bring_to_back(plane)
        self.wait(2)

        labels = plane.get_axis_labels("x", "\\dot{x}").fix_in_frame()

        txt2 = Title("Phase Space Diagram").fix_in_frame()
        txt2.set_color_by_gradient(CYAN, RED_B)
        self.play(TransformMatchingTex(txt, txt2), Write(labels))
        self.wait(5)

        eq2 = Tex(r"\ddot{x} = -kx - \gamma \dot{x}")
        eq2.move_to(eq1)

        sm.set_gamma(0.2)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(5)

        eq3 = Tex(r"\ddot{x} = -kx - \gamma \dot{x} - \beta x^3")
        eq3.move_to(eq1)
        sm.set_beta(5)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(5)

        f_eq = Tex(r"+  \ F_0\cos{\omega t}")
        f_eq.set_width(2.35)
        f_eq.next_to(eq2, DOWN, buff=0.35)

        sm.set_external_force(lambda: 0.5 * cos(1.1 * self.time))

        self.play(Write(f_eq))
        self.wait(20)


class ChaosWithVectorField(OscillatorVectorField):
    def construct(self):
        field = self.get_field_vector()
        self.play(ShowCreation(field))

        vals = Tex(r"k = -1, \gamma = 0.1, \beta = 0.25, F_0 = 2.5, \omega = 2")
        vals.add_background_rectangle(BLACK, opacity=0.75, buff=0.15)
        self.play(ShowCreation(vals))
        self.wait()
        self.play(vals.animate.to_edge(UP, buff=0.35))

        dot = Dot(0.5 * RIGHT, fill_color=YELLOW)
        dot2 = Dot(0.51 * RIGHT, fill_color=CYAN)
        trail = TracingTail(dot, 7, 4, 1, YELLOW)
        trail2 = TracingTail(dot2, 7, 4, 1, CYAN)
        self.add(trail, trail2)
        self.play(ShowCreation(dot), ShowCreation(dot2))

        def update_dots(d):
            shift = self.get_field(d.get_center(), -1, 0.1, 0.25, 2.5, 2) / 50
            d.shift(np.hstack((shift[0], array([0]))))

        dot.add_updater(update_dots)
        dot2.add_updater(update_dots)
        self.wait(60)
