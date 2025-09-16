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
        start_y = 130
        start_w = 110
        start_h = 10
        mouse_over_start = (
            start_x <= pyxel.mouse_x <= start_x + start_w and
            start_y <= pyxel.mouse_y <= start_y + start_h
        )

        mouse_over_quit = (130 <= pyxel.mouse_x <= 130 + 50 and
                           130 <= pyxel.mouse_y <= 130 + 10
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
        pyxel.cls(14)
        pyxel.blt(0, 0, 0, 0, 0, 250, 220)  
        pyxel.text(125, 130, "(Q)UIT", pyxel.frame_count % 4)
        pyxel.text(90, 130, "START |", pyxel.frame_count % 4)
        # Desenha cursor do mouse customizado
        pyxel.mouse(True)
        

#----------------- FASE 1 ----------------------------------------------------------------------------------------#

class Fase1:
    def __init__(self):
        self.colortext = 7
        self.pontos = 0
        altura_chao = 8
        altura_tela = 220
        altura_personagem = 18
        y_chao = altura_tela - altura_chao
        self.personagem = Personagem(2, y_chao - altura_personagem)
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
        if self.personagem.y + self.personagem.altura > 212:
            self.personagem.y = 212 - self.personagem.altura

        # ------------------- Movimento do personagem -------------------#
        dx = 0
        dy = 0

        #if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
         #   dy -= 4
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
        # --- Lógica de duplo pulo --- #
        if not hasattr(self.personagem, 'pulos_restantes'):
            self.personagem.pulos_restantes = 2
            self.personagem.ultimo_pulo_tick = 0
        if self.personagem.no_chao:
            self.personagem.pulos_restantes = 2
        if pyxel.btnp(pyxel.KEY_SPACE) and self.personagem.pulos_restantes > 0:
            agora = pyxel.frame_count
            if self.personagem.pulos_restantes == 1 and (agora - self.personagem.ultimo_pulo_tick) < 10:
                self.personagem.vy = -10  # 
            else:
                self.personagem.vy = -10
            self.personagem.no_chao = False
            self.personagem.pulos_restantes -= 1
            self.personagem.ultimo_pulo_tick = agora
        self.personagem.atualizar_pulo()

        if pyxel.btnp(pyxel.KEY_ESCAPE)*2:
            self.personagem.x = 2
            self.personagem.y = 194

    def paredes(self):
        
            self.parede1 = pyxel.rect(119, 172, 6, 40, pyxel.COLOR_BROWN)  # parede vertical
            self.parede2 = pyxel.rect(36, 164, 180, 8, pyxel.COLOR_BROWN)  # parede horizontal 1
            self.parede3 = pyxel.rect(0, 116, 100, 8, pyxel.COLOR_BROWN)  # parede horizontal 2
            self.parede4 = pyxel.rect(151, 116, 100, 8, pyxel.COLOR_BROWN)  # parede horizontal 3
            self.parede5 = pyxel.rect(40, 68, 210, 8, pyxel.COLOR_BROWN)   # parede horizontal 4
            

    def vidas(self):
        pass

    def draw_fase1(self):
        pyxel.cls(6)
        pyxel.blt(0, 0, 2, 0, 0, 250, 220)
        pyxel.mouse(False) # mouse desativado
        self.personagem.desenhapersonagem()

        pyxel.text(5, 5, "FASE 1", 0)
        pyxel.text(5+0.5, 5+0.5, "FASE 1", self.colortext)
        pyxel.rect(0, 212, 250, 8, 3) # chão
        self.porta_final = pyxel.rect(200, 37, 21, 31, pyxel.COLOR_BLACK) # porta final
        self.paredes()
        


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
        gravidade = 1.5
        altura_chao = 8
        y_chao = 220 - altura_chao
        if not self.no_chao:
            self.vy += gravidade
            self.y += self.vy
            # Chegou no chão
            if self.y + self.altura >= y_chao:
                self.y = y_chao - self.altura
                self.vy = 0
                self.no_chao = True



    #----------------- Personagem parado -------------------#
    def parada(self):

        self.x_mem = 0 
        self.y_mem = 0

    #----------------- colisão --------------------#
    def colisao(self):

        self.largura_parede = pyxel.width
        self.altura_parede = pyxel.height
         

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
        pyxel.init(250, 220, title="CandyMaze", fps=30, quit_key=pyxel.KEY_Q )

        
        self.fase1 = Fase1()
        self.start = True
        self.start_screen = Start()
        altura_chao = 8
        altura_tela = pyxel.height
        altura_personagem = 18
        y_chao = altura_tela - altura_chao
        self.personagem = Personagem(2, y_chao - altura_personagem)
        self.colisao = False

        #-------- carrega as imagens --------#
        pyxel.images[0].load(0, 0, "background.png")
        pyxel.images[1].load(0, 0, "personagem.png")
        pyxel.images[2].load(0, 0, "fundofase1.png")
        
        
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