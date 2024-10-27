# Varniex - CodingManim 09: Parametric Surfaces
# YouTube Video: https://youtu.be/pUC5a6XNEn4

from manim_imports import *


EARTH_DAY_TEXTURE = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Whole_world_-_land_and_oceans.jpg/1280px-Whole_world_-_land_and_oceans.jpg"

EARTH_NIGHT_TEXTURE = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/The_earth_at_night.jpg/1280px-The_earth_at_night.jpg"

SUN_TEXTURE = "https://commons.wikimedia.org/wiki/File:Solarsystemscope_texture_2k_sun.jpg"

MOON_TEXTURE = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Moon_texture.jpg/720px-Moon_texture.jpg"


class LorenzEvolution(InteractiveScene):
    def construct(self):
        frame = self.frame
        frame.reorient(45, 60)
        frame.scale(10).move_to(30 * OUT)

        num_particles = 100  # per axis
        ppa = linspace(-0.05, 0.05, num_particles)  # points per axis

        points = array([[x, y, z] for x in ppa for y in ppa for z in ppa])
        particles = DotCloud(points, radius=0.05, color=BLUE)

        particles.add_updater(
            lambda p, dt: p.set_points(self.update_lorenz(p.get_points(), dt))
        )
        self.add(particles)
        self.wait(60)

    @staticmethod
    def update_lorenz(points, dt: float = 1 / 60):
        a, b, c = 10, 28, 8 / 3

        x = points[:, 0]
        y = points[:, 1]
        z = points[:, 2]

        dx = (a * (y - x)) * dt
        dy = (x * (b - z) - y) * dt
        dz = (x * y - c * z) * dt

        x += dx
        y += dy
        z += dz

        return points


class SinCurve(InteractiveScene):
    def construct(self):
        curve = ParametricCurve(
            lambda t: [t, sin(t), 0],
            t_range=(-4, 4, 0.1),
        )
        curve.set_color_by_gradient(BLUE, WHITE, BLUE)
        self.play(ShowCreation(curve))
        self.wait()


class SinSurface(InteractiveScene):
    def construct(self):
        surface = ParametricSurface(
            lambda u, v: [u, v, sin(u)],
            u_range=(-4, 4),
            v_range=(-4, 4),
            resolution=(20, 20),
        )
        surface.set_color_by_gradient(BLUE, WHITE, BLUE)
        self.play(ShowCreation(surface))
        self.wait()


class SquareSheet(InteractiveScene):
    def construct(self):
        surface = ParametricSurface(
            lambda u, v: [u, v, 0], u_range=(-2, 2), v_range=(-2, 2)
        )
        surface.set_color_by_gradient(BLUE, WHITE, BLUE)
        self.play(ShowCreation(surface))
        self.wait()


class ParametricSurfacesScene(ThreeDScene):
    def construct(self):
        frame = self.frame
        frame.reorient(45, 60)
        frame.always.increment_theta(-0.25 * DEGREES)

        sin_surface1 = ParametricSurface(
            lambda u, v: [u, v, sin(u)],
            u_range=(-4, 4),
            v_range=(-4, 4),
        ).set_color_by_gradient(TEAL, WHITE, TEAL)
        self.play(ShowCreation(sin_surface1))
        self.wait()

        sin_surface2 = ParametricSurface(
            lambda u, v: [u, v, cos(v)],
            u_range=(-4, 4),
            v_range=(-4, 4),
        ).set_color_by_gradient(TEAL, WHITE, TEAL)
        self.play(ReplacementTransform(sin_surface1, sin_surface2))
        self.wait()

        paraboloid = ParametricSurface(
            lambda u, v: [u, v, u**2 + v**2],
            u_range=(-1, 1),
            v_range=(-1, 1),
        )

        # x, y, z = p
        # x = p[0], y = p[1], z = p[2]
        # z goes from 0 to 2
        paraboloid.set_color_by_rgba_func(
            lambda p: [
                r := (1 - p[2] / 2),
                g := abs(0.5 - p[2] / 2),
                b := p[2] / 2,
                a := 0.8,
            ]
        )

        self.play(ReplacementTransform(sin_surface2, paraboloid))
        self.wait(5)

        def get_wave_surface():
            return ParametricSurface(
                lambda u, v: [u, v, sin(u + self.time) * cos(v + self.time)],
                u_range=(-4, 4),
                v_range=(-4, 4),
            ).set_color_by_rgba_func(
                lambda p: [
                    1 - (p[2] + 1) / 2,
                    abs(0.5 - (p[2] + 1) / 2),
                    (p[2] + 1) / 2,
                    0.95,
                ]
            )

        wave = get_wave_surface()

        self.play(ReplacementTransform(paraboloid, wave))
        self.wait(5)

        wave_motion = always_redraw(get_wave_surface)
        self.play(ReplacementTransform(wave, wave_motion))
        self.wait(5)


