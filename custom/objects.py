from manimlib.mobject.geometry import Polygon, RegularPolygon

class Star(Polygon):
    def __init__(
            self,
            n: int = 6,
            inner_radius: float = 1.0,
            outer_radius: float = 2.0,
            **kwargs
    ):
        inner_polygon = RegularPolygon(n=n)
        outer_polygon = inner_polygon.copy()

        inner_polygon.scale(inner_radius)
        outer_polygon.scale(outer_radius)

        inner_dots = inner_polygon.get_points()[1::2]
        outer_dots = outer_polygon.get_points()[1::2]

        points = []

        for i in range(n):
            points.append(inner_dots[i])
            points.append(outer_dots[i])
        points.append(inner_dots[0])

        super().__init__(*points, **kwargs)
