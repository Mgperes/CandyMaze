import pyxel
import math 
import random

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

class InstructionsScreen:
    #Classe responsável por desenhar e gerenciar a tela de instruções
    
    def __init__(self, color_timer=0):
        self.color_timer = color_timer
        self.box_width = 180
        self.box_height = 140
        self.box_x = (250 - self.box_width) // 2  # Centraliza horizontalmente
        self.box_y = (220 - self.box_height) // 2  # Centraliza verticalmente
        
        # Lista de instruções
        self.instructions = [
            "COMO JOGAR:",
            "",
            "- Use setas para mover",
            "- Pressione ESPACO para pular",
            "- Colete balas (score)",
            "- Fuja da agua dos lagos",
            "- Chegue na porta, o tempo e seu inimigo!!",
            "- Pressione F para pausar",
            "",
            "Press SPACE to start!"
        ]
        
        # Tipos de balas para decoração (baseados na classe Balas)
        self.candy_types = [
            (96, 16, 9, 12),   # Bala especial
            (106, 8, 9, 9),    # Bala dourada 
            (130, 9, 9, 9),    # Bala comum 
            (121, 0, 9, 9),    # Bala comum 
            (130, 0, 9, 9),    # Bala comum 
        ]
        # Estado dos brilhos (partículas) — para movimento aleatório
        self.sparkle_count = 18
        self.sparkles = []
        for _ in range(self.sparkle_count):
            sx = random.uniform(0, 250)
            sy = random.uniform(0, 220)
            # evita nascer dentro da caixa
            if self.box_x <= sx <= self.box_x + self.box_width and self.box_y <= sy <= self.box_y + self.box_height:
                # empurra para fora com margem
                if random.random() < 0.5:
                    sy = self.box_y - random.uniform(6, 28)
                else:
                    sx = self.box_x - random.uniform(6, 28)
            svx = random.uniform(-0.6, 0.6)
            svy = random.uniform(-0.6, 0.6)
            ssize = random.choice([1, 1, 2])
            scol = random.choice([7, 8, 9, 10, 11, 12, 14])
            self.sparkles.append({"x": sx, "y": sy, "vx": svx, "vy": svy, "size": ssize, "col": scol})
    
    def update(self, color_timer):
        """Atualiza o timer de cores para animações"""
        self.color_timer = color_timer
        # Atualiza partículas de brilho
        if hasattr(self, 'sparkles'):
            self._update_sparkles()
    
    def draw(self):
        """Desenha a tela de instruções completa"""
        # Desenha o background da fase 1
        pyxel.blt(0, 0, 2, 0, 0, 250, 220)
        # Desenha brilhos por baixo do quadrado (para que NÃO fiquem na frente)
        if hasattr(self, 'sparkles'):
            self.draw_sparkles_around_box()

        # Desenha paredes de chocolate ao redor do quadrado
        self.draw_chocolate_walls()
        
        # Desenha o quadrado das instruções com cores mais alegres
        pyxel.rect(self.box_x, self.box_y, self.box_width, self.box_height, 10)  # Fundo verde claro alegre
        pyxel.rectb(self.box_x, self.box_y, self.box_width, self.box_height, 9)   # Borda laranja alegre
        pyxel.rectb(self.box_x + 1, self.box_y + 1, self.box_width - 2, self.box_height - 2, 8)  # Borda amarela
        pyxel.rectb(self.box_x + 2, self.box_y + 2, self.box_width - 4, self.box_height - 4, 14)  # Borda rosa
        
        # Adiciona balas decorativas nas bordas
        self.draw_candy_decorations()
        
        # Desenha o texto das instruções
        self.draw_instructions_text()
    
    def draw_instructions_text(self):
        """Desenha o texto das instruções"""
        start_y = self.box_y + 12
        for i, line in enumerate(self.instructions):
            text_x = self.box_x + 8
            text_y = start_y + i * 12
            
            if i == 0:  # Título com gradiente
                # Desenha sombra preta primeiro
                for char_i, char in enumerate(line):
                    pyxel.text(text_x + 1 + char_i * 4, text_y + 1, char, 0)
                # Desenha o texto com gradiente
                self.draw_gradient_text(line, text_x, text_y)
            elif "Press SPACE to start!" in line:  # Instrução final com gradiente também
                # Desenha sombra preta primeiro
                for char_i, char in enumerate(line):
                    pyxel.text(text_x + 1 + char_i * 4, text_y + 1, char, 0)
                # Desenha o texto com gradiente
                self.draw_gradient_text(line, text_x, text_y)
            else:  # Instruções normais
                pyxel.text(text_x, text_y, line, 0)  # Texto preto
    
    def draw_gradient_text(self, text, x, y):
        """Desenha texto com gradiente de cores que se move"""
        colors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Gradiente completo
        for i, char in enumerate(text):
            color_index = (i + self.color_timer // 8) % len(colors)
            color = colors[color_index]
            pyxel.text(x + i * 4, y, char, color)
    
    def draw_candy_decorations(self):
        """Desenha balas decorativas variadas ao redor da caixa de instruções"""
        candy_index = 0
        
        # Balas nas bordas superior e inferior - melhor espaçamento
        candy_spacing = 25
        start_x = self.box_x + 12
        end_x = self.box_x + self.box_width - 12
        
        for x in range(start_x, end_x, candy_spacing):
            if x + 12 <= end_x:  # Verifica se cabe (ajustado para maior bala 9x12)
                candy = self.candy_types[candy_index % len(self.candy_types)]
                # Borda superior - posiciona sobre a parede
                pyxel.blt(x, self.box_y - 12, 1, candy[0], candy[1], candy[2], candy[3], 7)
                # Borda inferior - posiciona sobre a parede
                candy = self.candy_types[(candy_index + 1) % len(self.candy_types)]
                pyxel.blt(x, self.box_y + self.box_height + 4, 1, candy[0], candy[1], candy[2], candy[3], 7)
                candy_index += 1
        
        # Balas nas bordas laterais - melhor espaçamento
        candy_spacing_v = 35
        start_y = self.box_y + 20
        end_y = self.box_y + self.box_height - 20
        
        for y in range(start_y, end_y, candy_spacing_v):
            if y + 12 <= end_y:  # Verifica se cabe (ajustado para maior bala 9x12)
                candy = self.candy_types[candy_index % len(self.candy_types)]
                # Borda esquerda - posiciona ao lado da parede
                pyxel.blt(self.box_x - 14, y, 1, candy[0], candy[1], candy[2], candy[3], 7)
                # Borda direita - posiciona ao lado da parede
                candy = self.candy_types[(candy_index + 1) % len(self.candy_types)]
                pyxel.blt(self.box_x + self.box_width + 6, y, 1, candy[0], candy[1], candy[2], candy[3], 7)
                candy_index += 1
        
        # Balas especiais nos cantos - tamanhos corretos da classe Balas
        pyxel.blt(self.box_x - 12, self.box_y - 12, 1, 106, 8, 9, 9, 7)  # Canto superior esquerdo - bala dourada
        pyxel.blt(self.box_x + self.box_width + 4, self.box_y - 12, 1, 130, 9, 9, 9, 7)  # Canto superior direito - bala comum
        pyxel.blt(self.box_x - 12, self.box_y + self.box_height + 4, 1, 96, 16, 9, 12, 7)  # Canto inferior esquerdo - bala especial
        pyxel.blt(self.box_x + self.box_width + 4, self.box_y + self.box_height + 4, 1, 121, 0, 9, 9, 7)  # Canto inferior direito - bala comum

    def draw_sparkles_around_box(self):
        # Desenha brilhos com base em self.sparkles
        
        if not hasattr(self, 'sparkles'):
            return

        for s in self.sparkles:
            x = int(s['x'])
            y = int(s['y'])
            size = s.get('size', 1)
            col = s.get('col', 7)
            # desenha apenas se estiver dentro da tela
            if x < 0 or x >= 250 or y < 0 or y >= 220:
                continue
            if size <= 1:
                pyxel.pset(x, y, col)
            else:
                # retângulo pequeno centrado
                pyxel.rect(max(0, x - 1), max(0, y - 1), size, size, col)

        # efeito de brilho extra ocasional
        if (self.color_timer % 30) < 6:
            for i in range(0, len(self.sparkles), 6):
                s = self.sparkles[i]
                bx = int(s['x'])
                by = int(s['y'])
                if 0 <= bx < 250 and 0 <= by < 220:
                    pyxel.pset(bx, by, 15)

    def _update_sparkles(self):
        """Atualiza posições das partículas e garante que elas não entrem na área do box."""
        for s in self.sparkles:
            # pequena aleatoriedade na velocidade
            if random.random() < 0.08:
                s['vx'] += random.uniform(-0.12, 0.12)
                s['vy'] += random.uniform(-0.12, 0.12)

            # limita velocidade
            s['vx'] = max(-1.2, min(1.2, s['vx']))
            s['vy'] = max(-1.2, min(1.2, s['vy']))

            # atualiza posição
            s['x'] += s['vx']
            s['y'] += s['vy']

            # rebater nas bordas da tela
            if s['x'] < 0:
                s['x'] = 0
                s['vx'] *= -1
            if s['x'] > 249:
                s['x'] = 249
                s['vx'] *= -1
            if s['y'] < 0:
                s['y'] = 0
                s['vy'] *= -1
            if s['y'] > 219:
                s['y'] = 219
                s['vy'] *= -1

            # se entrou na área do box, empurra para fora para a borda mais próxima
            if (self.box_x <= s['x'] <= self.box_x + self.box_width and
                    self.box_y <= s['y'] <= self.box_y + self.box_height):
                left_dist = abs(s['x'] - self.box_x)
                right_dist = abs(self.box_x + self.box_width - s['x'])
                top_dist = abs(s['y'] - self.box_y)
                bottom_dist = abs(self.box_y + self.box_height - s['y'])
                m = min(left_dist, right_dist, top_dist, bottom_dist)
                margin = 6 + random.uniform(0, 10)
                if m == left_dist:
                    s['x'] = self.box_x - margin
                elif m == right_dist:
                    s['x'] = self.box_x + self.box_width + margin
                elif m == top_dist:
                    s['y'] = self.box_y - margin
                else:
                    s['y'] = self.box_y + self.box_height + margin

                # ajusta velocidade para apontar para fora
                cx = self.box_x + self.box_width / 2
                cy = self.box_y + self.box_height / 2
                dx = s['x'] - cx
                dy = s['y'] - cy
                norm = max(0.1, math.hypot(dx, dy))
                s['vx'] = (dx / norm) * (0.6 + random.random() * 0.8)
                s['vy'] = (dy / norm) * (0.6 + random.random() * 0.8)

    def draw_chocolate_walls(self):
        """Desenha paredes de chocolate ao redor do quadrado formando bordas"""
        # Posições base das paredes
        parede_esquerda_x = self.box_x - 6  # Parede esquerda mais para fora
        parede_direita_x = self.box_x + self.box_width  # Parede direita alinhada com a borda
        parede_topo_y = self.box_y - 8  # Parede superior
        parede_base_y = self.box_y + self.box_height  # Parede inferior
        
        # PRIMEIRO: PAREDES VERTICAIS 
        altura_necessaria = self.box_height + 16  # Altura total incluindo bordas
        segmentos_verticais = (altura_necessaria + 39) // 40  # Quantos segmentos de 40px precisamos
        
        # Paredes verticais esquerdas
        for i in range(segmentos_verticais):
            y_pos = parede_topo_y + (i * 40)
            altura_segmento = min(40, altura_necessaria - (i * 40))
            if altura_segmento > 0:
                pyxel.blt(parede_esquerda_x, y_pos, 1, 191, 0, 6, altura_segmento, 7)
        
        # Paredes verticais direitas 
        for i in range(segmentos_verticais):
            y_pos = parede_topo_y + (i * 40)
            altura_segmento = min(40, altura_necessaria - (i * 40))
            if altura_segmento > 0:
                pyxel.blt(parede_direita_x, y_pos, 1, 191, 0, 6, altura_segmento, 7)
        
        # SEGUNDO: PAREDES HORIZONTAIS (ficam na frente das verticais)
        # Parede superior - primeira camada
        pyxel.blt(self.box_x - 6, parede_topo_y, 1, 56, 40, self.box_width + 12, 8, 7)
        # Parede superior - segunda camada 
        pyxel.blt(self.box_x + 100, parede_topo_y, 1, 56, 40, 86, 8, 7)
        
        # Parede inferior - primeira camada
        pyxel.blt(self.box_x - 6, parede_base_y, 1, 56, 40, self.box_width + 12, 8, 7)
        # Parede inferior - segunda camada
        pyxel.blt(self.box_x + 100, parede_base_y, 1, 56, 40, 86, 8, 7)

class Start:
    def __init__(self):
        self.colortext = 7
        self.hover_timer = 0
        self.x = 0
        self.y = 0
        self.width = 250
        self.height = 180
        self.color_timer = 0
        self.rainbow_offset = 0
        self.last_hover_start = False
        self.last_hover_quit = False


    def update_conect(self):
        self.color_timer += 1
        self.rainbow_offset += 0.1

        # Área do botão Start (
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
        
        # Som de hover nos botões
        if mouse_over_start and not self.last_hover_start:
            pyxel.play(1, 8)  
        if mouse_over_quit and not self.last_hover_quit:
            pyxel.play(1, 8)  
            
        self.last_hover_start = mouse_over_start
        self.last_hover_quit = mouse_over_quit

        # Clique em QUIT ou aperte o "Q "para fechar o jogo
        if mouse_over_quit and (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_Q)):
            pyxel.quit()
        # Clique em ENTER ou ESPAÇO para iniciar
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            pyxel.play(0, 4)  
            return False
    
        # Clique do mouse inicia o jogo se estiver sobre o texto Start
        if mouse_over_start and (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
            pyxel.play(0, 4)  # Som de menu/click
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

class pause:
    def __init__ (self):
        self.tempo_pause = 0
        self.pausado = False

    def update_pause(self):
        if pyxel.btnp(pyxel.KEY_F):
            print(f"Tecla F pressionada! tempo_pause: {self.tempo_pause}")
            self.tempo_pause += 1
            if self.tempo_pause % 2 == 1:
                self.pausado = True
                print("PAUSADO!")
                pyxel.stop(0)
                pyxel.stop(1)
                pyxel.stop(2)
                pyxel.stop(3)
            else:
                self.pausado = False
                print("DESPAUSADO!")
        return self.pausado
    
    def draw_pause_overlay(self):
        if self.pausado:
            for y in range(0, 220, 2):
                    pyxel.line(0, y, 250, y, 0)
            
            pause_text = "PAUSE"
            text2 = "- Press F para continuar -"

            # Calcula posição central
            text_x = (250 - len(pause_text) * 4) // 2
            inst_x = (250 - len(text2) * 4) // 2

            
            pyxel.text(text_x + 1, 101, pause_text, 0)  
            pyxel.text(text_x, 100, pause_text, 7)      

            pyxel.text(inst_x + 1, 121, text2, 0)  
            pyxel.text(inst_x, 120, text2, 6)      

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

class tempo:
    def __init__(self):
        self.tempo = 0 and True
        self.lose = False
        self.tempo_limite = 1000 # dividir por 20 fps = 50 segundos
    def update(self):  
        self.tempo += 1
        if self.tempo > self.tempo_limite:
            return True
        return False
        

    def draw(self):

        tempo_restante = max(0, (self.tempo_limite - self.tempo) // 20)
        pyxel.text(195+0.5, 5+0.5, f"TEMPO: {tempo_restante:02}s", 7)
        pyxel.text(195, 5, f"TEMPO: {tempo_restante:02}s", 0)
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

class Balas:
    def __init__(self):
        self.score = 0
        self.balas = [[130,9,121,128,9,9,False],   # Lista de Balas: [x_mem, y_mem, x, y, largura, altura, coletada]
                      [130,9,44,84,9,9,False],
                      [130,9,175,103,9,9,False],
                      [130,9,225,103,9,9,False],
                      [121,0,100,199,9,9,False],
                      [121,0,196,180,9,9,False],
                      [121,0,127,28,9,9,False],
                      [121,0,50,199,9,9,False],
                      [121,0,140,199,9,9,False],
                      [121,0,91,28,9,9,False],
                      [121,0,161,28,9,9,False],
                      [96,16,70,150,9,12,False],
                      [96,16,121,80,9,12,False],
                      [96,16,180,150,9,12,False],
                      [96,16,10,25,9,12,False],
                      [130,0,121,141,9,9,False],
                      [130,0,10,135,9,9,False],
                      [130,0,231,135,9,9,False]
                      ]
        
    def update(self,x_personagem,y_personagem):
        for i in range(len(self.balas)):  # Itera sobre a lista, que agora tem 7 elementos por item
            self.bala_xmem = self.balas[i][0]
            self.bala_ymem = self.balas[i][1]
            self.bala_x = self.balas[i][2]
            self.bala_y = self.balas[i][3]
            self.bala_w = self.balas[i][4] 
            self.bala_h = self.balas[i][5]  
            self.coletada = self.balas[i][6]
            if not self.coletada:
                self.colisao = (x_personagem + 14 >= self.bala_x and     
                          x_personagem <= self.bala_x + self.bala_w and 
                          y_personagem <= self.bala_y + self.bala_h and     
                          y_personagem + 18 >= self.bala_y)    
                if self.colisao:
                        # 1. Faz a bala sumir (muda o estado na lista: índice 6)
                        self.balas[i][6] = True 
                        if i == 11 or i == 12 or i == 13 or i == 14: 
                            self.score += 75
                        else:
                            self.score += 50

    def draw(self):
        score_text = f"SCORE: {self.score}"
        pyxel.text(125+0.5, 5+0.5, score_text, 7)
        pyxel.text(125, 5, score_text, 0) 
        pyxel.blt(112,3,1,106,8,9,9,7)
        # Desenha APENAS as balas que têm o estado 'coletada' como False
        for self.bala_xmem, self.bala_ymem, self.bala_x, self.bala_y, self.bala_w, self.bala_h, self.coletada in self.balas:
            if not self.coletada:
                # desenha cada bala
                pyxel.blt(self.bala_x, self.bala_y, 1, self.bala_xmem, self.bala_ymem, self.bala_w, self.bala_h, 7)


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

        # Sistema de instruções
        self.showing_instructions = True
        self.first_time_playing = True
        self.color_timer = 0  # Timer para animação do gradiente
        self.instructions_screen = InstructionsScreen(self.color_timer)  # Nova classe de instruções

        self.tempo = tempo()
        self.formiga = formiga()
        self.balas = Balas()

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
        self.mx_inicial_lago1 = 184
        self.mlargura_total_lago1 = 35
        self.afogando = False
        self.lose = False
        self.afogar_timer = 0
        self.mx_lago2 = 137
        self.my_lago2 = 68
        self.mlargura_lago2 = 40   #posicão inicial e tamanho do segundo lago
        self.maltura_lago2 = 8
        self.mx_inicial_lago2 = 86
        self.mlargura_total_lago2 = 90 
        self.mx_lago3 = 50
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
            self.pause_system = pause()

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

        if self.tempo.update():
            GameLogger.death_log("💀 GAME OVER! Tempo esgotado! 💀")
            pyxel.play(3, 2)
            self.lose = True
            return


        # Checa colisão do personagem com a porta final
        if (
            self.personagem.x < self.porta_x + self.porta_w and
            self.personagem.x + self.personagem.largura > self.porta_x and
            self.personagem.y < self.porta_y + self.porta_h and
            self.personagem.y + self.personagem.altura > self.porta_y
        ):
            self.win_counter += 1 
            if self.win_counter == 1:  
                GameLogger.info_log("Personagem chegou na porta final!")
            elif self.win_counter == 10:  
                GameLogger.warning_log("Aguardando confirmação de vitória...")
            elif self.win_counter > 20: 
                if not self.win:  
                    GameLogger.success_log("🎉 PARABÉNS! VOCÊ VENCEU O CANDY MAZE! 🎉")
                    pyxel.play(2, 3)  
                self.win = True
            else:
                self.win = False
        else:
            if self.win_counter > 0:  # Saiu da porta 
                GameLogger.warning_log("Saiu da porta! Volte para vencer essa fase!")
            self.win_counter = 0  # Reseta contador se sair da porta
            self.win = False

        #----TESTA COLISAO COM BALA------
        self.balas.update(self.personagem.x,self.personagem.y)  


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
                GameLogger.death_log("💀 TOCOU NA ÁGUA! O personagem está se afogando... 💀")
                print("COLISÃO DETECTADA COM LAGO 1!")

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
                GameLogger.death_log("💀 TOCOU NA ÁGUA! O personagem está se afogando... 💀")
                print("COLISÃO DETECTADA COM LAGO 2!")

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
                GameLogger.death_log("💀 TOCOU NA ÁGUA! O personagem está se afogando... 💀")
                print("COLISÃO DETECTADA COM LAGO 3!")

        # Sistema de morte lenta e inevitável 
        if self.afogando:
            self.afogar_timer += 1
            tempo_restante = (40 - self.afogar_timer) / 20  # Converte frames para segundos (fps=20)
            self.personagem.x_mem = 56   #muda a animacão
            self.personagem.y_mem = 48
            
            
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
                pyxel.play(3, 2)  # Som de morte/afogamento
                self.lose = True





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
                
                GameLogger.warning_log("💥 Bateu a cabeça na plataforma móvel grande!")

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
                self.formiga_collision_cooldown = 30  
                self.invencibilidade_timer = 30 
                
                pyxel.play(2, 1)  # Som de dano/colisão com formiga
                GameLogger.danger_log(f"🐜 FORMIGA ATACOU! {lado_tocado} encostou na formiga! Vidas restantes: {self.personagem.vidas}")
                
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
                    GameLogger.death_log("💀 GAME OVER! Todas as vidas foram perdidas! 💀")
                    pyxel.play(3, 2)  # Som de morte
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
    def __init__(self, score_atual=0):
        self.colortext = 7
        self.width = 250
        self.height = 220
        self.animation_timer = 0
        self.personagem = Personagem(117, 135)  # Posição inicial fixa
        self.dx = 0
        self.dy = 0
        self.animacao_ativa = False
        self.som_tocado = False
        self.posicao_inicial_y = 135  # Guarda a posição inicial para calcular a distância
        self.balas = Balas()
        
        # Sistema de Score
        self.score_atual = score_atual
        self.score_maximo = self.calcular_score_maximo()
        self.score_animado = 0
        self.score_animation_speed = 2
        self.score_animation_complete = False
        self.percentual = (self.score_atual / self.score_maximo * 100) if self.score_maximo > 0 else 0
    
    def calcular_score_maximo(self):
        """Calcula o score máximo possível baseado nas balas disponíveis"""
        score_max = 0
        # Balas especiais (índices 11, 12, 13, 14) valem 75 pontos
        balas_especiais = [11, 12, 13, 14]
        # Balas normais valem 50 pontos
        total_balas = 18  # Total de balas no jogo
        
        for i in range(total_balas):
            if i in balas_especiais:
                score_max += 75
            else:
                score_max += 50
        
        return score_max

    def update(self):
        self.animation_timer += 1
        
        # Animação do score (sempre ativa)
        if not self.score_animation_complete:
            if self.score_animado < self.score_atual:
                self.score_animado += self.score_animation_speed
                if self.score_animado >= self.score_atual:
                    self.score_animado = self.score_atual
                    self.score_animation_complete = True
        
        # Se a animação não foi iniciada e o jogador pressiona Enter/Espaço
        if not self.animacao_ativa and (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE)):
            if not self.som_tocado:
                pyxel.play(0, 4)  # Som de menu/click
                self.som_tocado = True
            self.animacao_ativa = True
            self.dy = 2 
            self.posicao_inicial_y = self.personagem.y 
            return False
        
        if self.animacao_ativa:
            self.personagem.y += self.dy
            
            frame_cycle = (self.animation_timer // 6) % 4  
            
            self.personagem.contX = frame_cycle
            self.personagem.contY = 0  
            
            # Calcula as posições na sprite sheet
            self.personagem.x_mem = self.personagem.contX * self.personagem.largura  # 0, 14, 28, 42
            self.personagem.y_mem = self.personagem.contY * self.personagem.altura   # 0 (primeira linha)
            
            if self.personagem.y >= 188:  
                return True  
            else:
                return False  
        
        return False

    def draw(self):
        pyxel.cls(0)
        # Fundo gradiente (mantém o original)
        for y in range(220):
            if y < 73:
                color = 12 # Azul claro
                pyxel.blt(0, 0, 2, 0, 20, 250, y) # Desenha o fundo azul claro
            elif y < 146:
                color = 14  # Rosa
                pyxel.line(0, y, 250, y, color)
            elif y < 206:
                color = pyxel.COLOR_DARK_BLUE
                pyxel.line(0, y, 250, y, color)
            else:
                color = 10  # Amarelo
                pyxel.line(0, y, 250, y, color)
        
        
        # Lago 1 - Lado esquerdo
        if not hasattr(self, 'mx_lago1'):
            self.mx_lago1 = -5  
            self.mlargura_lago1 = 20
        
        self.mx_lago1 += 0.3 
        if self.mlargura_lago1 > 0 and self.mx_lago1 < 25:  
            self.mlargura_lago1 -= 0.3
        else:
            self.mlargura_lago1 = 20
            self.mx_lago1 = -5  
        for offset_y in range(0, 56, 6):  
            pyxel.blt(int(self.mx_lago1), 144 + offset_y, 1, 56, 16, int(self.mlargura_lago1), 8, 7)
            pyxel.blt(int(self.mx_lago1) - 24, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago1) - 48, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago1) - 72, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago1) - 96, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 120, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 144, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 168, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 192, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 216, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 240, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 264, 144 + offset_y, 1, 56, 16, 20, 8, 7)

        # Lago 2 - Centro
        if not hasattr(self, 'mx_lago2'):
            self.mx_lago2 = 55  # Começa 5px mais à esquerda
            self.mlargura_lago2 = 20
        
        self.mx_lago2 += 0.4
        if self.mlargura_lago2 > 0 and self.mx_lago2 < 90:  
            self.mlargura_lago2 -= 0.4
        else:
            self.mlargura_lago2 = 20
            self.mx_lago2 = 55  
        for offset_y in range(0, 56, 6):  
            pyxel.blt(int(self.mx_lago2), 144 + offset_y, 1, 56, 16, int(self.mlargura_lago2), 8, 7)
            pyxel.blt(int(self.mx_lago2) - 29, 144 + offset_y, 1, 56, 16, 20, 8, 7)  # -29 para sobreposição de 4px
            pyxel.blt(int(self.mx_lago2) - 58, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago2) - 87, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago2) - 116, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago2) - 145, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago2) - 174, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago2) - 203, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago2) - 232, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
        
        # Lago 3 - Lado direito
        if not hasattr(self, 'mx_lago3'):
            self.mx_lago3 = 115  
            self.mlargura_lago3 = 20
        
        self.mx_lago3 += 0.35
        if self.mlargura_lago3 > 0 and self.mx_lago3 < 140: 
            self.mlargura_lago3 -= 0.35
        else:
            self.mlargura_lago3 = 20
            self.mx_lago3 = 115  
        
        for offset_y in range(0, 56, 6):  
            pyxel.blt(int(self.mx_lago3), 144 + offset_y, 1, 101, 0, int(self.mlargura_lago3), 8, 7)
            pyxel.blt(int(self.mx_lago3) - 21, 144 + offset_y, 1, 101, 0, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago3) - 42, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 63, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 84, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 105, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 126, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 147, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 168, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 189, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 210, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 231, 144 + offset_y, 1, 101, 0, 20, 8, 7)  

       
        if not hasattr(self, 'mx_lago4'):
            self.mx_lago4 = 135  
            self.mlargura_lago4 = 20
        
        self.mx_lago4 += 0.32 
        if self.mlargura_lago4 > 0 and self.mx_lago4 < 155:  
            self.mlargura_lago4 -= 0.32
        else:
            self.mlargura_lago4 = 20
            self.mx_lago4 = 135  
        
        for offset_y in range(0, 56, 6):  
            pyxel.blt(int(self.mx_lago4), 144 + offset_y, 1, 101, 0, int(self.mlargura_lago4), 8, 7)
            pyxel.blt(int(self.mx_lago4) - 21, 144 + offset_y, 1, 101, 0, 20, 8, 7) 
            pyxel.blt(int(self.mx_lago4) - 42, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 63, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 84, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 105, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 126, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 147, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 168, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 189, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 210, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 231, 144 + offset_y, 1, 101, 0, 20, 8, 7)

        
        if not hasattr(self, 'mx_lago5'):
            self.mx_lago5 = 155  
            self.mlargura_lago5 = 20

        self.mx_lago5 += 0.38  
        if self.mlargura_lago5 > 0 and self.mx_lago5 < 175:  
            self.mlargura_lago5 -= 0.38
        else:
            self.mlargura_lago5 = 20
            self.mx_lago5 = 155  
 
        # Desenha lago 5 com sobreposição de 4px
        for offset_y in range(0, 56, 6):
            pyxel.blt(int(self.mx_lago5), 144 + offset_y, 1, 56, 16, int(self.mlargura_lago5), 8, 7)
            pyxel.blt(int(self.mx_lago5) - 29, 144 + offset_y, 1, 56, 16, 20, 8, 7) 
            pyxel.blt(int(self.mx_lago5) - 58, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago5) - 87, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago5) - 116, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago5) - 145, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago5) - 174, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago5) - 203, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago5) - 232, 144 + offset_y, 1, 56, 16, 20, 8, 7)

        if not hasattr(self, 'mx_lago6'):
            self.mx_lago6 = 175  
            self.mlargura_lago6 = 20

        self.mx_lago6 += 0.36  # Velocidade intermediária
        if self.mlargura_lago6 > 0 and self.mx_lago6 < 195:  # Limite final
            self.mlargura_lago6 -= 0.36
        else:
            self.mlargura_lago6 = 20
            self.mx_lago6 = 175  
        for offset_y in range(0, 56, 6):
            pyxel.blt(int(self.mx_lago6), 144 + offset_y, 1, 101, 0, int(self.mlargura_lago6), 8, 7)
            pyxel.blt(int(self.mx_lago6) - 21, 144 + offset_y, 1, 101, 0, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago6) - 42, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 63, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 84, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 105, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 126, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 147, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 168, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 189, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 210, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 231, 144 + offset_y, 1, 101, 0, 20, 8, 7)

        if not hasattr(self, 'mx_lago7'):
            self.mx_lago7 = 195  
            self.mlargura_lago7 = 20
        
        self.mx_lago7 += 0.3  
        if self.mlargura_lago7 > 0 and self.mx_lago7 < 215:  
            self.mlargura_lago7 -= 0.3
        else:
            self.mlargura_lago7 = 20
            self.mx_lago7 = 195  
        for offset_y in range(0, 56, 6):  
            pyxel.blt(int(self.mx_lago7), 144 + offset_y, 1, 56, 16, int(self.mlargura_lago7), 8, 7)
            pyxel.blt(int(self.mx_lago7) - 24, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago7) - 48, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago7) - 72, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago7) - 96, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 120, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 144, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 168, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 192, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 216, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 240, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 264, 144 + offset_y, 1, 56, 16, 20, 8, 7)

       
        if not hasattr(self, 'mx_lago8'):
            self.mx_lago8 = 215  
            self.mlargura_lago8 = 20
        
        self.mx_lago8 += 0.4 
        if self.mlargura_lago8 > 0 and self.mx_lago8 < 240: 
            self.mlargura_lago8 -= 0.4
        else:
            self.mlargura_lago8 = 20
            self.mx_lago8 = 215  
        for offset_y in range(0, 56, 6):  
            pyxel.blt(int(self.mx_lago8), 144 + offset_y, 1, 56, 16, int(self.mlargura_lago8), 8, 7)
            pyxel.blt(int(self.mx_lago8) - 29, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago8) - 58, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago8) - 87, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago8) - 116, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago8) - 145, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago8) - 174, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago8) - 203, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago8) - 232, 144 + offset_y, 1, 56, 16, 20, 8, 7)  

        
        if not hasattr(self, 'mx_lago9'):
            self.mx_lago9 = 240  
            self.mlargura_lago9 = 20
        
        self.mx_lago9 += 0.35 
        if self.mlargura_lago9 > 0 and self.mx_lago9 < 265:  
            self.mlargura_lago9 -= 0.35
        else:
            self.mlargura_lago9 = 20
            self.mx_lago9 = 240  
        
        for offset_y in range(0, 56, 6):  
            pyxel.blt(int(self.mx_lago9), 144 + offset_y, 1, 101, 0, int(self.mlargura_lago9), 8, 7)
            pyxel.blt(int(self.mx_lago9) - 21, 144 + offset_y, 1, 101, 0, 20, 8, 7)  # -21 igual lago 3
            pyxel.blt(int(self.mx_lago9) - 42, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 63, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 84, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 105, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 126, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 147, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 168, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 189, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 210, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 231, 144 + offset_y, 1, 101, 0, 20, 8, 7)

        # Lago 10 - Final até 270px (250 + 20)
        if not hasattr(self, 'mx_lago10'):
            self.mx_lago10 = 265  # Começa onde o lago 9 termina
            self.mlargura_lago10 = 20
        
        self.mx_lago10 += 0.3  # Velocidade igual ao lago 1
        if self.mlargura_lago10 > 0 and self.mx_lago10 < 290:  # Até 270px + margem
            self.mlargura_lago10 -= 0.3
        else:
            self.mlargura_lago10 = 20
            self.mx_lago10 = 265 
        for offset_y in range(0, 56, 6): 
            pyxel.blt(int(self.mx_lago10), 144 + offset_y, 1, 56, 16, int(self.mlargura_lago10), 8, 7)
            pyxel.blt(int(self.mx_lago10) - 24, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago10) - 48, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago10) - 72, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago10) - 96, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 120, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 144, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 168, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 192, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 216, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 240, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 264, 144 + offset_y, 1, 56, 16, 20, 8, 7)


        # Animação de chão se formando (POR CIMA DOS LAGOS)
        x_chaoinicial1 = 115
        y_chaoinicial1 = 143
        W_chaolargura1 = 21
        x_chaoinicial2 = x_chaoinicial1
        y_chaoinicial2 = y_chaoinicial1
        W_chaolargura2 = 21

        # Animação de chão se formando (ORIGINAL)
        for i in range(1, 63):
            ch = pyxel.blt(x_chaoinicial1, y_chaoinicial1, 1, 56, 40, W_chaolargura1, 8, 7)
            if W_chaolargura1 >= 180:
                ch = pyxel.blt(x_chaoinicial2, y_chaoinicial2, 1, 56, 40, W_chaolargura2, 8, 7)
                x_chaoinicial2 -= 1
                y_chaoinicial2 += 1
                W_chaolargura2 += 2
            else:
                ch = pyxel.blt(x_chaoinicial1, y_chaoinicial1, 1, 56, 40, W_chaolargura1, 8, 7)
                x_chaoinicial1 -= 1
                y_chaoinicial1 += 1
                W_chaolargura1 += 2
        
        pyxel.blt(0, 204, 1, 0, 88, 160, 8, 7) # chão final
        pyxel.blt(160, 204, 1, 0, 88, 90, 8, 7) # chão final
        # Título principal
        title_text = "SWEET VICTORY!"
        title_x = 65
        title_y = 59
        x_title_mem_sweet1 = 197
        y_title_mem_sweet1 = 22
        y_title_mem_sweet2 = 31

        #sweet
        pyxel.blt(title_x + 2, title_y + 2, 1, x_title_mem_sweet1, y_title_mem_sweet1, 50, 9, 7 )
        pyxel.blt(title_x , title_y, 1, x_title_mem_sweet1, y_title_mem_sweet2, 50, 9, 7 )

        #victory
        pyxel.blt(title_x + 52, title_y + 2, 1, 70, 48, 62, 9, 7)
        pyxel.blt(title_x + 50, title_y, 1, 70, 57, 62, 9, 7)
        

        
        # Coração  
        heart_x = 120
        heart_y = 90
        pyxel.blt(heart_x, heart_y, 1, 139, 9, 10, 7, 7)
        
        # Porta aberta
        door_x = 115
        door_y = 110
        pyxel.blt(door_x, door_y, 1, 170, 0, 21, 31, 7)
        

        
        
        if not self.animacao_ativa:
            # Antes da animação - personagem comemorando na posição fixa
            char_x = 117
            char_y = 135
            
            if char_y >= 73 and char_y <= 146: 
                brilho_offsets = [
                    (-10, -8), (20, -6), (-7, 12), (18, 14),  # Cantos
                    (7, -10), (-5, 24), (22, 10), (0, -12)    # Meio
                ]
                for i, (offset_x, offset_y) in enumerate(brilho_offsets):
                    # Movimento suave e brilho piscante
                    brilho_x = char_x + offset_x + math.sin(self.animation_timer * 0.1 + i * 0.8) * 4
                    brilho_y = char_y + offset_y + math.cos(self.animation_timer * 0.08 + i * 1.2) * 3
                    
                    # Brilho com efeito de piscar (mais frequente)
                    if (self.animation_timer + i * 12) % 50 < 40:  # Visível na maior parte do tempo
                        pyxel.pset(int(brilho_x), int(brilho_y), 7)        # Pixel branco
                        pyxel.pset(int(brilho_x + 1), int(brilho_y), 15)   # Pixel pêssego claro
                        pyxel.pset(int(brilho_x), int(brilho_y + 1), 10)   # Pixel amarelo
            
            if self.animation_timer % 40 < 20:
                pyxel.blt(char_x, char_y, 1, 14, 0, 14, 18, 7)  # Pose de comemoração
            else:
                pyxel.blt(char_x, char_y, 1, 0, 0, 14, 18, 7)  # Pose padrão
        else:
            if self.personagem.y >= 73 and self.personagem.y <= 146:  # Só na zona rosa claro
                # Brilhos pequenos ao redor do personagem em movimento
                brilho_offsets = [
                    (-8, -6), (18, -4), (-5, 10), (20, 12),  
                    (7, -8), (-3, 22), (22, 8), (2, -10)     
                ]
                for i, (offset_x, offset_y) in enumerate(brilho_offsets):
                    brilho_x = self.personagem.x + offset_x + math.sin(self.animation_timer * 0.15 + i * 0.6) * 5
                    brilho_y = self.personagem.y + offset_y + math.cos(self.animation_timer * 0.12 + i * 1.0) * 4
                    
                    if (self.animation_timer + i * 8) % 35 < 28:  
                        pyxel.pset(int(brilho_x), int(brilho_y), 7)        # Pixel branco
                        pyxel.pset(int(brilho_x + 1), int(brilho_y), 15)   # Pixel pêssego claro
                        pyxel.pset(int(brilho_x), int(brilho_y + 1), 10)   # Pixel amarelo
                        
            pyxel.blt(self.personagem.x, self.personagem.y, 1, self.personagem.x_mem, self.personagem.y_mem, 
                     self.personagem.largura, self.personagem.altura, 7)
        
            
        
        
        # Instrução para jogar novamente (só mostra se animação não iniciou)
        if not self.animacao_ativa:
            instruction_text = "Press ENTER to play again!"
            text_x = 72
            text_y = 189
            
            # Efeito de piscar
            if self.animation_timer % 100 < 80:  # Visível na maior parte do tempo
                pyxel.text(text_x + 1, text_y + 1, instruction_text, 0)  # Sombra
                pyxel.text(text_x, text_y, instruction_text, 7)  # Texto branco
        
        # Moldura nas bordas (só se animação não iniciou)
        if not self.animacao_ativa:
            pyxel.line(0, 5, 250, 5, 15)  # Linha pêssego clara
            pyxel.line(0, 215, 250, 215, 15)
            pyxel.rect(237, 10, 3, 3, 15)
            pyxel.rect(10, 10, 3, 3, 15)

            # Painel de Score Melhorado 
            panel_x = 5
            panel_y = 75
            panel_w = 85
            panel_h = 60
            
            # Fundo do painel com bordas
            pyxel.rect(panel_x, panel_y, panel_w, panel_h, 0)  # Fundo preto
            pyxel.rectb(panel_x, panel_y, panel_w, panel_h, 15)  # Borda pêssego
            pyxel.rectb(panel_x + 1, panel_y + 1, panel_w - 2, panel_h - 2, 7)  # Borda interna branca
            
            # Título do painel
            pyxel.text(panel_x + 3, panel_y + 3, "SCORE", 15)
            
            # Score atual formatado como "ganhos / total pts"
            score_text = f"{int(self.score_animado)} / 1000 pts"
            pyxel.text(panel_x + 3, panel_y + 15, score_text, 11)  # Verde claro
            
            # Percentual
            percent_text = f"Progress: {int(self.percentual)}%"
            color_percent = 11 if self.percentual >= 80 else 10 if self.percentual >= 60 else 8
            pyxel.text(panel_x + 3, panel_y + 27, percent_text, color_percent)
            
            # Mensagem de desempenho dentro do painel
            if self.percentual == 100:
                msg = "PERFECT!"
                msg_color = 11
            elif self.percentual >= 80:
                msg = "EXCELLENT!"
                msg_color = 10
            elif self.percentual >= 60:
                msg = "GOOD!"
                msg_color = 8
            else:
                msg = "TRY HARDER!"
                msg_color = 6
            pyxel.text(panel_x + 3, panel_y + 39, msg, msg_color)
            
            # Barra de progresso dentro do painel
            bar_x = panel_x + 3
            bar_y = panel_y + 51
            bar_w = panel_w - 8
            bar_h = 6
            
            # Fundo da barra
            pyxel.rect(bar_x, bar_y, bar_w, bar_h, 1)  # Fundo azul escuro
            pyxel.rectb(bar_x, bar_y, bar_w, bar_h, 7)  # Borda branca
            
            # Preenchimento da barra baseado no percentual
            fill_width = int((self.percentual / 100) * (bar_w - 2))
            if fill_width > 0:
                fill_color = 11 if self.percentual >= 80 else 10 if self.percentual >= 60 else 8
                pyxel.rect(bar_x + 1, bar_y + 1, fill_width, bar_h - 2, fill_color)
            
            # Efeito de brilho se score completo
            if self.percentual == 100:
                blink_frame = self.animation_timer % 60
                if blink_frame < 30:
                    # Brilho dourado ao redor do painel
                    pyxel.rectb(panel_x - 1, panel_y - 1, panel_w + 2, panel_h + 2, 10)  # Borda dourada

            # Efeito de brilho se score completo
            if self.percentual == 100:
                blink_frame = self.animation_timer % 60
                if blink_frame < 30:
                    # Brilho dourado ao redor do painel
                    pyxel.rectb(panel_x - 1, panel_y - 1, panel_w + 2, panel_h + 2, 10)  # Borda dourada

        pyxel.mouse(False)