class SpaceTimeCurvature(ThreeDScene):
    default_frame_orientation = (0, 90)

    def construct(self):
        sphere = Sphere()

        # Adding Earth
        earth = TexturedSurface(
            uv_surface=sphere,
            image_file=EARTH_DAY_TEXTURE,
            dark_image_file=EARTH_NIGHT_TEXTURE
        )
        self.add(earth)
        earth.rotate(23.5 * DEGREES, axis=UP)

        axis_line = rotate_vector(OUT, 23.5 * DEGREES, UP)

        # always_rotate(earth, 2 * DEGREES, axis=axis_line)
        earth.always.rotate(2 * DEGREES, axis=axis_line)
        self.wait(10)

        # Adding Sun
        sun_radius = 3.5
        sun = TexturedSurface(
            uv_surface=sphere.scale(sun_radius), image_file=SUN_TEXTURE, z_index=1
        )
        always_rotate(sun, 0.5 * DEGREES)
        self.add(sun)

        # adding sun glow
        glow = TrueDot(
            center=sun.get_center(),
            radius=sun_radius,
            color=YELLOW,
            glow_factor=1.5,
            z_index=2,
        )
        glow.f_always.move_to(sun.get_center)
        self.add(glow)

        # Adding Moon
        moon_radius = 0.25
        moon = TexturedSurface(
            uv_surface=sphere.scale(moon_radius), image_file=MOON_TEXTURE, z_index=-2
        )
        always_rotate(moon, 5 * DEGREES)
        self.add(moon)

        # start orbital motion
        earth.f_always.move_to(
            lambda: self.get_orbital_position(sun.get_center(), 3.5, 0.5)
        )
        moon.f_always.move_to(
            lambda: self.get_orbital_position(earth.get_center(), 0.5, 5, 5)
        )

        # adding plane curvature
        grid = TexturedSurface(
            ParametricSurface(
                lambda u, v: [u, v, 0], u_range=(-20, 20), v_range=(-20, 20)
            ),
            image_file="grid",
            z_index=-99,
        ).move_to(1.5 * IN)

        grid.set_shading(reflectiveness=0.1, gloss=0.1)
        self.play(ShowCreation(grid))
        self.wait(10)

        def update_grid_curvature(points):
            x = points[:, 0]
            y = points[:, 1]

            z_sun = self.warp_function((x, y), sun.get_center()[:2], 5.5, 50)
            z_earth = self.warp_function((x, y), earth.get_center()[:2], 0.5, 0.8)
            z_moon = self.warp_function((x, y), moon.get_center()[:2], 0.1, 0.1)

            points[:, 2] = 0.5 + z_sun + z_earth + z_moon
            return points

        grid.add_updater(lambda p: p.set_points(update_grid_curvature(p.get_points())))

        # frame following the earth
        frame = self.frame
        frame.reorient(0, 60).set_width(10)
        frame.f_always.move_to(earth.get_center)
        frame.f_always.set_theta(lambda: angle_of_vector(earth.get_center()) + PI / 4)
        self.wait(60)

    @staticmethod
    def warp_function(point, center, mass, radius):
        num = (center[0] - point[0])**2 + (center[1] - point[1])**2
        return -mass * exp(-num / radius)

    def get_orbital_position(self, center, radius, omega, tilt=0):
        # I found out later that there's actually a 5 degree tilt
        # in the orbital plane of the moon that I forgot in the code.
        # So, here's the updated one!

        t = self.time
        orbit_position = rotate_vector(
            vector=radius * array([cos(omega * t), sin(omega * t), 0]),
            angle=tilt * DEGREES,
            axis=UP,
        )
        return center + orbit_position


class ThreeDAxesDemonstration(ThreeDScene):
    """
    ThreeDAxes is an extention to the Axes class.
    You have one more axis (z-axis) to configure with.
    Everything else works the same.
    """
    default_frame_orientation = (45, 60)

    def construct(self):
        three_d_axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(-5, 5, 1),
            axis_config=dict(include_tip=True, include_numbers=True),
        )
        # to add labels
        three_d_axes.add_axis_labels(font_size=48)

        self.play(ShowCreation(three_d_axes))
        self.wait()

        surface = three_d_axes.get_parametric_surface(...)
