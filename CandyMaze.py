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
        self.win = False
        self.win_counter = 0  # Contador de frames na porta final
        self.x_lago1 = 209
        self.y_lago1 = 212
        self.largura_lago1 = 20   #posicão inicial e tamanho do primeiro lago
        self.altura_lago1 = 8


    def update_fase1(self):
        # Se venceu, não atualiza mais nada
        if self.win:
            return
        


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


        # Porta final (posição e tamanho)
        porta_x, porta_y, porta_w, porta_h = 220, 37, 21, 31
        # Checa colisão do personagem com a porta final
        if (
            self.personagem.x < porta_x + porta_w and
            self.personagem.x + self.personagem.largura > porta_x and
            self.personagem.y < porta_y + porta_h and
            self.personagem.y + self.personagem.altura > porta_y
        ):
            self.win_counter += 1  # Incrementa contador se estiver na porta
            if self.win_counter > 30:  # Espera 30 frames (~1 segundo a 30fps)
                self.win = True
            else:
                self.win = False
        else:
            self.win_counter = 0  # Reseta contador se sair da porta
            self.win = False
    #-------------LAGO--------------
        self.x_lago1 += 0.5 #movimento do lago para a direita, e corte na largura de acordo com o movimento
        if self.largura_lago1 > 0 and self.x_lago1 < 250:
            self.largura_lago1 -= 0.5
        else:                #quando chega no limite imposto ele volta para a posicão inicial para reiniciar o movimento
            self.largura_lago1 = 20
            self.x_lago1 = 209

    def paredes(self):
        
            self.parede1 = pyxel.blt(122, 172, 1, 191, 0, 6, 40)  # parede vertical
            self.parede2 = pyxel.blt(35, 164, 1, 56, 40, 180, 8)  # parede horizontal 1
            self.parede3 = pyxel.blt(0, 116, 1, 0, 72, 100, 8)  # parede horizontal 2
            self.parede4 = pyxel.blt(150, 116, 1, 150, 72, 100, 8)  # parede horizontal 3
            self.parede5 = pyxel.blt(40, 68, 1, 0, 80, 210, 8)   # parede horizontal 4
            

    def vidas(self):
        pass

    def draw_fase1(self):
        pyxel.cls(6)
        pyxel.blt(0, 0, 2, 0, 0, 250, 220)
        pyxel.mouse(False) # mouse desativado
        self.porta_final = pyxel.blt(220, 37, 1, 149, 0, 21, 31) # porta final
        pyxel.blt(self.x_lago1, self.y_lago1, 1, 101, 0, self.largura_lago1, self.altura_lago1,7) #primeira imagem do looping do lago
        pyxel.blt(self.x_lago1 - 20, self.y_lago1, 1, 101, 0, 20, self.altura_lago1,7)  #segunda imagem do looping do lago
        pyxel.blt(self.x_lago1 - 40, self.y_lago1, 1, 101, 0, 20, self.altura_lago1,7)   #terceira imagem do looping do lago
        self.personagem.desenhapersonagem()
        pyxel.text(5+0.5, 5+0.5, "FASE 1", self.colortext)
        pyxel.text(5, 5, "FASE 1", 0)
        pyxel.blt(0, 212, 1, 0, 88, 250, 8,7) # chão
        self.paredes()
        if self.win:
            Win().desenhawin()
            return
        

