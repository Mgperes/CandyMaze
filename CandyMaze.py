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

    def draw_rainbow_text(self, text, x, y):
        """
        Desenha texto com cada letra em uma cor diferente (efeito arco-íris)
        
        PALETA DE CORES PYXEL:
        0 = Preto        8 = Vermelho
        1 = Azul escuro  9 = Laranja  
        2 = Roxo         10 = Amarelo
        3 = Verde escuro 11 = Verde claro
        4 = Marrom       12 = Azul claro
        5 = Cinza escuro 13 = Cinza
        6 = Cinza claro  14 = Rosa/Branco rosado
        7 = Branco       15 = Bege claro
        """
        colors = [8, 9, 10, 11, 12, 13, 14, 15, 7, 6, 5, 4, 3, 2, 1]  # Paleta de cores
        for i, char in enumerate(text):
            color_index = (i + int(self.rainbow_offset)) % len(colors)
            color = colors[color_index]
            pyxel.text(x + i * 4, y, char, color)
    
    def draw_blinking_text(self, text, x, y):
        # Desenha texto piscante com cores alternadas
        if self.color_timer % 30 < 15:  # Pisca a cada 30 frames (15 frames cada cor)
            color = 8  # Vermelho
        else:
            color = 12  # Azul claro
        pyxel.text(x, y, text, color)
    
    def draw_gradient_text(self, text, x, y):
        # Desenha texto com gradiente de cores que se move
        colors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Gradiente completo
        for i, char in enumerate(text):
            color_index = (i + self.color_timer // 8) % len(colors)
            color = colors[color_index]
            pyxel.text(x + i * 4, y, char, color)
    
    def draw_wave_text(self, text, x, y):
        # Desenha texto com efeito de onda (cores se movem como ondas)
        import math
        for i, char in enumerate(text):
            wave = math.sin((self.color_timer + i * 10) * 0.1)
            color = int(8 + wave * 4)  # Varia entre cores 4-12
            if color < 1: color = 1
            if color > 15: color = 15
            pyxel.text(x + i * 4, y, char, color)
    
    def draw_fire_text(self, text, x, y):
        # Desenha texto com efeito de fogo (cores quentes)
        fire_colors = [8, 9, 10, 14, 7]  # Vermelho, laranja, amarelo, branco
        for i, char in enumerate(text):
            # Cria um efeito aleatório usando o frame count
            color_index = (self.color_timer + i * 3) % len(fire_colors)
            color = fire_colors[color_index]
            pyxel.text(x + i * 4, y, char, color)

    def desenhastart(self):
        pyxel.cls(14)
        pyxel.blt(0, 0, 0, 0, 0, 250, 220)  
        
        # ====== OPÇÕES DE TEXTO COLORIDO ======
        # Descomente apenas uma das opções abaixo para testar diferentes efeitos:
        
        
        # MÉTODO 1: Efeito Rainbow - cada letra uma cor diferente 
        # self.draw_rainbow_text("START  |", 90, 130)
        # self.draw_rainbow_text("(Q)UIT", 118, 130)
        
        # MÉTODO 2: Texto piscante com duas cores alternadas
        #self.draw_blinking_text("START  |", 90, 130)
        #self.draw_blinking_text("(Q)UIT", 118, 130)
        
        # MÉTODO 3: Gradiente animado
        # self.draw_gradient_text("START |", 90, 130)
        # self.draw_gradient_text("(Q)UIT", 118, 130)
        
        # MÉTODO 4: Efeito onda com matemática (ativo) ✨
        self.draw_wave_text("START |", 90, 130)
        self.draw_wave_text(" (Q)UIT", 118, 130)

        # MÉTODO 5: Efeito fogo (cores quentes)
        # self.draw_fire_text("START |", 90, 130)
        # self.draw_fire_text(" (Q)UIT", 118, 130)

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
        self.personagem = Personagem(2, y_chao - altura_personagem)
        self.x = 0
        self.y = 0
        self.colisao = False
        self.win = False
        self.win_counter = 0  # Contador de frames na porta final
        self.x_lago1 = 204
        self.y_lago1 = 212
        self.largura_lago1 = 20   #posicão inicial e tamanho do primeiro lago
        self.altura_lago1 = 8
        self.afogando = False
        self.lose = False
        self.afogar_timer = 0
        self.x_lago2 = 137
        self.y_lago2 = 68
        self.largura_lago2 = 40   #posicão inicial e tamanho do segundo lago
        self.altura_lago2 = 8
        self.x_lago3 = 50
        self.y_lago3 = 116
        self.largura_lago3 = 20   #posicão inicial e tamanho do terceiro lago
        self.altura_lago3 = 8
        self.plataforma = Plataforma()
        self.sobre_agua = False
        
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

        self.x_lago1 += 0.5 #movimento do lago para a direita, e corte na largura de acordo com o movimento
        if self.largura_lago1 > 0 and self.x_lago1 < 224:
            self.largura_lago1 -= 0.5
        else:                #quando chega no limite imposto ele volta para a posicão inicial para reiniciar o movimento
            self.largura_lago1 = 20
            self.x_lago1 = 204
    
    #----------LAGO2--------------
        self.x_lago2 += 0.5 #movimento do lago para a direita, e corte na largura de acordo com o movimento
        if self.largura_lago2 > 0 and self.x_lago2 < 177:
            self.largura_lago2 -= 0.5
        else:                #quando chega no limite imposto ele volta para a posicão inicial para reiniciar o movimento
            self.largura_lago2 = 40
            self.x_lago2 = 137

    #----------LAGO3--------------
        self.x_lago3 += 0.5 #movimento do lago para a direita, e corte na largura de acordo com o movimento
        if self.largura_lago3 > 0 and self.x_lago3 < 70:
            self.largura_lago3 -= 0.5
        else:                #quando chega no limite imposto ele volta para a posicão inicial para reiniciar o movimento
            self.largura_lago3 = 20
            self.x_lago3 = 50



        # ------------------- Detecta se personagem está sobre a água dos lagos (APÓS movimento) -------------------#
        px, py, pl, pa = self.personagem.x, self.personagem.y, self.personagem.largura, self.personagem.altura

        # Verifica colisão com Lago 1 (x=204, y=212)
        if (px + pl > 203 and px < 204 + 10 and
            py + pa > 211.5 and py < 211.5 + 8):
            GameLogger.death_log("TOCOU NO LAGO 1! O personagem se afogou instantaneamente!")
            self.lose = True

        # Verifica colisão com Lago 2 (x=137, y=68)
        elif (px + pl > 136 and px < 137 + 30 and
              py + pa > 67.5 and py < 67.5 + 8):
            GameLogger.death_log("TOCOU NO LAGO 2! O personagem se afogou instantaneamente!")
            self.lose = True

        # Verifica colisão com Lago 3 (x=50, y=116)
        elif (px + pl > 49 and px < 50 + 10 and
              py + pa > 115.5 and py < 115.5 + 8):
            GameLogger.death_log("TOCOU NO LAGO 3! O personagem se afogou instantaneamente!")
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



        if self.win or self.lose:
            return

    def paredes(self):
        
            self.parede1 = pyxel.blt(122, 172, 1, 191, 0, 6, 40)  # parede vertical
            self.parede2 = pyxel.blt(35, 164, 1, 56, 40, 180, 8)  # parede horizontal 1
            self.parede3 = pyxel.blt(0, 116, 1, 0, 72, 100, 8,7)  # parede horizontal 2
            self.parede4 = pyxel.blt(150, 116, 1, 150, 72, 100, 8)  # parede horizontal 3
            self.parede5 = pyxel.blt(40, 68, 1, 0, 80, 210, 8,7)   # parede horizontal 4

    def vidas(self):
        pass

    def draw_fase1(self):
        pyxel.cls(6)
        pyxel.blt(0, 0, 2, 0, 0, 250, 220)
        pyxel.mouse(False) # mouse desativado

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

        # Desenha o personagem ANTES do lago
        self.personagem.desenhapersonagem()

        #----LAGO1-------
        pyxel.blt(self.x_lago1, self.y_lago1, 1, 101, 0, self.largura_lago1, self.altura_lago1,7) #primeira imagem do looping do lago
        pyxel.blt(self.x_lago1 - 20, self.y_lago1, 1, 101, 0, 20, self.altura_lago1,7)  #segunda imagem do looping do lago
        pyxel.blt(self.x_lago1 - 40, self.y_lago1, 1, 101, 0, 20, self.altura_lago1,7)   #terceira imagem do looping do lago
       #-----LAGO2--------
        pyxel.blt(self.x_lago2, self.y_lago2, 1, 56, 16, self.largura_lago2, self.altura_lago2,7) 
        pyxel.blt(self.x_lago2 - 40, self.y_lago2, 1, 56, 16, 40, self.altura_lago2,7) 
        pyxel.blt(self.x_lago2 - 80, self.y_lago2, 1, 56, 16, 40, self.altura_lago2,7) 
        pyxel.blt(self.x_lago2 - 95, self.y_lago2, 1, 56, 16, 15, self.altura_lago2,7)   
        #-----LAGO3--------
        pyxel.blt(self.x_lago3, self.y_lago3, 1, 56, 24, self.largura_lago3, self.altura_lago3,7) 
        pyxel.blt(self.x_lago3 - 20, self.y_lago3, 1, 56, 24, 20, self.altura_lago3,7)  
        pyxel.blt(self.x_lago3 - 40, self.y_lago3, 1, 56, 24, 20, self.altura_lago3,7) 


        pyxel.text(5+0.5, 5+0.5, "FASE 1", self.colortext)
        pyxel.text(5, 5, "FASE 1", 0)
        pyxel.blt(0, 212, 1, 0, 88, 250, 8,7) # chão
        pyxel.blt(self.plataforma.x,42,1,56,32,24,8) #plataforma móvel
        self.paredes()

        pyxel.blt(145, 199, 1, 121, 0, 7, 7,7)
        
        

        


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