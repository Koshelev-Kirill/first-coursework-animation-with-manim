from manim import *

class FirstScene(Scene):
    def construct(self):
        circle = Circle(color=BLUE, fill_opacity=0.5)
        text = MathTex(r"\text{Hello, Manim!}")
        text.next_to(circle, DOWN)
        self.play(Create(circle))
        self.play(Write(text))
        self.wait(2)
