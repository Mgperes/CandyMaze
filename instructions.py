import pyxel, random, math


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
            "- Use as teclas A e D ou setas para mover;",
            "- Pressione ESPACO para pular;",
            "- Pressione F para pausar",
            "- Colete balas para ganhar pontos;",
            "- Nao caia na agua dos lagos;",
            "- A formiga faz perder vidas e score;",
            "- Chegue na porta, o tempo e seu inimigo!!",
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
        start_y = self.box_y + 8
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
        end_x = self.box_x + self.box_width 
        
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
        end_y = self.box_y + self.box_height 
        
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