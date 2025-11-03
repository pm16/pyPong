import pyglet
import random


class Rect:
    x: int
    y: int
    width: int
    height: int

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Paddle:
    rect: Rect
    velocity: float = 0
    batch: pyglet.graphics.Batch
    graphic: pyglet.shapes.Rectangle

    def __init__(self, x: int, y: int, batch: pyglet.graphics.Batch):
        self.rect = Rect(x, y, 5, 40)
        self.batch = batch
        self.graphic = pyglet.shapes.Rectangle(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
            batch=self.batch,
        )

    def update(self):
        self.graphic.x = self.rect.x
        self.graphic.y = self.rect.y
        self.graphic.width = self.rect.width
        self.graphic.height = self.rect.height


class Ball:
    x: int
    y: int
    x_velocity: float = 0
    y_velocity: float = 0
    radius: int = 5
    batch: pyglet.graphics.Batch
    graphic: pyglet.shapes.Circle
    rect: Rect

    def __init__(self, x: int, y: int, batch: pyglet.graphics.Batch):
        self.x = x
        self.y = y
        self.batch = batch
        self.graphic = pyglet.shapes.Circle(
            self.x, self.y, self.radius, batch=self.batch
        )
        self.rect = Rect(self.x, self.y, self.x + self.radius, self.y + self.radius)

    def update(self):
        self.graphic.x = self.rect.x
        self.graphic.y = self.rect.y
        self.rect.width = self.rect.x + self.radius
        self.rect.height = self.rect.y + self.radius


class Game:
    game_start: bool = False
    max_velocity: float = 40


window = pyglet.window.Window(800, 450)
batch = pyglet.graphics.Batch()

paddle_one = Paddle(x=0, y=int(window.height / 2), batch=batch)
paddle_two = Paddle(x=window.width - 5, y=int(window.height / 2), batch=batch)
ball_one = Ball(x=int(window.width / 2), y=int(window.height / 2), batch=batch)
game = Game()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.A:
        paddle_one.velocity += 10

    if symbol == pyglet.window.key.Z:
        paddle_one.velocity -= 10

    if symbol == pyglet.window.key.SPACE:
        if not game.game_start:
            ball_one.x_velocity = random.randint(
                -int(game.max_velocity), int(game.max_velocity)
            )
            ball_one.y_velocity = random.randint(
                -int(game.max_velocity), int(game.max_velocity)
            )
            game.game_start = True


@window.event
def on_draw():
    window.clear()
    batch.draw()


def check_collision(r1: Rect, r2: Rect) -> bool:
    return (
        r1.x + r1.width >= r2.x
        and r1.x <= r2.x + r2.width
        and r1.y + r1.height >= r2.y
        and r1.y <= r2.y + r2.height
    )


def update(dt):
    if game.game_start:
        if abs(ball_one.x_velocity) < game.max_velocity:
            ball_one.x_velocity *= 1.01
        if abs(ball_one.y_velocity) < game.max_velocity:
            ball_one.y_velocity *= 1.01
    paddle_one.rect.y += paddle_one.velocity * dt
    paddle_two.rect.y += paddle_two.velocity * dt
    paddle_one.update()
    paddle_two.update()
    ball_one.rect.x += ball_one.x_velocity * dt
    ball_one.rect.y += ball_one.y_velocity * dt
    if ball_one.rect.y > window.height - 5:
        ball_one.y_velocity = -ball_one.y_velocity
    if ball_one.rect.y < 0 + 5:
        ball_one.y_velocity = -ball_one.y_velocity
    if check_collision(paddle_one.rect, ball_one.rect):
        ball_one.x_velocity = -ball_one.x_velocity
    if check_collision(paddle_two.rect, ball_one.rect):
        ball_one.x_velocity = -ball_one.x_velocity
    ball_one.update()


pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run()
