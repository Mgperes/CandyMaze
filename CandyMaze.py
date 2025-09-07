import pyxel


#----------------- Start -------------------#
class Start:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 250
        self.height = 180
    def update_conect(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.start = False
            

    def desenhastart(self):
        pyxel.cls(0)
        pyxel.blt(0, 0, 0, 0, 0, 250, 180)
        pyxel.text(80, 109, "(Q)uit", 7)
        pyxel.text(80, 119, "(Enter ou Espaço) Start", 7)




#----------------- Personagem -------------------#
class Personagem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 14
        self.altura = 18
        self.x_mem = 0
        self.contX = 0
        self.y_mem = 0
        self.contY = 0
        

    def move(self, dx, dy):
        self.x_mem = self.contX * self.largura
        self.contX = (self.contX + 1) % 4

        if dy > 0: # indo para baixo, linha 0
            self.contY = 0

        if dy < 0: # indo para cima, linha 1
            self.contY = 1

        if dx > 0: # indo para direita, linha 2
            self.contY = 3

        if dx < 0: # indo para esquerda, linha 3
            self.contY = 2

        self.y_mem = self.contY * self.altura
            

        self.x += dx
        self.y += dy

#----------------- Desenha o personagem -------------------#
    def desenhapersonagem(self):

        pyxel.blt(self.x, self.y, 1, self.x_mem, self.y_mem, self.largura, self.altura, 7)



#----------------- CandyMazeGame -------------------#
class CandyMazeGame:
    def __init__(self):
        pyxel.init(250, 180, title="CandyMaze", fps=30, quit_key=pyxel.KEY_Q)

        self.start = True
        self.personagem = Personagem(56, 72)
        #-------- carrega as imagens --------#
        pyxel.images[0].load(0, 0, "background.png")
        pyxel.images[1].load(0, 0, "personagem56x72(14x18_cada)")

    
        pyxel.run(self.update, self.draw)






    def update(self):
        pass

    # ------------------- Movimento do personagem -------------------#
        #dx = 0
        #dy = 0

        #if pyxel.btn(pyxel.KEY_UP):
         #   dy -= 4
        #if pyxel.btn(pyxel.KEY_DOWN):
         #   dy += 4
        #if pyxel.btn(pyxel.KEY_LEFT):
         #   dx -= 4
        #if pyxel.btn(pyxel.KEY_RIGHT):
         #   dx += 4


        #if dx != 0 or dy != 0:
         #   self.personagem.move(dx, dy)

          #  for parede in self.paredes:
           #     if self.colisao(self.personagem, parede):
            #     # Se houver colisão, reverte o movimento
             #       self.personagem.move(-dx, -dy)
              #      break

    def draw(self):

        if self.start == True:
            Start().desenhastart()
            Start().update_conect()
        else:
            pyxel.cls(0)
            pyxel.blt(0, 0, 0, 0, 0, 250, 180)
            self.personagem.desenhapersonagem()

CandyMazeGame()