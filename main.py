import pyxel
import math

class Game:
    def __init__(self):
        pyxel.init(128, 256, title="Pinball Flipper Test")

        # Left Flipper
        self.left_flipper_pivot = (28, 240)
        self.left_flipper_length = 30
        self.left_flipper_angle_rest = math.atan2(-10, 30) + math.radians(30)
        self.left_flipper_angle_up = self.left_flipper_angle_rest - math.radians(30)
        self.left_flipper_angle = self.left_flipper_angle_rest

        # Right Flipper
        self.right_flipper_pivot = (100, 240)
        self.right_flipper_length = 30
        self.right_flipper_angle_rest = math.atan2(-10, -30) - math.radians(30)
        self.right_flipper_angle_up = self.right_flipper_angle_rest + math.radians(30)
        self.right_flipper_angle = self.right_flipper_angle_rest

        pyxel.run(self.update, self.draw)

    def update(self):
        # Left Flipper Controls
        if pyxel.btn(pyxel.KEY_Z):
            self.left_flipper_angle = self.left_flipper_angle_up
        else:
            self.left_flipper_angle = self.left_flipper_angle_rest

        # Right Flipper Controls
        if pyxel.btn(pyxel.KEY_X):
            self.right_flipper_angle = self.right_flipper_angle_up
        else:
            self.right_flipper_angle = self.right_flipper_angle_rest

    def draw(self):
        pyxel.cls(0)

        # Draw Left Flipper
        left_end_x = self.left_flipper_pivot[0] + self.left_flipper_length * math.cos(self.left_flipper_angle)
        left_end_y = self.left_flipper_pivot[1] + self.left_flipper_length * math.sin(self.left_flipper_angle)
        pyxel.line(
            self.left_flipper_pivot[0], self.left_flipper_pivot[1],
            left_end_x, left_end_y,
            7
        )

        # Draw Right Flipper
        right_end_x = self.right_flipper_pivot[0] + self.right_flipper_length * math.cos(self.right_flipper_angle)
        right_end_y = self.right_flipper_pivot[1] + self.right_flipper_length * math.sin(self.right_flipper_angle)
        pyxel.line(
            self.right_flipper_pivot[0], self.right_flipper_pivot[1],
            right_end_x, right_end_y,
            7
        )

Game()
