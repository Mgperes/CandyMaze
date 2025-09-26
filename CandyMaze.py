import pyxel
import math

    # --------------------- Classe para logs coloridos e aparentes no terminal --------------------------#
class GameLogger:
    
    # Códigos para cores
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Cores de texto
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Cores de fundo
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    @staticmethod
    def death_log(message):
        #Log de morte super aparente
        border = "=" * 50
        print(f"\n{GameLogger.BG_RED}{GameLogger.WHITE}{GameLogger.BOLD}")
        print(border)
        print(f"💀 MORTE: {message} 💀")
        print(border)
        print(f"{GameLogger.RESET}\n")
    
    @staticmethod
    def warning_log(message):
        #Log de aviso em amarelo
        print(f"{GameLogger.BG_YELLOW}{GameLogger.RED}{GameLogger.BOLD}⚠️  {message} ⚠️{GameLogger.RESET}")
    
    @staticmethod
    def danger_log(message):
        #Log de perigo em vermelho piscante
        print(f"{GameLogger.RED}{GameLogger.BOLD}🚨 {message} 🚨{GameLogger.RESET}")
    
    @staticmethod
    def info_log(message):
        #Log de informação em azul
        print(f"{GameLogger.CYAN}ℹ️  {message}{GameLogger.RESET}")
    
    @staticmethod
    def success_log(message):
        #Log de sucesso em verde
        print(f"\n{GameLogger.GREEN}{GameLogger.BOLD}✅ {message}{GameLogger.RESET}")
    
    @staticmethod
    def debug_log(message):
        #Log de debug em magenta
        print(f"{GameLogger.MAGENTA}🔧 DEBUG: {message}{GameLogger.RESET}")
    
    @staticmethod
    def game_start_log():
        #Log especial para início do jogo
        border = "🎮" * 20
        print(f"\n{GameLogger.BG_BLUE}{GameLogger.WHITE}{GameLogger.BOLD}")
        print(f"    {border}")
        print(f"    🕹️  CANDY MAZE INICIADO! 🕹️")
        print(f"    {border}")
        print(f"{GameLogger.RESET}")
        print(f"\n{GameLogger.CYAN}📋 OBJETIVO: Chegue na porta final sem se afogar!{GameLogger.RESET}")
        print(f"{GameLogger.YELLOW}⚠️  CUIDADO: Evite ficar muito tempo na água dos lagos!{GameLogger.RESET}\n")

