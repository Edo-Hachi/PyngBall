import pyxel
import math

# Screen size
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 256

# Ball settings
BALL_RADIUS = 4
GRAVITY = 0.2

# Flipper settings
FLIPPER_WIDTH = 4

class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pinball Flipper Test")

        # Ball
        self.reset_ball()

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

    def reset_ball(self):
        """Resets the ball to its initial position"""
        self.ball_x = pyxel.rndi(40, SCREEN_WIDTH - 40)
        self.ball_y = 40
        self.ball_vx = pyxel.rndf(-1, 1)
        self.ball_vy = 1.0

    def update(self):
        # Ball physics
        self.ball_vy += GRAVITY
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # Wall collision
        if self.ball_x <= BALL_RADIUS or self.ball_x >= SCREEN_WIDTH - BALL_RADIUS:
            self.ball_vx *= -0.9
            self.ball_x = max(BALL_RADIUS, min(self.ball_x, SCREEN_WIDTH - BALL_RADIUS))

        if self.ball_y <= BALL_RADIUS:
            self.ball_vy *= -0.9
            self.ball_y = BALL_RADIUS
        
        # Reset if falls off screen
        if self.ball_y >= SCREEN_HEIGHT + BALL_RADIUS * 2:
            self.reset_ball()

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

        # Ball and flipper collision detection
        self.check_flipper_collision()

    def check_flipper_collision(self):
        """Checks for collision between the ball and flippers and bounces the ball back"""
        # Left Flipper
        flipper_x1, flipper_y1 = self.left_flipper_pivot
        flipper_x2 = flipper_x1 + math.cos(self.left_flipper_angle) * self.left_flipper_length
        flipper_y2 = flipper_y1 + math.sin(self.left_flipper_angle) * self.left_flipper_length
        
        dist = self.dist_point_to_line(self.ball_x, self.ball_y, flipper_x1, flipper_y1, flipper_x2, flipper_y2)
        if dist < BALL_RADIUS + FLIPPER_WIDTH / 2:
            self.ball_vy = -abs(self.ball_vy) * 1.1 - 3 # Bounce upwards strongly
            self.ball_vx += (self.ball_x - flipper_x1) * 0.1 # Change horizontal velocity based on where it hit the flipper

        # Right Flipper
        flipper_x1, flipper_y1 = self.right_flipper_pivot
        flipper_x2 = flipper_x1 + math.cos(self.right_flipper_angle) * self.right_flipper_length
        flipper_y2 = flipper_y1 + math.sin(self.right_flipper_angle) * self.right_flipper_length

        dist = self.dist_point_to_line(self.ball_x, self.ball_y, flipper_x1, flipper_y1, flipper_x2, flipper_y2)
        if dist < BALL_RADIUS + FLIPPER_WIDTH / 2:
            self.ball_vy = -abs(self.ball_vy) * 1.1 - 3
            self.ball_vx += (self.ball_x - flipper_x1) * 0.1

    def dist_point_to_line(self, px, py, x1, y1, x2, y2):
        """Calculates the distance between a point (px, py) and a line segment (x1, y1)-(x2, y2) (simplified version)"""
        # For simplicity, substitute with the distance to the midpoint of the line segment
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        return math.sqrt((px - cx)**2 + (py - cy)**2)

    def draw(self):
        pyxel.cls(0)

        # Draw Ball
        pyxel.circ(self.ball_x, self.ball_y, BALL_RADIUS, 8)

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
