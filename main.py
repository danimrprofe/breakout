import tkinter as tk
from paddle import *
from ball import *
from brick import *

class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.vidas = 3
        
        # Configuramos la ventana de juego

        self.width = 610
        self.height = 400
        self.colorFondo ='#aaaaff'

        self.canvas = tk.Canvas(self, bg=self.colorFondo, width=self.width, height=self.height)
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.pelota = None
        self.paddle = Paddle(self.canvas, self.width/2, 326)
        self.items[self.paddle.item] = self.paddle
        
        # Vamos a colocar todos los ladrillos. 
        # La fila final resiste 2 golpes

        for x in range(5, self.width - 5, 75):
            self.add_brick(x + 37.5, 50, 2)
            self.add_brick(x + 37.5, 70, 1)
            self.add_brick(x + 37.5, 90, 1)
        
        self.hud = None
        self.setup_game()
        self.canvas.focus_set()
        self.canvas.bind('<Left>',  lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>', lambda _: self.paddle.move(10))
    
    def add_ball(self):
        if self.pelota is not None:
            self.pelota.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.pelota = Ball(self.canvas, x, 310)
        self.paddle.set_ball(self.pelota)
    
    def add_brick(self, x, y, hits):
        '''Agregamos un bloque'''
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def draw_text(self, x, y, text, size='20'):
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=text, font=font)
    
    def update_lives_text(self):
        text = 'Vidas: %s' % self.vidas
        if self.hud is None:
            self.hud = self.draw_text(50, 20, text, 15)
        else:
            self.canvas.itemconfig(self.hud, text=text)



    def check_collisions(self):
        ball_coords = self.pelota.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.pelota.collide(objects)

    def game_loop(self):
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:
            self.pelota.speed = None
            self.draw_text(300, 200, 'Has ganado!')
        elif self.pelota.get_position()[3] >= self.height:
            self.pelota.speed = None
            self.vidas -= 1
            if self.vidas < 0:
                self.draw_text(300, 200, 'Game Over')
            else:
                self.after(1000, self.setup_game)
        else:
            self.pelota.update()
            self.after(50, self.game_loop)

    def start_game(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()
    
    def setup_game(self):
        
        self.add_ball()
        self.update_lives_text()
        self.text = self.draw_text(300, 200, 'Presiona ESPACIO para comenzar')
        self.canvas.bind('<space>', lambda _: self.start_game())
    

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Hello, Pong!')
    game = Game(root)
    game.mainloop()