#----------------- LoseScreen ---------------------------------------------------------------------------------------#
class LoseScreen:
    def __init__(self, score_atual=0):
        self.colortext = 8 
        self.width = 250
        self.height = 220
        self.animation_timer = 0
        self.char_x = 20.0  
        self.char_y = 145.0  # Posiciona no meio da nova área permitida (entre 129 e 172)
        self.velocity_x = 0.0  
        self.velocity_y = 0.0  
        self.target_x = 20.0  
        self.target_y = 145.0  # Target inicial também no meio da nova área permitida
        self.direction_timer = 0
        
        # Sistema de Score
        self.score_atual = score_atual
        self.score_maximo = self.calcular_score_maximo()
        self.score_animado = 0
        self.score_animation_speed = 1.5
        self.score_animation_complete = False
        self.percentual = (self.score_atual / self.score_maximo * 100) if self.score_maximo > 0 else 0
    
    def calcular_score_maximo(self):
        """Calcula o score máximo possível baseado nas balas disponíveis"""
        score_max = 0
        # Balas especiais (índices 11, 12, 13, 14) valem 75 pontos
        balas_especiais = [11, 12, 13, 14]
        # Balas normais valem 50 pontos
        total_balas = 18  # Total de balas no jogo
        
        for i in range(total_balas):
            if i in balas_especiais:
                score_max += 75
            else:
                score_max += 50
        
        return score_max  

    def update(self):
        self.animation_timer += 1
        self.direction_timer += 1
        
        # Animação do score (sempre ativa)
        if not self.score_animation_complete:
            if self.score_animado < self.score_atual:
                self.score_animado += self.score_animation_speed
                if self.score_animado >= self.score_atual:
                    self.score_animado = self.score_atual
                    self.score_animation_complete = True
        
        # A cada 120 frames (6 segundos a 20fps), escolhe nova direção
        if self.direction_timer >= 120:
            # Escolhe nova posição alvo aleatória dentro da área permitida
            self.target_x = random.uniform(20, 140)  # Margem de 20px das bordas
            self.target_y = random.uniform(129, 172)  # Entre Y=129 (15px acima dos lagos) e Y=172 (metade dos lagos)
            self.direction_timer = 0
        
        lerp_speed = 0.02 
        
        # Calcula a diferença entre posição atual e alvo
        diff_x = self.target_x - self.char_x
        diff_y = self.target_y - self.char_y
        
        # Move gradualmente em direção ao alvo
        self.char_x += diff_x * lerp_speed
        self.char_y += diff_y * lerp_speed
        
        # Adiciona um leve movimento de flutuação (oscilação suave)
        float_offset_x = math.sin(self.animation_timer * 0.05) * 2
        float_offset_y = math.cos(self.animation_timer * 0.03) * 1.5
        
        # Aplica a flutuação à posição final
        final_x = self.char_x + float_offset_x
        final_y = self.char_y + float_offset_y
        
        # Limita o movimento para criar efeito de afogamento
        # Os lagos começam em y=144 e terminam em y=200
        # Limita o personagem entre y=129 (15px acima dos lagos) e y=172 (metade da altura dos lagos)
        limite_superior = 129  # Y = 144 - 15px (15 pixels acima do início dos lagos)
        limite_inferior = 172  # Metade da altura dos lagos (144 + 56/2 = 172)
        
        # Garante que não saia da tela e respeita os limites de afogamento
        self.char_x = max(10, min(final_x, 230))
        self.char_y = max(limite_superior, min(final_y, limite_inferior))

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            pyxel.play(0, 4)  # Som de menu/click
            return True
        return False
    

    def draw(self):
        pyxel.cls(0)  # Fundo preto 
        for y in range(220):
            if y < 73:
                color = pyxel.COLOR_DARK_BLUE  # Céu azul claro
            elif y < 146:
                color = pyxel.COLOR_NAVY
            else:
                color = pyxel.COLOR_DARK_BLUE
            pyxel.line(0, y, 250, y, color)
               
        
        title_x = 75
        title_y = 57
        x_mem_title = 132
        y_mem_title1 = 48
        y_mem_title2 = 57

        pyxel.blt(title_x + 2, title_y + 2, 1, x_mem_title, y_mem_title1, 90, 10, 7)
        pyxel.blt(title_x , title_y, 1, x_mem_title, y_mem_title2, 90, 10, 7)

        # Desenha o personagem na frente do painel de score mas atrás dos lagos
        pyxel.blt(int(self.char_x), int(self.char_y), 1, 0, 0, 14, 18, 7)

        # Lago 1 - Lado esquerdo
        if not hasattr(self, 'mx_lago1'):
            self.mx_lago1 = -5  # Começa 5px mais à esquerda
            self.mlargura_lago1 = 20
        
        self.mx_lago1 += 0.3 
        if self.mlargura_lago1 > 0 and self.mx_lago1 < 25:  
            self.mlargura_lago1 -= 0.3
        else:
            self.mlargura_lago1 = 20
            self.mx_lago1 = -5  # Reposiciona 5px mais à esquerda
        
        # Desenha lago 1 com sobreposição de 4px (24px em vez de 28px de distância) e 2 fileiras a menos
        for offset_y in range(0, 56, 6):  # y=144 até y=200 (56 pixels de altura) com 2px mais juntas
            pyxel.blt(int(self.mx_lago1), 144 + offset_y, 1, 56, 16, int(self.mlargura_lago1), 8, 7)
            pyxel.blt(int(self.mx_lago1) - 24, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago1) - 48, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago1) - 72, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago1) - 96, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 120, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 144, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 168, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 192, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 216, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 240, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago1) - 264, 144 + offset_y, 1, 56, 16, 20, 8, 7)

        # Lago 2 - Centro
        if not hasattr(self, 'mx_lago2'):
            self.mx_lago2 = 55  # Começa 5px mais à esquerda
            self.mlargura_lago2 = 20
        
        self.mx_lago2 += 0.4
        if self.mlargura_lago2 > 0 and self.mx_lago2 < 90:  
            self.mlargura_lago2 -= 0.4
        else:
            self.mlargura_lago2 = 20
            self.mx_lago2 = 55  # Reposiciona 5px mais à esquerda
        
        # Desenha lago 2 com sobreposição de 4px e 2 fileiras a menos
        for offset_y in range(0, 56, 6):  # y=144 até y=200 com 2px mais juntas
            pyxel.blt(int(self.mx_lago2), 144 + offset_y, 1, 56, 16, int(self.mlargura_lago2), 8, 7)
            pyxel.blt(int(self.mx_lago2) - 29, 144 + offset_y, 1, 56, 16, 20, 8, 7)  # -29 para sobreposição de 4px
            pyxel.blt(int(self.mx_lago2) - 58, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago2) - 87, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago2) - 116, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago2) - 145, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago2) - 174, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago2) - 203, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago2) - 232, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
        
        # Lago 3 - Lado direito
        if not hasattr(self, 'mx_lago3'):
            self.mx_lago3 = 115  
            self.mlargura_lago3 = 20
        
        self.mx_lago3 += 0.35
        if self.mlargura_lago3 > 0 and self.mx_lago3 < 140: 
            self.mlargura_lago3 -= 0.35
        else:
            self.mlargura_lago3 = 20
            self.mx_lago3 = 115  
        
        # Desenha lago 3 com sobreposição de 4px e 2 fileiras a menos
        for offset_y in range(0, 56, 6):  # y=144 até y=200 com 2px mais juntas
            pyxel.blt(int(self.mx_lago3), 144 + offset_y, 1, 101, 0, int(self.mlargura_lago3), 8, 7)
            pyxel.blt(int(self.mx_lago3) - 21, 144 + offset_y, 1, 101, 0, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago3) - 42, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 63, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 84, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 105, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 126, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 147, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 168, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 189, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 210, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago3) - 231, 144 + offset_y, 1, 101, 0, 20, 8, 7)  

        # Lago 4 - Continuação do lado direito
        if not hasattr(self, 'mx_lago4'):
            self.mx_lago4 = 135  # Começa mais próximo ao lago 3
            self.mlargura_lago4 = 20
        
        self.mx_lago4 += 0.32  # Velocidade ligeiramente diferente
        if self.mlargura_lago4 > 0 and self.mx_lago4 < 155:  # Limite ajustado
            self.mlargura_lago4 -= 0.32
        else:
            self.mlargura_lago4 = 20
            self.mx_lago4 = 135  # Reset correto
        
        # Desenha lago 4 com sobreposição de 4px (seguindo padrão dos outros)
        for offset_y in range(0, 56, 6):  # Mesma altura e espaçamento dos outros lagos
            pyxel.blt(int(self.mx_lago4), 144 + offset_y, 1, 101, 0, int(self.mlargura_lago4), 8, 7)
            pyxel.blt(int(self.mx_lago4) - 21, 144 + offset_y, 1, 101, 0, 20, 8, 7)  # -21 para sobreposição de 4px (igual lago 3)
            pyxel.blt(int(self.mx_lago4) - 42, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 63, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 84, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 105, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 126, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 147, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 168, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 189, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 210, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago4) - 231, 144 + offset_y, 1, 101, 0, 20, 8, 7)

        # Lago 5 - Continuação mais à direita
        if not hasattr(self, 'mx_lago5'):
            self.mx_lago5 = 155  # Começa onde o lago 4 termina
            self.mlargura_lago5 = 20

        self.mx_lago5 += 0.38  # Velocidade ligeiramente maior
        if self.mlargura_lago5 > 0 and self.mx_lago5 < 175:  # Limite adequado
            self.mlargura_lago5 -= 0.38
        else:
            self.mlargura_lago5 = 20
            self.mx_lago5 = 155  # Reset correto

        # Desenha lago 5 com sobreposição de 4px
        for offset_y in range(0, 56, 6):
            pyxel.blt(int(self.mx_lago5), 144 + offset_y, 1, 56, 16, int(self.mlargura_lago5), 8, 7)
            pyxel.blt(int(self.mx_lago5) - 29, 144 + offset_y, 1, 56, 16, 20, 8, 7)  # -29 para sobreposição de 4px (igual lago 2)
            pyxel.blt(int(self.mx_lago5) - 58, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago5) - 87, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago5) - 116, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago5) - 145, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago5) - 174, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago5) - 203, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago5) - 232, 144 + offset_y, 1, 56, 16, 20, 8, 7)

        # Lago 6 - Continuação da sequência
        if not hasattr(self, 'mx_lago6'):
            self.mx_lago6 = 175  # Começa onde o lago 5 termina
            self.mlargura_lago6 = 20

        self.mx_lago6 += 0.36  # Velocidade intermediária
        if self.mlargura_lago6 > 0 and self.mx_lago6 < 195:  # Limite final
            self.mlargura_lago6 -= 0.36
        else:
            self.mlargura_lago6 = 20
            self.mx_lago6 = 175  # Reset correto

        # Desenha lago 6 com sobreposição de 4px
        for offset_y in range(0, 56, 6):
            pyxel.blt(int(self.mx_lago6), 144 + offset_y, 1, 101, 0, int(self.mlargura_lago6), 8, 7)
            pyxel.blt(int(self.mx_lago6) - 21, 144 + offset_y, 1, 101, 0, 20, 8, 7)  # -21 para sobreposição de 4px (igual lago 3)
            pyxel.blt(int(self.mx_lago6) - 42, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 63, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 84, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 105, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 126, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 147, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 168, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 189, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 210, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago6) - 231, 144 + offset_y, 1, 101, 0, 20, 8, 7)

        # Lago 7 - Continuação seguindo padrão do lago 1
        if not hasattr(self, 'mx_lago7'):
            self.mx_lago7 = 195  # Começa onde o lago 6 termina
            self.mlargura_lago7 = 20
        
        self.mx_lago7 += 0.3  # Mesma velocidade do lago 1
        if self.mlargura_lago7 > 0 and self.mx_lago7 < 215:  # Limite de 20 pixels
            self.mlargura_lago7 -= 0.3
        else:
            self.mlargura_lago7 = 20
            self.mx_lago7 = 195  # Reset correto
        
        # Desenha lago 7 com padrão do lago 1 (sprite 56, 16 e sobreposição -24)
        for offset_y in range(0, 56, 6):  # y=144 até y=200 (56 pixels de altura) com 2px mais juntas
            pyxel.blt(int(self.mx_lago7), 144 + offset_y, 1, 56, 16, int(self.mlargura_lago7), 8, 7)
            pyxel.blt(int(self.mx_lago7) - 24, 144 + offset_y, 1, 56, 16, 20, 8, 7)  # -24 igual lago 1
            pyxel.blt(int(self.mx_lago7) - 48, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago7) - 72, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago7) - 96, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 120, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 144, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 168, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 192, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 216, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 240, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago7) - 264, 144 + offset_y, 1, 56, 16, 20, 8, 7)

        # Lago 8 - Continuação seguindo padrão do lago 2
        if not hasattr(self, 'mx_lago8'):
            self.mx_lago8 = 215  # Começa onde o lago 7 termina
            self.mlargura_lago8 = 20
        
        self.mx_lago8 += 0.4  # Mesma velocidade do lago 2
        if self.mlargura_lago8 > 0 and self.mx_lago8 < 240:  # Limite ajustado
            self.mlargura_lago8 -= 0.4
        else:
            self.mlargura_lago8 = 20
            self.mx_lago8 = 215  # Reset correto
        
        # Desenha lago 8 com padrão do lago 2 (sprite 56, 16 e sobreposição -29)
        for offset_y in range(0, 56, 6):  # y=144 até y=200 com 2px mais juntas
            pyxel.blt(int(self.mx_lago8), 144 + offset_y, 1, 56, 16, int(self.mlargura_lago8), 8, 7)
            pyxel.blt(int(self.mx_lago8) - 29, 144 + offset_y, 1, 56, 16, 20, 8, 7)  # -29 igual lago 2
            pyxel.blt(int(self.mx_lago8) - 58, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago8) - 87, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago8) - 116, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago8) - 145, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago8) - 174, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago8) - 203, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago8) - 232, 144 + offset_y, 1, 56, 16, 20, 8, 7)  

        # Lago 9 - Continuação final seguindo padrão do lago 3
        if not hasattr(self, 'mx_lago9'):
            self.mx_lago9 = 240  # Começa onde o lago 8 termina
            self.mlargura_lago9 = 20
        
        self.mx_lago9 += 0.35  # Mesma velocidade do lago 3
        if self.mlargura_lago9 > 0 and self.mx_lago9 < 265:  # Limite até 265px
            self.mlargura_lago9 -= 0.35
        else:
            self.mlargura_lago9 = 20
            self.mx_lago9 = 240  # Reset correto
        
        # Desenha lago 9 com padrão do lago 3 (sprite 101, 0 e sobreposição -21)
        for offset_y in range(0, 56, 6):  # y=144 até y=200 com 2px mais juntas
            pyxel.blt(int(self.mx_lago9), 144 + offset_y, 1, 101, 0, int(self.mlargura_lago9), 8, 7)
            pyxel.blt(int(self.mx_lago9) - 21, 144 + offset_y, 1, 101, 0, 20, 8, 7)  # -21 igual lago 3
            pyxel.blt(int(self.mx_lago9) - 42, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 63, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 84, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 105, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 126, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 147, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 168, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 189, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 210, 144 + offset_y, 1, 101, 0, 20, 8, 7)
            pyxel.blt(int(self.mx_lago9) - 231, 144 + offset_y, 1, 101, 0, 20, 8, 7)

        # Lago 10 - Final até 270px (250 + 20)
        if not hasattr(self, 'mx_lago10'):
            self.mx_lago10 = 265  # Começa onde o lago 9 termina
            self.mlargura_lago10 = 20
        
        self.mx_lago10 += 0.3  # Velocidade igual ao lago 1
        if self.mlargura_lago10 > 0 and self.mx_lago10 < 290:  # Até 270px + margem
            self.mlargura_lago10 -= 0.3
        else:
            self.mlargura_lago10 = 20
            self.mx_lago10 = 265  # Reset correto
        
        # Desenha lago 10 com padrão do lago 1 (sprite 56, 16 e sobreposição -24)
        for offset_y in range(0, 56, 6):  # y=144 até y=200 com 2px mais juntas
            pyxel.blt(int(self.mx_lago10), 144 + offset_y, 1, 56, 16, int(self.mlargura_lago10), 8, 7)
            pyxel.blt(int(self.mx_lago10) - 24, 144 + offset_y, 1, 56, 16, 20, 8, 7)  # -24 igual lago 1
            pyxel.blt(int(self.mx_lago10) - 48, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago10) - 72, 144 + offset_y, 1, 56, 16, 20, 8, 7)  
            pyxel.blt(int(self.mx_lago10) - 96, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 120, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 144, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 168, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 192, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 216, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 240, 144 + offset_y, 1, 56, 16, 20, 8, 7)
            pyxel.blt(int(self.mx_lago10) - 264, 144 + offset_y, 1, 56, 16, 20, 8, 7)
        

        pyxel.blt(170, 130, 1, 150, 72, 100, 8)
        # Uma formiga solitária no canto (menos poluído)
        formiga_x = 200 + math.sin(self.animation_timer * 0.05) * 5
        formiga_y = 120
        pyxel.blt(int(formiga_x), formiga_y, 1, 197, 0, 18, 11, 7)
        
        # Painel de Score da Derrota 
        panel_x = 5
        panel_y = 75
        panel_w = 85
        panel_h = 60
        
        # Fundo do painel com bordas melancólicas
        pyxel.rect(panel_x, panel_y, panel_w, panel_h, 0)  
        pyxel.rectb(panel_x, panel_y, panel_w, panel_h, 2)  # Borda roxa escura
        pyxel.rectb(panel_x + 1, panel_y + 1, panel_w - 2, panel_h - 2, 6)  # Borda interna cinza claro
        
        # Título do painel
        pyxel.text(panel_x + 3, panel_y + 3, "SCORE", 8)  # Vermelho
        
        # Score atual formatado como "ganhos / total pts"
        score_text = f"{int(self.score_animado)} / 1000 pts"
        pyxel.text(panel_x + 3, panel_y + 15, score_text, 11)  # Verde claro
        
        # Percentual
        percent_text = f"Progress: {int(self.percentual)}%"
        color_percent = 11 if self.percentual >= 80 else 10 if self.percentual >= 60 else 8
        pyxel.text(panel_x + 3, panel_y + 27, percent_text, color_percent)
        
        # Mensagem motivacional dentro do painel
        if self.percentual == 100:
            msg = "PERFECT!"
            msg_color = 11
        elif self.percentual >= 80:
            msg = "EXCELLENT!"
            msg_color = 10
        elif self.percentual >= 50:
            msg = "TRY HARDER!"
            msg_color = 8
        else:
            msg = "YOU CAN DO IT!"
            msg_color = 6
            
        pyxel.text(panel_x + 3, panel_y + 39, msg, msg_color)
        
        # Barra de progresso dentro do painel
        bar_x = panel_x + 3
        bar_y = panel_y + 51
        bar_w = panel_w - 8
        bar_h = 6
        
        # Fundo da barra
        pyxel.rect(bar_x, bar_y, bar_w, bar_h, 0)  # Fundo preto
        pyxel.rectb(bar_x, bar_y, bar_w, bar_h, 6)  # Borda cinza claro
        
        # Preenchimento da barra baseado no percentual
        fill_width = int((self.percentual / 100) * (bar_w - 2))
        if fill_width > 0:
            fill_color = 11 if self.percentual >= 80 else 10 if self.percentual >= 60 else 8
            pyxel.rect(bar_x + 1, bar_y + 1, fill_width, bar_h - 2, fill_color)

        instruction_text = "Don't give up! Press ENTER to try again"
        text_x = 45
        text_y = 180
        
        
        if self.animation_timer % 120 < 90:  # Mais tempo visível
            pyxel.text(text_x + 1, text_y + 1, instruction_text, 0)  # Sombra
            pyxel.text(text_x, text_y, instruction_text, 7)  # Texto branco 
        
        # Moldura
        pyxel.line(0, 5, 250, 5, 2)   # Linha roxa escura
        pyxel.line(0, 215, 250, 215, 2)
        
        # Cantos 
        pyxel.rect(10, 10, 2, 2, 2)
        pyxel.rect(238, 10, 2, 2, 2)
        pyxel.rect(10, 208, 2, 2, 2)
        pyxel.rect(238, 208, 2, 2, 2)
        
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
        self.victory_screen = None  
        self.lose_screen = None      
        self.transition_played = False

        #-------- carrega as imagens --------#
        pyxel.images[0].load(0, 0, "background.png")
        pyxel.images[1].load(0, 0, "itens.png")
        pyxel.images[2].load(0, 0, "fundofase1.png")

        #-------- configuração de áudio --------#
        self.setup_audio()

        pyxel.run(self.update, self.draw)

    def setup_audio(self):
        
        # caso o personagem for ter a função de atirar:

        """pyxel.sounds[0].set(
            notes="A4 G#4 G4 F#4 F4 E4 D#4 D4 C#4 C4 B3 A#3 A3 G3 F#3 F3",  
            tones="TTTTTTTTTTTTTTTT",   
            volumes="6666555544443333", 
            effects="NNNNNNNNNNNNNNNN", 
            speed=3                 
        )""" 



        # Som de pulo
        pyxel.sounds[0].set(
            notes="A3 G#3 G3 F#3 F3 E3 D#3 D3 C#3 C3 B2 A#2 A2 G2 F#2 F2",  
            tones="TTTTTTTTTTTTTTTT",   
            volumes="6666555544443333", 
            effects="NNNNNNNNNNNNNNNN", 
            speed=3
        )

        # Som de dano/colisão com formiga
        pyxel.sounds[1].set(
            notes="F2E2D2C2", 
            tones="TTTT", 
            volumes="3221", 
            effects="NNNN", 
            speed=15
        )
        
        # Som de morte
        pyxel.sounds[2].set(
            notes="G3F3E3D3C3", 
            tones="TTTTT", 
            volumes="43321", 
            effects="NNNNN", 
            speed=20
        )
        
        # Som de vitória 
        pyxel.sounds[3].set(
            notes="C3E3G3C4G3E3C3", 
            tones="TTTTTTT", 
            volumes="3454543", 
            effects="NNNNNNN", 
            speed=20
        )
        
        # Som de menu/click 
        pyxel.sounds[4].set(
            notes="E3", 
            tones="T", 
            volumes="2", 
            effects="N", 
            speed=40
        )
        
        # Som ambiente da fase 1 
        pyxel.sounds[5].set(
            notes="C3E3G3C3F3A2D3F3E3G3C3E3G2A2F2G2C3D3F3E3C3G2", 
            tones="TTTTTTSSTTTTSSSSTTSSTTTT", 
            volumes="2321232123212321232123", 
            effects="NNNNNNNNNNNNNNNNNNNNNN", 
            speed=22  
        )
        
        # Som do menu 
        pyxel.sounds[6].set(
            notes="C2E2G2F2E2D2C2G2", 
            tones="SSSSSSSS", 
            volumes="12211221", 
            effects="NNNNNNNN", 
            speed=120
        )
        
        # Som de toque na água 
        pyxel.sounds[7].set(
            notes="G3F3E3", 
            tones="SSS", 
            volumes="321", 
            effects="NNN", 
            speed=25
        )
        
        # Som de hover no menu 
        pyxel.sounds[8].set(
            notes="C4", 
            tones="T", 
            volumes="1", 
            effects="N", 
            speed=50
        )
        
        # Trilha de apoio 
        pyxel.sounds[9].set(
            notes="C2R R G1R R F1R R C2R R G1R R ", 
            tones="SNSNSNSNSNSNSN", 
            volumes="10101010101010", 
            effects="NNNNNNNNNNNNNN", 
            speed=24  # Batida mais espaçada e suave
        )
        
        # Som de transição menu -> fase 
        pyxel.sounds[10].set(
            notes="C3G3C4E4G4C4", 
            tones="TTTTTT", 
            volumes="234543", 
            effects="NNNNNN", 
            speed=30 
        )

    def play_sound(self, sound_id, channel=0):
        """Toca um som específico em um canal"""
        pyxel.play(channel, sound_id)

    def update(self):
        if self.state == "start":
            if not pyxel.play_pos(0):  
                pyxel.play(0, 6, loop=True)  
            
            # Aguarda Enter ou Espaço para começar
            if not self.start_screen.update_conect():
                pyxel.stop(0)  # Para o som do menu
                # Toca som de transição antes de iniciar a fase
                pyxel.play(0, 10)  
                self.transition_played = False  
                self.state = "game"
                GameLogger.game_start_log()  
            return
        elif self.state == "game":
            
            self.fase1.update_fase1()
            
            
            if hasattr(self.fase1, 'pause_system') and self.fase1.pause_system.pausado:
                # Se o jogo está pausado, para todas as trilhas da fase
                pyxel.stop(0)
                pyxel.stop(1)
                return
                
            # Aguarda a transição terminar antes de tocar a música da fase
            if not pyxel.play_pos(0) and not self.transition_played:
                # Transição terminou, agora toca a música da fase
                pyxel.play(0, 5, loop=True)  
                pyxel.play(1, 9, loop=True)  
                self.transition_played = True
            elif not pyxel.play_pos(0) and self.transition_played:
                # Se a música parou, reinicia (só acontece se necessário)
                pyxel.play(0, 5, loop=True)
            if not pyxel.play_pos(1) and self.transition_played:
                pyxel.play(1, 9, loop=True)
            if self.fase1.win:
                # Para todas as trilhas da fase
                pyxel.stop(0)
                pyxel.stop(1) 
                # Cria nova tela de vitória a cada vitória com o score atual
                self.victory_screen = VictoryScreen(self.fase1.balas.score)
                self.state = "victory"
                return
            if self.fase1.lose:
                # Para todas as trilhas da fase
                pyxel.stop(0)
                pyxel.stop(1)
                # Cria nova tela de derrota a cada derrota com o score atual
                self.lose_screen = LoseScreen(self.fase1.balas.score)
                self.state = "lose"
                return
            # -------- se clicar em ESC volta pra tela inicial -------------------#
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                pyxel.stop(0)  # Para o som do jogo
                pyxel.stop(1)  # Para a trilha de apoio
                self.state = "start"
                return
        elif self.state == "victory":
            pyxel.stop(0)  # Para qualquer som de fundo
            if self.victory_screen and self.victory_screen.update():
                # Reinicia a fase e volta ao menu inicial
                self.fase1 = Fase1()
                self.victory_screen = None  # Remove a tela de vitória usada
                self.state = "start"
                return
        elif self.state == "lose":
            pyxel.stop(0)  
            if self.lose_screen and self.lose_screen.update():
                # Reinicia a fase e volta ao menu inicial
                self.fase1 = Fase1()
                self.lose_screen = None  # Remove a tela de derrota usada
                self.state = "start"
                return

    def draw(self):
        if self.state == "start":
            self.start_screen.desenhastart()
        elif self.state == "game":
            self.fase1.draw_fase1()
        elif self.state == "victory":
            if self.victory_screen:
                self.victory_screen.draw()
        elif self.state == "lose":
            if self.lose_screen:
                self.lose_screen.draw()


CandyMazeGame()