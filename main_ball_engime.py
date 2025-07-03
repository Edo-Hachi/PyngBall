import pyxel
import math

# 画面サイズ
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 240

# ボールの設定
BALL_RADIUS = 4
GRAVITY = 0.2

# フリッパーの設定
FLIPPER_LENGTH = 25
FLIPPER_WIDTH = 4
FLIPPER_SPEED = 0.3

# ゲーム状態定数
STATE_READY = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Pinball", fps=60)

        self.reset_ball()

        # フリッパーの角度（ラジアン）
        self.left_flipper_angle = 0.7
        
        # フリッパーの初期静止角度
        self.LEFT_FLIPPER_REST_ANGLE = 0.7
        self.RIGHT_FLIPPER_REST_ANGLE = math.pi - self.LEFT_FLIPPER_REST_ANGLE
        
        # フリッパーが上がった時の角度
        self.LEFT_FLIPPER_ACTIVE_ANGLE = -0.3
        self.RIGHT_FLIPPER_ACTIVE_ANGLE = math.pi - self.LEFT_FLIPPER_ACTIVE_ANGLE

        # 右フリッパーの初期角度を静止位置に設定
        self.right_flipper_angle = self.RIGHT_FLIPPER_REST_ANGLE

        self.launcher_power = 1

        # ゲーム状態の初期化
        self.game_state = STATE_READY

        pyxel.run(self.update, self.draw)

    def reset_ball(self):
        """ボールを初期位置に戻す"""
        self.ball_x = pyxel.rndi(40, SCREEN_WIDTH - 40)
        self.ball_y = 40
        self.ball_vx = pyxel.rndf(-1, 1)
        self.ball_vy = 1.0

    def update(self):
        # ボールの物理演算
        self.ball_vy += GRAVITY
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # 壁との衝突判定
        if self.ball_x <= BALL_RADIUS or self.ball_x >= SCREEN_WIDTH - BALL_RADIUS:
            self.ball_vx *= -0.9
            self.ball_x = max(BALL_RADIUS, min(self.ball_x, SCREEN_WIDTH - BALL_RADIUS))

        if self.ball_y <= BALL_RADIUS:
            self.ball_vy *= -0.9
            self.ball_y = BALL_RADIUS
        
        # 落下したらリセット
        if self.ball_y >= SCREEN_HEIGHT + BALL_RADIUS * 2:
            self.reset_ball()

        # フリッパーの操作（アニメーションで徐々に動かす）
        FLIPPER_ANIMATION_SPEED = 0.18
        # 左フリッパー (Zキー)
        if pyxel.btn(pyxel.KEY_Z):
            self.left_flipper_angle += (self.LEFT_FLIPPER_ACTIVE_ANGLE - self.left_flipper_angle) * FLIPPER_ANIMATION_SPEED
        else:
            self.left_flipper_angle += (self.LEFT_FLIPPER_REST_ANGLE - self.left_flipper_angle) * FLIPPER_ANIMATION_SPEED

        # 右フリッパー (Xキー)
        if pyxel.btn(pyxel.KEY_X):
            self.right_flipper_angle += (self.RIGHT_FLIPPER_ACTIVE_ANGLE - self.right_flipper_angle) * FLIPPER_ANIMATION_SPEED
        else:
            self.right_flipper_angle += (self.RIGHT_FLIPPER_REST_ANGLE - self.right_flipper_angle) * FLIPPER_ANIMATION_SPEED
        
        # ボールとフリッパーの衝突判定（簡易版）
        self.check_flipper_collision()

    def check_flipper_collision(self):
        """ボールとフリッパーの衝突をチェックしてボールを跳ね返す"""
        # 左フリッパー
        flipper_x1, flipper_y1 = 40, 200
        flipper_x2 = flipper_x1 + pyxel.cos(self.left_flipper_angle) * FLIPPER_LENGTH
        flipper_y2 = flipper_y1 + pyxel.sin(self.left_flipper_angle) * FLIPPER_LENGTH
        
        dist = self.dist_point_to_line(self.ball_x, self.ball_y, flipper_x1, flipper_y1, flipper_x2, flipper_y2)
        if dist < BALL_RADIUS + FLIPPER_WIDTH / 2:
            self.ball_vy = -abs(self.ball_vy) * 1.1 - 3 # 上向きに強く跳ね返す
            self.ball_vx += (self.ball_x - flipper_x1) * 0.1 # フリッパーの当たった場所で横方向の速度を変える

        # 右フリッパー
        flipper_x1, flipper_y1 = SCREEN_WIDTH - 40, 200
        flipper_x2 = flipper_x1 + pyxel.cos(self.right_flipper_angle) * FLIPPER_LENGTH
        flipper_y2 = flipper_y1 + pyxel.sin(self.right_flipper_angle) * FLIPPER_LENGTH

        dist = self.dist_point_to_line(self.ball_x, self.ball_y, flipper_x1, flipper_y1, flipper_x2, flipper_y2)
        if dist < BALL_RADIUS + FLIPPER_WIDTH / 2:
            self.ball_vy = -abs(self.ball_vy) * 1.1 - 3
            self.ball_vx += (self.ball_x - flipper_x1) * 0.1

    def dist_point_to_line(self, px, py, x1, y1, x2, y2):
        """点(px, py)と線分(x1, y1)-(x2, y2)の距離を計算する（簡易版）"""
        # 簡単のため、線分の中点との距離で代用
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        return pyxel.sqrt((px - cx)**2 + (py - cy)**2)

    def draw(self):
        pyxel.cls(7)  # 背景を白でクリア

        # 壁とランチャーレーン
        pyxel.rect(SCREEN_WIDTH - 25, 100, 25, SCREEN_HEIGHT, 13) # ランチャーレーン
        pyxel.line(SCREEN_WIDTH - 25, 100, SCREEN_WIDTH - 25, SCREEN_HEIGHT, 1) # レーンの壁

        # ランチャー
        launcher_y = SCREEN_HEIGHT - 10 - self.launcher_power
        pyxel.rect(SCREEN_WIDTH - 20, launcher_y, 15, 5, 8)

        # ボールを描画
        pyxel.circ(self.ball_x, self.ball_y, BALL_RADIUS, 8)

        # フリッパーを描画
        # 左
        pyxel.line(40, 200, 
                   40 + pyxel.cos(self.left_flipper_angle) * FLIPPER_LENGTH, 
                   200 + pyxel.sin(self.left_flipper_angle) * FLIPPER_LENGTH, 
                   2)
        # 右
        pyxel.line(SCREEN_WIDTH - 40, 200, 
                   SCREEN_WIDTH - 40 + pyxel.cos(self.right_flipper_angle) * FLIPPER_LENGTH, 
                   200 + pyxel.sin(self.right_flipper_angle) * FLIPPER_LENGTH, 
                   2)
        
        # 操作説明
        pyxel.text(5, 5, "Z/X: Flippers", 0)
        if self.game_state == STATE_READY:
            pyxel.text(5, 15, "DOWN: Charge & Launch", 0)

App()