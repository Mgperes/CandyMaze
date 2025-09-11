import pyxel


#----------------- Start ---------------------------------------------------------------------------------#
class Start:
    def __init__(self):
        self.colortext = 7
        self.hover_timer = 0
        self.x = 0
        self.y = 0
        self.width = 250
        self.height = 180


    def update_conect(self):

        # Área do botão Start (ajuste conforme o texto)
        start_x = 97
        start_y = 119
        start_w = 110
        start_h = 10
        mouse_over_start = (
            start_x <= pyxel.mouse_x <= start_x + start_w and
            start_y <= pyxel.mouse_y <= start_y + start_h
        )

        mouse_over_quit = (130 <= pyxel.mouse_x <= 130 + 50 and
                           119 <= pyxel.mouse_y <= 119 + 10
                           )
        

        # Clique em QUIT ou aperte o "Q "para fechar o jogo
        if mouse_over_quit and (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_Q)):
            pyxel.quit()
        # Clique em ENTER ou ESPAÇO para iniciar
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            return False
    
        # Clique do mouse inicia o jogo se estiver sobre o texto Start
        if mouse_over_start and (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
            self.hover_timer += 1
            if self.hover_timer > 10:
                self.colortext = 8  # cor diferente
            else:
                self.colortext = 7
                return False
        return True

    def desenhastart(self):
        pyxel.cls(8)
        pyxel.blt(0, 0, 0, 0, 0, 250, 180)  
        pyxel.text(130, 119, "(Q)UIT", pyxel.frame_count % 8)
        pyxel.text(97, 119, "START |", pyxel.frame_count % 8)
        # Desenha cursor do mouse customizado
        pyxel.mouse(True)
        

#----------------- FASE 1 ----------------------------------------------------------------------------------------#

class Fase1:
    def __init__(self):
        self.colortext = 7
        self.pontos = 0
        self.personagem = Personagem(56, 72)
        self.x = 0
        self.y = 0
        self.colisao = False

    def update_fase1(self):
        
        #---------------------- Personagem não sumir da tela ----------------------#
        if self.colisao == True:
            self.x = self.x - dx
            self.y = self.y - dy
        if self.personagem.x < 0:
            self.personagem.x = 0
        if self.personagem.x + self.personagem.largura > 250:
            self.personagem.x = 250 - self.personagem.largura
        if self.personagem.y < 0:
            self.personagem.y = 0
        if self.personagem.y + self.personagem.altura > 180:
            self.personagem.y = 180 - self.personagem.altura

        # ------------------- Movimento do personagem -------------------#
        dx = 0
        dy = 0

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            dy -= 4
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            dy += 4
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            dx -= 4
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            dx += 4


        if dx != 0 or dy != 0:
            self.personagem.move(dx, dy)
        else:
            #-------------- Personagem parado -------------------#
            self.personagem.parada()
        #----------------- Personagem pulando -------------------#
        if pyxel.btnp(pyxel.KEY_SPACE) and self.personagem.no_chao:
            self.personagem.vy = -10
            self.personagem.no_chao = False
        self.personagem.atualizar_pulo()

    def draw_fase1(self):
        pyxel.cls(14)
        pyxel.mouse(False) # mouse desativado
        self.personagem.desenhapersonagem()

        pyxel.text(5, 5, "FASE 1", 0)
        pyxel.text(5+0.5, 5+0.5, "FASE 1", self.colortext)


#----------------- Personagem ---------------------------------------------------------------------------------------#
class Personagem:
    def __init__(self, x, y):
        self.vy = 0
        self.no_chao = True
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
    #----------------- Personagem pulando -------------------#
    def atualizar_pulo(self):

        gravidade = 1
        if not self.no_chao:
            self.vy += gravidade
            self.y += self.vy
            # Chegou no chão 
            if self.y >= 72:
                self.y = 72
                self.vy = 0
                self.no_chao = True



    #----------------- Personagem parado -------------------#
    def parada(self):

        self.x_mem = 0 
        self.y_mem = 0

    #----------------- colisão --------------------#
    def colisao(self):

        self.largura_parede = 250
        self.altura_parede = 180

        Esquerda_personagem = self.x
        Direita_personagem = self.x + self.largura_parede
        Cima_personagem = self.y
        Baixo_personagem = self.y + self.altura_parede

        if (self.x + self.largura > Esquerda_personagem and self.x < Direita_personagem and
            self.y + self.altura > Cima_personagem and self.y < Baixo_personagem):
            return True
        return False

    #----------------- Desenha o personagem -------------------#
    def desenhapersonagem(self):

        pyxel.blt(self.x, self.y, 1, self.x_mem, self.y_mem, self.largura, self.altura, 7)



#----------------- CandyMazeGame ---------------------------------------------------------------------------#
class CandyMazeGame:
    def __init__(self):
        pyxel.init(250, 180, title="CandyMaze", fps=30, quit_key=pyxel.KEY_Q )

        
        self.fase1 = Fase1()
        self.start = True
        self.start_screen = Start()
        self.personagem = Personagem(56, 72)
        self.colisao = False

        #-------- carrega as imagens --------#
        pyxel.images[0].load(0, 0, "background.png")
        pyxel.images[1].load(0, 0, "personagem.png")
        
        
        pyxel.run(self.update, self.draw)

        
    def update(self):
        if self.start:
            # Aguarda Enter ou Espaço para começar
            if not self.start_screen.update_conect():
                self.start = False
            return
        self.fase1.update_fase1()

        

        # -------- se clicar em ESC volta pra tela inicial -------------------#
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.start = True
            return

    def draw(self):
        if self.start:
            self.start_screen.desenhastart()
        else:
            self.fase1.draw_fase1()
            


CandyMazeGame()