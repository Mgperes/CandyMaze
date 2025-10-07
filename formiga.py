import pyxel

class Formiga:
    def __init__(self):

        
        self.x = 35
        self.y = 153
        self.largura = 18
        self.altura = 11
        self.x_mem = 197
        self.y_mem = 0
        self.direita = True
        self.v = 0  #velocidade
        self.i = 1  #imagem 1 da formiga (são duas imagens para simular movimento)

    def update(self):
        if self.x == 35:
            self.direita = True  #quando x for 835 (o inicial) ela se moverá para a direita
        if self.x == 197:
            self.direita = False  #quando x chegar a 197 o movimento inverte para a esquerda
        if self.direita == True:
            self.v = 1.5
            self.x += self.v
            self.direita = True
            self.y_mem = 11
        if self.direita == False:
            self.v = -(1.5)
            self.x += self.v
            self.direita = False
            self.y_mem = 0
        #desenho do movimento
        if self.v == 1.5 and self.i == 1:
            self.x_mem = 197
            self.i = 2
        else: 
            if self.v == 1.5:
                self.x_mem = 215
                self.i = 1
        if self.v == -(1.5) and self.i == 1:
            self.x_mem = 197
            self.i = 2
        else: 
            if self.v == -(1.5):
                self.x_mem = 215
                self.i = 1
        
    def draw(self):
        pyxel.blt(self.x, self.y, 1, self.x_mem, self.y_mem, 18, 11,7)