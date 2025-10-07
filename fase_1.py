import pyxel
from jujuba import Personagem
from formiga import Formiga
from Tempo import Tempo
from Plataformas import Plataforma1, Plataforma2
from Pause import Pause
from instructions import InstructionsScreen
from Vidas import Vidas
from Balas import Balas





class Fase1:
    def __init__(self):
        self.porta_x, self.porta_y, self.porta_w, self.porta_h = 220, 37, 21, 31
        self.colortext = 7
        self.pontos = 0
        altura_chao = 8
        altura_tela = 220
        altura_personagem = 18
        y_chao = altura_tela - altura_chao
        self.chegou_aofim = False

        # Sistema de instruções
        self.showing_instructions = True
        self.first_time_playing = True
        self.color_timer = 0  # Timer para animação do gradiente
        self.instructions_screen = InstructionsScreen(self.color_timer)  # Nova classe de instruções
        #################################################################################################

        self.tempo = Tempo()
        self.formiga = Formiga()
        self.balas = Balas()

        self.personagem = Personagem(2, y_chao - altura_personagem)
        self.vidas = Vidas(self.personagem)
        self.x = 0
        self.y = 0

        self.colisao = False

        self.win = False
        self.win_counter = 0  # Contador de frames na porta final

        self.mx_lago1 = 204   #x inicial do ultimo bloco de lago(cada lago é formado por tres blocos)
        self.my_lago1 = 212
        self.mlargura_lago1 = 20   #posicão inicial e tamanho do primeiro lago
        self.maltura_lago1 = 8
        self.mx_inicial_lago1 = 184
        self.mlargura_total_lago1 = 35
        self.afogando = False
        self.lose = False
        self.afogar_timer = 0
        self.mx_lago2 = 137    #x inicial do ultimo bloco de lago(cada lago é formado por tres blocos)
        self.my_lago2 = 68
        self.mlargura_lago2 = 40   #posicão inicial e tamanho do segundo lago
        self.maltura_lago2 = 8
        self.mx_inicial_lago2 = 86
        self.mlargura_total_lago2 = 90 
        self.mx_lago3 = 509      #x inicial do ultimo bloco de lago(cada lago é formado por tres blocos)
        self.my_lago3 = 116
        self.mlargura_lago3 = 20   #posicão inicial e tamanho do terceiro lago
        self.maltura_lago3 = 8
        self.mx_inicial_lago3 = 30
        self.mlargura_total_lago3 = 35 

        self.plataforma1 = Plataforma1()
        self.plataforma2 = Plataforma2()
        
        # Cooldown para colisão com formiga
        self.formiga_collision_cooldown = 0
        
        # Sistema de invencibilidade visual
        self.invencibilidade_timer = 0

    # Motivo da derrota: 'formiga', 'tempo', 'afogado' ou None
        self.lose_reason = None
        



    def update_fase1(self):
        # Atualiza timer para animação do gradiente nas instruções
        self.color_timer += 1
        
        # Verifica se deve mostrar as instruções no início
        if self.showing_instructions and self.first_time_playing:
            # Aguarda o jogador pressionar ESPAÇO para sair das instruções
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.showing_instructions = False
                self.first_time_playing = False
            return  # Não executa o resto do update enquanto mostra instruções

        if not hasattr(self, 'pause_system'):
            self.pause_system = Pause() 

        # Sempre atualiza o sistema de pause (para detectar F)
        self.pause_system.update_pause()
        
        # Se está pausado, não executa o resto do gameplay
        if self.pause_system.pausado:
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

        if (dx != 0 or dy != 0) and not self.afogando: 
            self.personagem.move(dx, dy)
        else:
            if not self.chegou_aofim:   #se a personagem não estiver na porta final

            #-------------- Personagem parado -------------------#
                self.personagem.parada()


        #----------------- Personagem pulando -------------------#
        
        if not hasattr(self.personagem, 'pulos_restantes'):
            self.personagem.pulos_restantes = 2
            self.personagem.ultimo_pulo_tick = 0
        if self.personagem.no_chao:
            self.personagem.pulos_restantes = 2
        if pyxel.btnp(pyxel.KEY_SPACE) and self.personagem.pulos_restantes > 0:
            agora = pyxel.frame_count
            if self.personagem.pulos_restantes == 1 and (agora - self.personagem.ultimo_pulo_tick) < 10 and not self.afogando:
                self.personagem.vy = -10  # 
            else:
                if not self.afogando:
                    self.personagem.vy = -10
            self.personagem.no_chao = False
            self.personagem.pulos_restantes -= 1
            self.personagem.ultimo_pulo_tick = agora
            pyxel.play(2, 0)  # Som de pulo
        self.personagem.atualizar_pulo()

        if pyxel.btnp(pyxel.KEY_ESCAPE)*2:
            self.personagem.x = 2
            self.personagem.y = 194



        # Sistema de morte por tempo
        if self.tempo.update():
            pyxel.play(3, 2)
            self.lose = True
            self.lose_reason = 'tempo'
            return


        # Checa colisão do personagem com a porta final
        if (
            self.personagem.x < self.porta_x + self.porta_w and
            self.personagem.x + self.personagem.largura > self.porta_x and
            self.personagem.y < self.porta_y + self.porta_h and
            self.personagem.y + self.personagem.altura > self.porta_y
        ):
            self.win_counter += 1 
            self.personagem.x_mem = 0
            self.personagem.y_mem = 18
            if self.win_counter == 1:  
                self.chegou_aofim = True
            elif self.win_counter > 20: 
                if not self.win:  
                    pyxel.play(2, 3)  
                self.win = True
            else:
                self.win = False
        else:
            self.win_counter = 0  # Reseta contador se sair da porta
            self.win = False

        #----TESTA COLISAO COM BALA------
        self.balas.update(self.personagem.x,self.personagem.y)  


    #-------------LAGO 1--------------(lago do primeiro andar)

        self.mx_lago1 += 0.5 #movimento do lago para a direita, e corte na largura de acordo com o movimento
        if self.mlargura_lago1 > 0 and self.mx_lago1 < 224:
            self.mlargura_lago1 -= 0.5
        else:                #quando chega no limite imposto ele volta para a posicão inicial para reiniciar o movimento
            self.mlargura_lago1 = 20
            self.mx_lago1 = 204
    
    #----------LAGO2--------------(lago do ultimo andar)
        self.mx_lago2 += 0.5 #movimento do lago para a direita, e corte na largura de acordo com o movimento
        if self.mlargura_lago2 > 0 and self.mx_lago2 < 177:
            self.mlargura_lago2 -= 0.5
        else:                #quando chega no limite imposto ele volta para a posicão inicial para reiniciar o movimento
            self.mlargura_lago2 = 40
            self.mx_lago2 = 137

    #----------LAGO3--------------(lago do meio)
        self.mx_lago3 += 0.5 #movimento do lago para a direita, e corte na largura de acordo com o movimento
        if self.mlargura_lago3 > 0 and self.mx_lago3 < 70:
            self.mlargura_lago3 -= 0.5
        else:                #quando chega no limite imposto ele volta para a posicão inicial para reiniciar o movimento
            self.mlargura_lago3 = 20
            self.mx_lago3 = 50  

        # Função auxiliar para verificar colisão com retângulo (lago)
        def colide_com_lago(lago_x,lago_y,lago_w):
