from manim import *

class FirstScene(Scene):
    def construct(self):
        # Создаем круг
        circle = Circle(color=BLUE, fill_opacity=0.5)
        # Создаем надпись с LaTeX
        text = MathTex(r"\text{Hello, Manim!}")
        # Располагаем текст под кругом
        text.next_to(circle, DOWN)

        # Анимация: проявление круга и текста
        self.play(Create(circle))
        self.play(Write(text))
        # Пауза в конце
        self.wait(2)