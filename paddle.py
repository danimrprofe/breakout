from gameobject import GameObject

class Paddle(GameObject):
    def __init__(self, canvas, x, y):

        self.width = 80
        self.height = 10
        self.ball = None
        item = canvas.create_rectangle(x - self.width / 2,
                                    y - self.height / 2,
                                    x + self.width / 2,
                                    y + self.height / 2,
                                    fill='blue')
        super(Paddle, self).__init__(canvas, item)
    def set_ball(self, ball):
        self.ball = ball
    def move(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
        if self.ball is not None:
            self.ball.move(offset, 0)
