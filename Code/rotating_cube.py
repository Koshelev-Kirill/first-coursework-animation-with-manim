from manim import *
import numpy as np

class RotatingCubeWithFormulas(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        side_length = 2
        half_side = side_length / 2

        faces_data = [
            {"center": [0, 0, half_side], "normal": [0, 0, 1], "name": "front", "formula": r"e^{i\pi} + 1 = 0"},
            {"center": [0, 0, -half_side], "normal": [0, 0, -1], "name": "back",
             "formula": r"\int_{-\infty}^{\infty} e^{-x^2}dx = \sqrt{\pi}"},
            {"center": [half_side, 0, 0], "normal": [1, 0, 0], "name": "right", "formula": r"\frac{d}{dx}e^x = e^x"},
            {"center": [-half_side, 0, 0], "normal": [-1, 0, 0], "name": "left",
             "formula": r"F = G\frac{m_1 m_2}{r^2}"},
            {"center": [0, half_side, 0], "normal": [0, 1, 0], "name": "top", "formula": r"E = mc^2"},
            {"center": [0, -half_side, 0], "normal": [0, -1, 0], "name": "bottom",
             "formula": r"\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}"},
        ]

        cube_group = VGroup()

        for face in faces_data:
            square = Square(side_length=side_length, color=BLUE, fill_opacity=0.3)
            square.move_to(face["center"])

            rotation_axis = np.array([0, 0, 1])
            angle = 0

            default_normal = np.array([0, 0, 1])
            target_normal = np.array(face["normal"])

            if not np.allclose(default_normal, target_normal):
                rotation_axis = np.cross(default_normal, target_normal)
                if np.linalg.norm(rotation_axis) > 0:
                    rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
                    angle = np.arccos(np.dot(default_normal, target_normal))
                    square.rotate(angle=angle, axis=rotation_axis)

            formula = MathTex(face["formula"], font_size=24, color=WHITE)

            formula.move_to(face["center"])
            offset = 0.01
            formula.shift(np.array(face["normal"]) * offset)

            if angle != 0:
                formula.rotate(angle=angle, axis=rotation_axis, about_point=face["center"])

            cube_group.add(square, formula)

        diagonal_vector = np.array([1, 1, 1])
        diagonal_vector = diagonal_vector / np.linalg.norm(diagonal_vector)

        target_vector = np.array([0, 0, 1])

        rotation_axis = np.cross(diagonal_vector, target_vector)
        if np.linalg.norm(rotation_axis) > 0:
            rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
            angle = np.arccos(np.dot(diagonal_vector, target_vector))

            cube_group.rotate(angle=angle, axis=rotation_axis)

        center_to_vertex = np.sqrt(3) * half_side
        cube_group.shift([0, 0, center_to_vertex])

        axis_length = 2 * center_to_vertex
        vertical_axis = Line(
            start=[0, 0, 0],
            end=[0, 0, axis_length],
            color=RED,
            stroke_width=3
        )

        self.add(vertical_axis)
        self.play(Create(cube_group), run_time=2)

        rotation_animation = Rotate(
            cube_group,
            angle=2 * PI,
            axis=Z_AXIS,
            about_point=[0, 0, 0],
            run_time=8,
            rate_func=linear
        )

        self.play(rotation_animation)
        self.wait(2)

# manim -pql rotating_cube.py RotatingCubeWithFormulas