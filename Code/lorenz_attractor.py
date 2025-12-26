import numpy as np
from manim import *

config.frame_rate = 30
config.pixel_width = 1280
config.pixel_height = 720
config.max_files_cached = 100

class LorenzAttractor(ThreeDScene):
    def construct(self):
        sigma, rho, beta = 10, 28, 8 / 3
        x, y, z = 0.1, 0, 0

        def lorenz_system(point):
            x, y, z = point[0], point[1], point[2]
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            return np.array([dx, dy, dz])

        dt = 0.01
        points = []
        current_point = np.array([x, y, z])
        for _ in range(2000):
            points.append(current_point.copy())
            current_point += lorenz_system(current_point) * dt

        lorenz_points = [p for p in points]

        axes = ThreeDAxes(
            x_range=[-25, 25, 10],
            y_range=[-25, 25, 10],
            z_range=[0, 50, 10],
            x_length=config.frame_width * 0.4,
            y_length=config.frame_width * 0.4,
            z_length=config.frame_width * 0.4,
        )
        axes_labels = axes.get_axis_labels(
            Text("X").scale(0.5), Text("Y").scale(0.5), Text("Z").scale(0.5)
        )

        self.set_camera_orientation(phi=75 * DEGREES, theta=-40 * DEGREES)

        shift_vector = np.array([0, 0, -2.7])
        axes.shift(shift_vector)
        axes_labels.shift(shift_vector)

        trajectory = ParametricFunction(
            lambda t: axes.coords_to_point(*points[int(t * (len(points) - 1))]),
            t_range=[0, 1, 1 / (len(points) - 1)],
            color=BLUE,
            stroke_width=1.5
        )

        self.add(axes, axes_labels)
        self.play(Create(trajectory), run_time=8)

        self.begin_ambient_camera_rotation(rate=16 * DEGREES)
        self.wait(14)