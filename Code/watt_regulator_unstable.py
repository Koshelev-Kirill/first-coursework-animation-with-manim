import numpy as np
from manim import *

config.frame_rate = 30
config.pixel_width = 1280
config.pixel_height = 720
config.max_files_cached = 100
config.background_color = WHITE


class WattRegulatorAttractor_Unstable(ThreeDScene):
    def construct(self):
        alpha = 20
        gamma = 20
        beta = 20
        J = 1.0
        G = 2.75
        m = 1.0
        r = 1.0

        omega0 = 1.5
        x0 = 1.5
        v0 = 0.0

        def arccoth_safe(x):
            if x >= 1:
                x = min(x, 1.01)
            elif x <= -1:
                x = max(x, -1.01)
            else:
                x = 1.01 if x >= 0 else -1.01
            return 0.5 * np.log((x + 1) / (x - 1))

        def watt_system(state):
            omega, x, v = state
            omega = np.clip(omega, -100, 100)
            v = np.clip(v, -100, 100)
            if abs(x) <= 1.0:
                x = 1.01 if x >= 0 else -1.01
            domega_dt = (arccoth_safe(x) - G) / J
            dx_dt = v
            dv_dt = (beta * m * (x + r) * omega ** 2 - alpha * v - gamma * x) / m
            return np.array([domega_dt, dx_dt, dv_dt])

        # Интегрирование
        dt, total_steps = 0.02, 1200
        states = []
        current_state = np.array([omega0, x0, v0])
        for _ in range(total_steps):
            states.append(current_state.copy())
            current_state += watt_system(current_state) * dt

        omega_vals = np.array([s[0] for s in states])
        x_vals = np.array([s[1] for s in states])
        v_vals = np.array([s[2] for s in states])


        x_min, x_max = x_vals.min(), x_vals.max()
        v_min, v_max = v_vals.min(), v_vals.max()
        omega_min, omega_max = omega_vals.min(), omega_vals.max()


        def add_margin(mn, mx, margin=0.2):
            if mn == mx:
                return mn - 1, mx + 1
            rng = mx - mn
            return mn - margin * rng, mx + margin * rng

        x_min, x_max = add_margin(x_min, x_max)
        v_min, v_max = add_margin(v_min, v_max)
        omega_min, omega_max = add_margin(omega_min, omega_max)

        def nice_step(mn, mx, ticks=5):
            rng = mx - mn
            if rng <= 0:
                return 1.0
            step = rng / ticks
            mag = 10 ** np.floor(np.log10(step))
            return np.ceil(step / mag) * mag

        # Оси
        axes = ThreeDAxes(
            x_range=[x_min, x_max, nice_step(x_min, x_max)],
            y_range=[v_min, v_max, nice_step(v_min, v_max)],
            z_range=[omega_min, omega_max, nice_step(omega_min, omega_max)],
            x_length=config.frame_width * 0.4,
            y_length=config.frame_width * 0.4,
            z_length=config.frame_width * 0.4,
            axis_config={"color": BLACK}
        )

        axes_labels = axes.get_axis_labels(
            MathTex("x(t)").scale(0.6).set_color(BLACK),
            MathTex("v(t)").scale(0.6).set_color(BLACK),
            MathTex(r"\omega(t)").scale(0.6).set_color(BLACK)
        )

        # Сдвиг вниз
        shift_down = 0
        axes.shift([0, 0, -shift_down])
        axes_labels.shift([0, 0, -shift_down])


        # Траектория
        points_3d = []
        for i in range(len(states)):
            xv, vv, omv = x_vals[i], v_vals[i], omega_vals[i]
            if x_min <= xv <= x_max and v_min <= vv <= v_max and omega_min <= omv <= omega_max:
                points_3d.append(axes.coords_to_point(xv, vv, omv))

        points_3d = points_3d[::2]  # прореживание для скорости

        trajectory = VMobject(stroke_width=2)
        trajectory.set_points_smoothly(points_3d)
        trajectory.set_color_by_gradient(BLUE, GREEN, RED, PURPLE)

        # Анимация
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, axes_labels)
        self.play(Create(trajectory), run_time=8, rate_func=linear)
        self.begin_ambient_camera_rotation(rate=12 * DEGREES)
        self.wait(12)
        self.stop_ambient_camera_rotation()
        self.wait(2)


        # manim -pql watt_regulator_unstable.py WattRegulatorAttractor_Unstable
