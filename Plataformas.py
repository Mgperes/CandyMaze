import pyxel

class Plataforma1:
    def __init__(self):
        self.x = 87
        self.y = 42
        self.direita = True
    def update(self):
        if self.x == 87:
            self.direita = True  #quando x for 87 (o inicial) ela se moverá para a direita
        if self.x == 153:
            self.direita = False  #quando x chegar a 153 o movimento inverte para a esquerda
        if self.direita == True:   
            self.x += 2
            self.direita = True
        if self.direita == False:
            self.x -= 2
            self.direita = False
    def draw(self):
        pyxel.blt(self.x, self.y, 1, 56, 32, 24, 8,7)

class Plataforma2:
    def __init__(self):
        self.x = 100
        self.y = 116
        self.direita = True
    def update(self):
        if self.x == 100:
            self.direita = True
        if self.x == 190:
            self.direita = False
        if self.direita == True:
            self.x += 2
            self.direita = True
        if self.direita == False:
            self.x -= 2
            self.direita = False
    def draw(self):
        pyxel.blt(self.x, self.y, 1, 56, 8, 50, 8, 7)