#----------------- Win ---------------------------------------------------------------------------------------#
class Win:
    def __init__(self):
        self.colortext = 7
        self.x = 0
        self.y = 0
        self.width = 250
        self.height = 220


    def desenhawin(self):
        pyxel.cls(0)
        pyxel.text(120, 110, "YOU WIN!", pyxel.frame_count % 4)
        pyxel.mouse(True)



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
    def ha_parede_abaixo(self):
        # Lista das paredes horizontais (x, y, largura, altura)
        paredes_horizontais = [
            (35, 164, 180, 8),   # parede horizontal 1
            (0, 116, 100, 8),    # parede horizontal 2
            (150, 116, 100, 8),  # parede horizontal 3
            (40, 68, 210, 8),    # parede horizontal 4
            (0, 212, 250, 8)     # chão
        ]
        for rx, ry, rl, ra in paredes_horizontais:
            # Verifica se há parede logo abaixo do personagem
            if (
                self.y + self.altura == ry and
                self.x + self.largura > rx and
                self.x < rx + rl
            ):
                return True
        return False
    # Função utilitária para colisão de retângulos
    def colide_retangulo(self, px, py, pl, pa, rx, ry, rl, ra):
        return (
            px < rx + rl and
            px + pl > rx and
            py < ry + ra and
            py + pa > ry
        )

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

        # Lista de paredes verticais e horizontais (x, y, largura, altura)
        paredes = [
            (122, 172, 6, 40),   # parede vertical
            (35, 164, 180, 8),   # parede horizontal 1
            (0, 116, 100, 8),    # parede horizontal 2
            (150, 116, 100, 8),  # parede horizontal 3
            (40, 68, 210, 8),    # parede horizontal 4
            (0, 212, 250, 8)     # chão
        ]

        # --- Colisão lateral (X) ---
        novo_x = self.x + dx
        pode_mover_x = True
        for rx, ry, rl, ra in paredes:
            if self.colide_retangulo(novo_x, self.y, self.largura, self.altura, rx, ry, rl, ra):
                pode_mover_x = False
                break
        if pode_mover_x:
            self.x = novo_x

        # --- Colisão vertical (Y) ---
        novo_y = self.y + dy
        pode_mover_y = True
        for rx, ry, rl, ra in paredes:
            if self.colide_retangulo(self.x, novo_y, self.largura, self.altura, rx, ry, rl, ra):
                pode_mover_y = False
                break
        if pode_mover_y:
            self.y = novo_y

        # --- Após qualquer movimento, verifica se há parede embaixo ---
        if not self.ha_parede_abaixo():
            self.no_chao = False
    #----------------- Personagem pulando -------------------#
    def atualizar_pulo(self):
        gravidade = 1.5
        altura_chao = 8
        y_chao = 220 - altura_chao
        # Lista das paredes horizontais (x, y, largura, altura)
        paredes_horizontais = [
            (36, 164, 180, 8),   # parede horizontal 1
            (0, 116, 100, 8),    # parede horizontal 2
            (151, 116, 100, 8),  # parede horizontal 3
            (40, 68, 210, 8),    # parede horizontal 4
            (0, 212, 250, 8)     # chão
        ]
        if not self.no_chao:
            self.vy += gravidade  # Aplica gravidade
            novo_y = self.y + self.vy  # Calcula nova posição vertical
            colidiu = False  # Flag para saber se colidiu com alguma parede
            # Lista das paredes horizontais (x, y, largura, altura)
            paredes_horizontais = [
                (36, 164, 180, 8),   # parede horizontal 1
                (0, 116, 100, 8),    # parede horizontal 2
                (151, 116, 100, 8),  # parede horizontal 3
                (40, 68, 210, 8),    # parede horizontal 4
                (0, 212, 250, 8)     # chão
            ]
            for rx, ry, rl, ra in paredes_horizontais:
                # Colisão por cima (cair sobre a plataforma)
                if (
                    self.y + self.altura <= ry and  # Personagem acima da parede
                    novo_y + self.altura >= ry and  # Vai cruzar o topo da parede
                    self.x + self.largura > rx and  # Sobrepõe horizontalmente
                    self.x < rx + rl
                ):
                    self.y = ry - self.altura  # Encosta o personagem no topo da parede
                    self.vy = 0  # Para o movimento vertical
                    self.no_chao = True  # Marca que está no chão
                    colidiu = True
                    break
                # Colisão por baixo (bater a cabeça na plataforma)
                if (
                    self.y >= ry + ra and  # Personagem abaixo da parede
                    novo_y <= ry + ra and  # Vai cruzar a parte de baixo da parede
                    self.x + self.largura > rx and
                    self.x < rx + rl
                ):
                    self.y = ry + ra  # Encosta o personagem embaixo da parede
                    self.vy = 0  # Para o movimento vertical
                    colidiu = True
                    break
            if not colidiu:
                self.y = novo_y  # Se não colidiu, atualiza normalmente
                self.no_chao = False  # Não está no chão
            # Chegou no chão do cenário (garantia extra)
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
        pyxel.images[1].load(0, 0, "itens.png")
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
            # Exibe tela de vitória se win estiver True
            if self.fase1.win:
                Win().desenhawin()


CandyMazeGame()