# ------------------- Detecta se personagem está sobre a água dos lagos (APÓS movimento) -------------------#
            px, py, pl, pa = self.personagem.x, self.personagem.y, self.personagem.largura, self.personagem.altura
            self.pdir = px + pl - 7  # lado direito do personagem
            self.pesq = px + 7   # lado esquerdo do personagem
            self.ptop = py      # topo do personagem
            self.pbottom = py + pa  # base do personagem

            lago_esq = lago_x           # Limites do lago
            lago_dir = lago_x + lago_w
            lago_top = lago_y 
            lago_dow = lago_y + 7

            if (self.pdir >= lago_esq and 
                self.pesq <= lago_dir and
                self.ptop <= lago_dow and
                self.pbottom >= lago_top):  
                return True

            return False

        # Verifica colisão com qualquer lago
        if colide_com_lago(self.mx_inicial_lago1,self.my_lago1,self.mlargura_total_lago1): 
            if not self.afogando:
                self.afogando = True
                self.afogar_timer = 0
                self.personagem.y += 6
                self.personagem.altura -= 6
                if self.personagem.x < 192:
                    self.personagem.x += 7
                if self.personagem.x > 208:
                    self.personagem.x -= 7 
                pyxel.play(3, 7)  # Som suave de toque na água

        elif colide_com_lago(self.mx_inicial_lago3,self.my_lago3,self.mlargura_total_lago3):
            if not self.afogando:
                self.afogando = True
                self.afogar_timer = 0
                self.personagem.y += 6
                self.personagem.altura -= 6
                if self.personagem.x < 38:
                    self.personagem.x += 7
                if self.personagem.x > 55:
                    self.personagem.x -= 7 
                pyxel.play(3, 7)  

        elif colide_com_lago(self.mx_inicial_lago2,self.my_lago2,self.mlargura_total_lago2):
            if not self.afogando:
                
                self.afogando = True
                self.afogar_timer = 0
                self.personagem.y += 6
                self.personagem.altura -= 6
                if self.personagem.x < 96:
                    self.personagem.x += 7
                if self.personagem.x > 165 :
                    self.personagem.x -= 7 
                pyxel.play(3, 7)  

        # Sistema de morte lenta e inevitável 
        if self.afogando:
            self.afogar_timer += 1
            tempo_restante = (40 - self.afogar_timer) / 20  # Converte frames para segundos (fps=20)
            self.personagem.x_mem = 56   #muda a animacão
            self.personagem.y_mem = 48
            
            # Após 2 segundos (40 frames com fps=20), morte definitiva
            if self.afogar_timer >= 40:
                pyxel.play(3, 2)  # Som de morte/afogamento
                self.lose = True
                self.lose_reason = 'afogado'





        # ---------- plataforma movimento ---------------------------------
        self.plataforma1.update() 
    
        # Colisão com TOPO da plataforma 1 (personagem em cima)
        if self.plataforma1.x < self.personagem.x + self.personagem.largura/2 and self.plataforma1.x + 24 > self.personagem.x:
            if self.personagem.y + self.personagem.altura <= 50 and self.personagem.y + self.personagem.altura >= 42:
                self.personagem.y = 42 - self.personagem.altura
                self.personagem.no_chao = True
                self.personagem.vy = 0
                # Move o personagem junto com a plataforma na direção correta
                if self.plataforma1.direita:
                    self.personagem.x += 2  # Move para a direita
                else:
                    self.personagem.x -= 2  # Move para a esquerda

        # COLISÃO COM PARTE DE BAIXO da plataforma 1 (bater a cabeça)
        if (self.plataforma1.x < self.personagem.x + self.personagem.largura and 
            self.plataforma1.x + 24 > self.personagem.x):
            # Verifica se o personagem está subindo (vy negativo) e vai bater a cabeça
            if (self.personagem.y >= self.plataforma1.y + 8 and  # Personagem abaixo da plataforma
                self.personagem.y <= self.plataforma1.y + 8 + 5 and  # Margem de 5px para detecção
                self.personagem.vy < 0):  # Personagem subindo
                # Bate a cabeça na parte de baixo da plataforma
                self.personagem.y = self.plataforma1.y + 8  # Posiciona logo abaixo da plataforma
                self.personagem.vy = 2  # Força para baixo (efeito de "rebote")
                self.personagem.no_chao = False
                # Som de batida na cabeça (opcional)
                pyxel.play(2, 1)  # Usa o som de dano
                

        self.plataforma2.update()
        
        # Colisão com TOPO da plataforma 2 (personagem em cima)
        if self.plataforma2.x < self.personagem.x + self.personagem.largura/2 and self.plataforma2.x + 50 > self.personagem.x:
            if self.personagem.y + self.personagem.altura <= 124 and self.personagem.y + self.personagem.altura >= 116:
                self.personagem.y = 116 - self.personagem.altura
                
                # Verifica se está na posição específica para parar de mover junto
                if self.personagem.y == 98 and self.personagem.x >= 152:  # y = 116 - 18 (altura do personagem) = 98
                    # Personagem para de se mover junto com a plataforma
                    self.personagem.no_chao = True
                    self.personagem.vy = 0
                    # NÃO move o personagem junto com a plataforma
                else:
                    # Comportamento normal - move junto com a plataforma
                    if self.personagem.x >= 152 and self.personagem.x <= 90: 
                        self.personagem.no_chao = False
                    else:
                        self.personagem.no_chao = True
                    self.personagem.vy = 0
                    # Move o personagem junto com a plataforma na direção correta
                    if self.plataforma2.direita:
                        self.personagem.x += 2  # Move para a direita
                    else:
                        self.personagem.x -= 2  # Move para a esquerda
        

        # COLISÃO COM PARTE DE BAIXO da plataforma 2
        if (self.plataforma2.x < self.personagem.x + self.personagem.largura and 
            self.plataforma2.x + 50 > self.personagem.x):  
            
            if (self.personagem.y >= self.plataforma2.y + 8 and  
                self.personagem.y <= self.plataforma2.y + 8 + 5 and  
                self.personagem.vy < 0):  
                
                self.personagem.y = self.plataforma2.y + 8  
                self.personagem.vy = 2  
                self.personagem.no_chao = False

            elif (self.personagem.y > self.plataforma2.y + 8 and  
                  self.personagem.y < self.plataforma2.y + 8 + 15 and  
                  self.personagem.vy <= 0):  
                
                self.personagem.y = self.plataforma2.y + 8 + 2  
                if self.personagem.vy < 0:
                    self.personagem.vy = 1  
                self.personagem.no_chao = False
        
        # ---------- Colisão formiga - Sistema de perda de vida ---------------------------------
        
        self.formiga.update() 

        # Verificar se o personagem encostar em qualquer lado da formiga
        formiga_esquerda = self.formiga.x
        formiga_direita = self.formiga.x + self.formiga.largura
        formiga_topo = self.formiga.y
        formiga_base = self.formiga.y + self.formiga.altura
        
        personagem_esquerda = self.personagem.x
        personagem_direita = self.personagem.x + self.personagem.largura
        personagem_topo = self.personagem.y
        personagem_base = self.personagem.y + self.personagem.altura
        
        # Verificar colisão geral
        colisao_formiga = (
            personagem_direita > formiga_esquerda and
            personagem_esquerda < formiga_direita and
            personagem_base > formiga_topo and
            personagem_topo < formiga_base
        )
        
        # Se houver colisão e o cooldown permitir, aplicar perda de vida
        if colisao_formiga and self.formiga_collision_cooldown <= 0:
            # Verificar qual lado do personagem tocou na formiga
            lado_tocado = ""
            
            # Lado esquerdo do personagem toca no lado direito da formiga
            if personagem_esquerda <= formiga_direita and personagem_direita > formiga_direita:
                lado_tocado = "esquerda do personagem"
                
            # Lado direito do personagem toca no lado esquerdo da formiga  
            elif personagem_direita >= formiga_esquerda and personagem_esquerda < formiga_esquerda:
                lado_tocado = "direita do personagem"
                
            # Topo do personagem toca na base da formiga
            elif personagem_topo <= formiga_base and personagem_base > formiga_base:
                lado_tocado = "topo do personagem"
                
            # Base do personagem toca no topo da formiga
            elif personagem_base >= formiga_topo and personagem_topo < formiga_topo:
                lado_tocado = "base do personagem"
            
            if lado_tocado:
                self.personagem.vidas -= 1
                self.balas.score -= 100          #diminui o score
                self.formiga_collision_cooldown = 30  
                self.invencibilidade_timer = 30 
                
                pyxel.play(2, 1)  # Som de dano/colisão com formiga
                
                # Empurrar o personagem para trás
                knockback_distance = 20  # Distância maior de empurrão
                
                if lado_tocado == "esquerda do personagem":
                    # Empurra para a esquerda (para trás)
                    self.personagem.x -= knockback_distance
                elif lado_tocado == "direita do personagem":
                    # Empurra para a direita (para trás)
                    self.personagem.x += knockback_distance
                elif lado_tocado == "topo do personagem":
                    # Empurra para cima (para trás)
                    self.personagem.y -= knockback_distance
                elif lado_tocado == "base do personagem":
                    # Empurra para baixo (para trás)
                    self.personagem.y += knockback_distance
                
                # Adicionar efeito de knockback na velocidade vertical se estiver no ar
                if not self.personagem.no_chao:
                    if lado_tocado in ["esquerda do personagem", "direita do personagem"]:
                        # Se colidiu lateralmente, empurra também verticalmente
                        self.personagem.vy = -5  # Pequeno impulso para cima
                    elif lado_tocado == "topo do personagem":
                        # Se bateu por cima, empurra para baixo
                        self.personagem.vy = 8
                    elif lado_tocado == "base do personagem":
                        # Se colidiu por baixo, empurra mais para cima
                        self.personagem.vy = -8
                
                # Garantir que o personagem não saia dos limites da tela
                if self.personagem.x < 0:
                    self.personagem.x = 0
                if self.personagem.x + self.personagem.largura > 250:
                    self.personagem.x = 250 - self.personagem.largura
                if self.personagem.y < 0:
                    self.personagem.y = 0
                if self.personagem.y + self.personagem.altura > 212:
                    self.personagem.y = 212 - self.personagem.altura
                
                # Verificar se perdeu todas as vidas
                if self.personagem.vidas <= 0:
                    pyxel.play(3, 2)  # Som de morte
                    self.lose = True
                    # normalmente perda de vidas vem da formiga (colisão)
                    self.lose_reason = 'formiga'
        
        # Decrementar cooldowns
        if self.formiga_collision_cooldown > 0:
            self.formiga_collision_cooldown -= 1
        if self.invencibilidade_timer > 0:
            self.invencibilidade_timer -= 1


        if self.win or self.lose:
            return

    def paredes(self):
        self.parede1 = pyxel.blt(122, 172, 1, 191, 0, 6, 40)  # parede vertical
        self.parede2 = pyxel.blt(35, 164, 1, 56, 40, 180, 8)  # parede horizontal 1
        self.parede3 = pyxel.blt(0, 116, 1, 0, 72, 100, 8,7)  # parede horizontal 2
        self.parede4 = pyxel.blt(150, 116, 1, 150, 72, 100, 8)  # parede horizontal 3
        self.parede5 = pyxel.blt(40, 68, 1, 0, 80, 210, 8,7)   # parede horizontal 4

    def draw_gradient_text(self, text, x, y):
        """Desenha texto com gradiente de cores que se move (igual ao menu)"""
        colors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Gradiente completo
        for i, char in enumerate(text):
            color_index = (i + self.color_timer // 8) % len(colors)
            color = colors[color_index]
            pyxel.text(x + i * 4, y, char, color)

    def draw_fase1(self):
        pyxel.cls(6)
        pyxel.blt(0, 0, 2, 0, 0, 250, 220)
        pyxel.mouse(False) # mouse desativado

        

        # Verifica se perdeu todas as vidas
        if self.vidas.sistema_vidas():
            self.lose = True
            # se as vidas acabaram, normalmente foi por ataques (formiga)
            if not self.lose_reason:
                self.lose_reason = 'formiga'
        self.tempo.draw()
        # Checa colisão do personagem com a porta final
        if (
            self.personagem.x < self.porta_x + self.porta_w and
            self.personagem.x + self.personagem.largura > self.porta_x and
            self.personagem.y < self.porta_y + self.porta_h and
            self.personagem.y + self.personagem.altura > self.porta_y
        ):
            self.porta_final = pyxel.blt(220, 37, 1, 170, 0, 21, 31)  # Porta final
        else:
            self.porta_final = pyxel.blt(220, 37, 1, 149, 0, 21, 31) # porta final

        # Desenha o personagem ANTES do lago (com efeito de piscar se invencível)
        if self.invencibilidade_timer > 0 and self.invencibilidade_timer % 4 < 2:
            # Personagem piscando (desenha só metade do tempo)
            pass  # Não desenha o personagem neste frame
        else:
            self.personagem.desenhapersonagem()

        #----LAGO1-------(lago do primeiro andar)
        pyxel.blt(self.mx_lago1, self.my_lago1, 1, 101, 0, self.mlargura_lago1, self.maltura_lago1,7) #primeira imagem do looping do lago
        pyxel.blt(self.mx_lago1 - 20, self.my_lago1, 1, 101, 0, 20, self.maltura_lago1,7)  #segunda imagem do looping do lago
        pyxel.blt(self.mx_lago1 - 40, self.my_lago1, 1, 101, 0, 20, self.maltura_lago1,7)   #terceira imagem do looping do lago
       #-----LAGO2--------(lago do ultimo andar)
        pyxel.blt(self.mx_lago2, self.my_lago2, 1, 56, 16, self.mlargura_lago2, self.maltura_lago2,7) 
        pyxel.blt(self.mx_lago2 - 40, self.my_lago2, 1, 56, 16, 40, self.maltura_lago2,7) 
        pyxel.blt(self.mx_lago2 - 80, self.my_lago2, 1, 56, 16, 40, self.maltura_lago2,7) 
        pyxel.blt(self.mx_lago2 - 95, self.my_lago2, 1, 56, 16, 15, self.maltura_lago2,7)   
        #-----LAGO3--------(lago do meio)
        pyxel.blt(self.mx_lago3, self.my_lago3, 1, 56, 24, self.mlargura_lago3, self.maltura_lago3,7) 
        pyxel.blt(self.mx_lago3 - 20, self.my_lago3, 1, 56, 24, 20, self.maltura_lago3,7)  
        pyxel.blt(self.mx_lago3 - 40, self.my_lago3, 1, 56, 24, 20, self.maltura_lago3,7) 
        
        self.formiga.draw()
        self.balas.draw() 
        
        pyxel.text(5+0.5, 5+0.5, "FASE 1", self.colortext)
        pyxel.text(5, 5, "FASE 1", 0)
        pyxel.blt(0, 212, 1, 0, 88, 250, 8,7) # chão
        pyxel.blt(self.plataforma1.x,42,1,56,32,24,8,7) #plataforma móvel
        pyxel.blt(self.plataforma2.x,116,1, 56, 8, 50, 8, 7) #plataforma móvel
        
        self.paredes()

        # Desenha as instruções no início da fase
        if self.showing_instructions and self.first_time_playing:
            self.instructions_screen.update(self.color_timer)
            self.instructions_screen.draw()

        if hasattr(self, 'pause_system'):
            self.pause_system.draw_pause_overlay()