class Start:
    def __init__(self):
        self.colortext = 7
        self.hover_timer = 0
        self.x = 0
        self.y = 0
        self.width = 250
        self.height = 180
        # Variáveis para efeitos de cor
        self.color_timer = 0
        self.rainbow_offset = 0


    def update_conect(self):
        # Atualiza timer para efeitos de cor
        self.color_timer += 1
        self.rainbow_offset += 0.1

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

    
    def draw_gradient_text(self, text, x, y):
        # Desenha texto com gradiente de cores que se move
        colors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Gradiente completo
        for i, char in enumerate(text):
            color_index = (i + self.color_timer // 8) % len(colors)
            color = colors[color_index]
            pyxel.text(x + i * 4, y, char, color)
    

    def desenhastart(self):
        pyxel.cls(14)
        pyxel.blt(0, 0, 0, 0, 0, 250, 220)  
        self.draw_gradient_text("START |", 90, 130)
        self.draw_gradient_text(" (Q)UIT", 118, 130)
        pyxel.mouse(True)


class Plataforma:
    def __init__(self):
        self.x = 87
        self.direita = True
    def update(self):
        if self.x == 87:
            self.direita = True  #quando x for 87 (o inicial) ela se moverá para a direita
        if self.x == 153:
            self.direita = False  #quando x chegar a 153 o movimento inverte para a esquerda
        if self.direita == True:
            self.x += 0.5
            self.direita = True
        if self.direita == False:
            self.x -= 0.5
            self.direita = False
    def draw(self):
        pyxel.blt(self.x, 42, 1, 56, 32, 24, 8,7)

class formiga:
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
            self.direita = True  #quando x for 87 (o inicial) ela se moverá para a direita
        if self.x == 197:
            self.direita = False  #quando x chegar a 153 o movimento inverte para a esquerda
        if self.direita == True:
            self.v = 0.5
            self.x += self.v
            self.direita = True
            self.y_mem = 11
        if self.direita == False:
            self.v = -(0.5)
            self.x += self.v
            self.direita = False
            self.y_mem = 0
        #desenho do movimento
        if self.v == 0.5 and self.i == 1:
            self.x_mem = 197
            self.i = 2
        else: 
            if self.v == 0.5:
                self.x_mem = 215
                self.i = 1
        if self.v == -(0.5) and self.i == 1:
            self.x_mem = 197
            self.i = 2
        else: 
            if self.v == -(0.5):
                self.x_mem = 215
                self.i = 1
        
    def draw(self):
        pyxel.blt(self.x, self.y, 1, self.x_mem, self.y_mem, 18, 11,7)


#----------------- FASE 1 ----------------------------------------------------------------------------------------#

class Fase1:
    def __init__(self):
        self.porta_x, self.porta_y, self.porta_w, self.porta_h = 220, 37, 21, 31
        self.colortext = 7
        self.pontos = 0
        altura_chao = 8
        altura_tela = 220
        altura_personagem = 18
        y_chao = altura_tela - altura_chao



        self.formiga = formiga()

        self.personagem = Personagem(2, y_chao - altura_personagem)
        self.vidas = Vidas(self.personagem)
        self.x = 0
        self.y = 0

        self.colisao = False

        self.win = False
        self.win_counter = 0  # Contador de frames na porta final

        self.mx_lago1 = 204
        self.my_lago1 = 212
        self.mlargura_lago1 = 20   #posicão inicial e tamanho do primeiro lago
        self.maltura_lago1 = 8
        self.afogando = False
        self.lose = False
        self.afogar_timer = 0
        self.mx_lago2 = 137
        self.my_lago2 = 68
        self.mlargura_lago2 = 40   #posicão inicial e tamanho do segundo lago
        self.maltura_lago2 = 8
        self.mx_lago3 = 50
        self.my_lago3 = 116
        self.mlargura_lago3 = 20   #posicão inicial e tamanho do terceiro lago
        self.maltura_lago3 = 8

        self.plataforma = Plataforma()
        
        # Cooldown para colisão com formiga
        self.formiga_collision_cooldown = 0
        
        # Sistema de invencibilidade visual
        self.invencibilidade_timer = 0
        
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


        # Checa colisão do personagem com a porta final
        if (
            self.personagem.x < self.porta_x + self.porta_w and
            self.personagem.x + self.personagem.largura > self.porta_x and
            self.personagem.y < self.porta_y + self.porta_h and
            self.personagem.y + self.personagem.altura > self.porta_y
        ):
            self.win_counter += 1  # Incrementa contador se estiver na porta
            if self.win_counter == 1:  # Primeira vez na porta
                GameLogger.info_log("Personagem chegou na porta final!")
            elif self.win_counter == 10:  # Meio caminho
                GameLogger.warning_log("Aguardando confirmação de vitória...")
            elif self.win_counter > 20:  # Espera 20 frames (~1 segundo a 30fps)
                if not self.win:  # Só mostra uma vez
                    GameLogger.success_log("🎉 PARABÉNS! VOCÊ VENCEU O CANDY MAZE! 🎉")
                self.win = True
            else:
                self.win = False
        else:
            if self.win_counter > 0:  # Saiu da porta antes de ganhar
                GameLogger.warning_log("Saiu da porta! Volte para vencer essa fase!")
            self.win_counter = 0  # Reseta contador se sair da porta
            self.win = False






    #-------------LAGO 1--------------

        self.mx_lago1 += 0.5 #movimento do lago para a direita, e corte na largura de acordo com o movimento
        if self.mlargura_lago1 > 0 and self.mx_lago1 < 224:
            self.mlargura_lago1 -= 0.5
        else:                #quando chega no limite imposto ele volta para a posicão inicial para reiniciar o movimento
            self.mlargura_lago1 = 20
            self.mx_lago1 = 204
    
    #----------LAGO2--------------
        self.mx_lago2 += 0.5 #movimento do lago para a direita, e corte na largura de acordo com o movimento
        if self.mlargura_lago2 > 0 and self.mx_lago2 < 177:
            self.mlargura_lago2 -= 0.5
        else:                #quando chega no limite imposto ele volta para a posicão inicial para reiniciar o movimento
            self.mlargura_lago2 = 40
            self.mx_lago2 = 137

    #----------LAGO3--------------
        self.mx_lago3 += 0.5 #movimento do lago para a direita, e corte na largura de acordo com o movimento
        if self.mlargura_lago3 > 0 and self.mx_lago3 < 70:
            self.mlargura_lago3 -= 0.5
        else:                #quando chega no limite imposto ele volta para a posicão inicial para reiniciar o movimento
            self.mlargura_lago3 = 20
            self.mx_lago3 = 50



        # ------------------- Detecta se personagem está sobre a água dos lagos (APÓS movimento) -------------------#
        px, py, pl, pa = self.personagem.x, self.personagem.y, self.personagem.largura, self.personagem.altura
        self.pdir = px + pl  # lado direito do personagem
        self.pesq = px       # lado esquerdo do personagem
        self.ptop = py       # topo do personagem
        self.pbottom = py + pa  # base do personagem

        print(f"Personagem: x={self.personagem.x}, y={self.personagem.y}, direita={self.pdir}, base={self.pbottom}")
        print(f"Lago1: x={self.mx_lago1}-{self.mx_lago1+self.mlargura_lago1}, y={self.my_lago1}-{self.my_lago1+self.maltura_lago1}")
        print(f"Lago2: x={self.mx_lago2}-{self.mx_lago2+self.mlargura_lago2}, y={self.my_lago2}-{self.my_lago2+self.maltura_lago2}")
        print(f"Lago3: x={self.mx_lago3}-{self.mx_lago3+self.mlargura_lago3}, y={self.my_lago3}-{self.my_lago3+self.maltura_lago3}")
        
        

        # Função auxiliar para verificar colisão com retângulo (lago)
        def colide_com_lago(lago_x, lago_y, lago_w, lago_h):
            return (
                self.pdir > lago_x and self.pesq < lago_x + lago_w and  # colisão horizontal
                self.pbottom > lago_y and self.ptop < lago_y + lago_h   # colisão vertical
            )

        # Verifica colisão com qualquer lago
        if colide_com_lago(self.mx_lago1, self.my_lago1, self.mlargura_lago1, self.maltura_lago1):
            if not self.afogando:
                # Primeira vez tocando na água - MORTE INEVITÁVEL iniciada
                self.afogando = True
                self.afogar_timer = 0
                GameLogger.death_log("💀 TOCOU NA ÁGUA! O personagem está se afogando... 💀")
                print("COLISÃO DETECTADA COM LAGO 1!")
        elif colide_com_lago(self.mx_lago2, self.my_lago2, self.mlargura_lago2, self.maltura_lago2):
            if not self.afogando:
                # Primeira vez tocando na água - MORTE INEVITÁVEL iniciada
                self.afogando = True
                self.afogar_timer = 0
                GameLogger.death_log("💀 TOCOU NA ÁGUA! O personagem está se afogando... 💀")
                print("COLISÃO DETECTADA COM LAGO 2!")
        elif colide_com_lago(self.mx_lago3, self.my_lago3, self.mlargura_lago3, self.maltura_lago3):
            if not self.afogando:
                # Primeira vez tocando na água - MORTE INEVITÁVEL iniciada
                self.afogando = True
                self.afogar_timer = 0
                GameLogger.death_log("💀 TOCOU NA ÁGUA! O personagem está se afogando... 💀")
                print("COLISÃO DETECTADA COM LAGO 3!")

        # Sistema de morte lenta e inevitável (2 segundos)
        if self.afogando:
            self.afogar_timer += 1
            tempo_restante = (40 - self.afogar_timer) / 20  # Converte frames para segundos (fps=20)
            
            # Avisos progressivos durante o afogamento
            if self.afogar_timer == 10:  # 0.5 segundos
                GameLogger.danger_log("🌊 AFOGANDO... Não há como escapar! 🌊")
            elif self.afogar_timer == 20:  # 1 segundo
                GameLogger.danger_log("💀 MEIO AFOGADO... Prepare-se para morrer! 💀")
            elif self.afogar_timer == 30:  # 1.5 segundos
                GameLogger.danger_log("☠️  QUASE MORTO... Últimos momentos! ☠️")
            
            # Após 2 segundos (40 frames com fps=20), morte definitiva
            if self.afogar_timer >= 40:
                GameLogger.death_log("💀💀💀 O PERSONAGEM SE AFOGOU COMPLETAMENTE! 💀💀💀")
                self.lose = True





        # ---------- plataforma movimento ---------------------------------
        self.plataforma.update() 
        if self.plataforma.x < self.personagem.x + self.personagem.largura and self.plataforma.x + 24 > self.personagem.x:
            if self.personagem.y + self.personagem.altura <= 50 and self.personagem.y + self.personagem.altura >= 42:
                self.personagem.y = 42 - self.personagem.altura
                self.personagem.no_chao = True
                self.personagem.vy = 0
                # Move o personagem junto com a plataforma na direção correta
                if self.plataforma.direita:
                    self.personagem.x += 0.5  # Move para a direita
                else:
                    self.personagem.x -= 0.5  # Move para a esquerda
            else:
                pass  # Não faz nada se o personagem não estiver em cima da plataforma
        else:
            pass  # Não faz nada se não houver colisão

        self.formiga.update() 

        # ---------- Colisão formiga - Sistema de perda de vida ---------------------------------
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
                self.formiga_collision_cooldown = 30  # 1.5 segundos de cooldown (30 frames a 20fps)
                self.invencibilidade_timer = 30  # Efeito visual de invencibilidade
                
                GameLogger.danger_log(f"🐜 FORMIGA ATACOU! {lado_tocado} encostou na formiga! Vidas restantes: {self.personagem.vidas}")
                
                # Empurrar o personagem para trás com mais força (knockback)
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
                    GameLogger.death_log("💀 GAME OVER! Todas as vidas foram perdidas! 💀")
                    self.lose = True
        
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
        



    def draw_fase1(self):
        pyxel.cls(6)
        pyxel.blt(0, 0, 2, 0, 0, 250, 220)
        pyxel.mouse(False) # mouse desativado

        # Verifica se perdeu todas as vidas
        if self.vidas.sistema_vidas():
            self.lose = True

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

        #----LAGO1-------
        pyxel.blt(self.mx_lago1, self.my_lago1, 1, 101, 0, self.mlargura_lago1, self.maltura_lago1,7) #primeira imagem do looping do lago
        pyxel.blt(self.mx_lago1 - 20, self.my_lago1, 1, 101, 0, 20, self.maltura_lago1,7)  #segunda imagem do looping do lago
        pyxel.blt(self.mx_lago1 - 40, self.my_lago1, 1, 101, 0, 20, self.maltura_lago1,7)   #terceira imagem do looping do lago
       #-----LAGO2--------
        pyxel.blt(self.mx_lago2, self.my_lago2, 1, 56, 16, self.mlargura_lago2, self.maltura_lago2,7) 
        pyxel.blt(self.mx_lago2 - 40, self.my_lago2, 1, 56, 16, 40, self.maltura_lago2,7) 
        pyxel.blt(self.mx_lago2 - 80, self.my_lago2, 1, 56, 16, 40, self.maltura_lago2,7) 
        pyxel.blt(self.mx_lago2 - 95, self.my_lago2, 1, 56, 16, 15, self.maltura_lago2,7)   
        #-----LAGO3--------
        pyxel.blt(self.mx_lago3, self.my_lago3, 1, 56, 24, self.mlargura_lago3, self.maltura_lago3,7) 
        pyxel.blt(self.mx_lago3 - 20, self.my_lago3, 1, 56, 24, 20, self.maltura_lago3,7)  
        pyxel.blt(self.mx_lago3 - 40, self.my_lago3, 1, 56, 24, 20, self.maltura_lago3,7) 

        self.formiga.draw()

        pyxel.text(5+0.5, 5+0.5, "FASE 1", self.colortext)
        pyxel.text(5, 5, "FASE 1", 0)
        pyxel.blt(0, 212, 1, 0, 88, 250, 8,7) # chão
        pyxel.blt(self.plataforma.x,42,1,56,32,24,8) #plataforma móvel
        self.paredes()

        pyxel.blt(145, 199, 1, 121, 0, 7, 7,7)
        
#----------------- Vidas ---------------------------------------------------------------------------------------#
class Vidas:
    def __init__(self, personagem):
        self.personagem = personagem
        self.lose = False

    def sistema_vidas(self):
        if self.personagem.vidas >= 3:
            pyxel.blt(40, 5, 1, 139, 9, 10, 7, 7)  # coração
            pyxel.blt(52, 5, 1, 139, 9, 10, 7, 7)  # coração
            pyxel.blt(64, 5, 1, 139, 9, 10, 7, 7)  # coração
        elif self.personagem.vidas == 2:
            pyxel.blt(40, 5, 1, 139, 9, 10, 7, 7)  # coração
            pyxel.blt(52, 5, 1, 139, 9, 10, 7, 7)  # coração
        elif self.personagem.vidas == 1:
            pyxel.blt(40, 5, 1, 139, 9, 10, 7, 7)  # coração
        elif self.personagem.vidas <= 0:
            self.lose = True
            return True  # Retorna True quando perde todas as vidas
        return False


#----------------- VictoryScreen ---------------------------------------------------------------------------------------#
class VictoryScreen:
    def __init__(self):
        self.colortext = 7
        self.width = 250
        self.height = 220

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            return True
        return False

    def draw(self):
        pyxel.cls(11)
        pyxel.text(100, 90, "YOU WIN!", pyxel.frame_count % 16)
        pyxel.text(70, 120, "Press ENTER/SPACE to play again", 7)
        pyxel.mouse(False)

#----------------- LoseScreen ---------------------------------------------------------------------------------------#
class LoseScreen:
    def __init__(self):
        self.colortext = 8
        self.width = 250
        self.height = 220

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            return True
        return False

    def draw(self):
        pyxel.cls(8)
        pyxel.text(100, 90, "YOU LOSE!", pyxel.frame_count % 16)
        pyxel.text(70, 120, "Press ENTER/SPACE to try again", 7)
        pyxel.mouse(False)
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
        self.vidas = 3  # Número inicial de vidas
        
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
        pyxel.init(250, 220, title="CandyMaze", fps=20, quit_key=pyxel.KEY_Q )

        self.state = "start"  # start, game, victory
        self.start_screen = Start()
        self.fase1 = Fase1()
        self.victory_screen = VictoryScreen()
        self.lose_screen = LoseScreen()

        #-------- carrega as imagens --------#
        pyxel.images[0].load(0, 0, "background.png")
        pyxel.images[1].load(0, 0, "itens.png")
        pyxel.images[2].load(0, 0, "fundofase1.png")

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state == "start":
            # Aguarda Enter ou Espaço para começar
            if not self.start_screen.update_conect():
                self.state = "game"
                GameLogger.game_start_log()  # Log aparente de início do jogo
            return
        elif self.state == "game":
            self.fase1.update_fase1()
            if self.fase1.win:
                self.state = "victory"
                return
            if self.fase1.lose:
                self.state = "lose"
                return
            # -------- se clicar em ESC volta pra tela inicial -------------------#
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                self.state = "start"
                return
        elif self.state == "victory":
            if self.victory_screen.update():
                # Reinicia a fase e volta ao menu inicial
                self.fase1 = Fase1()
                self.state = "start"
                return
        elif self.state == "lose":
            if self.lose_screen.update():
                # Reinicia a fase e volta ao menu inicial
                self.fase1 = Fase1()
                self.state = "start"
                return

    def draw(self):
        if self.state == "start":
            self.start_screen.desenhastart()
        elif self.state == "game":
            self.fase1.draw_fase1()
        elif self.state == "victory":
            self.victory_screen.draw()
        elif self.state == "lose":
            self.lose_screen.draw()


CandyMazeGame()