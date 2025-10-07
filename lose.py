import pyxel, math, random


class LoseScreen:
    def __init__(self, score_atual=0, lose_reason=None):
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
        # motivo da derrota: 'formiga', 'tempo', 'afogado' ou None
        self.lose_reason = lose_reason
    
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
               
        
        title_x = 80
        title_y = 40
        x_mem_title = 132
        y_mem_title1 = 48
        y_mem_title2 = 57

        pyxel.blt(title_x + 2, title_y + 2, 1, x_mem_title, y_mem_title1, 90, 10, 7)
        pyxel.blt(title_x , title_y, 1, x_mem_title, y_mem_title2, 90, 10, 7)

        # Mensagem específica de perda, exibida abaixo do título
        message = None
        if self.lose_reason == 'formiga':
            message = "Oh nao! A formiga esgotou suas vidas."
        elif self.lose_reason == 'tempo':
            message = "Seu tempo acabou! Tente ser mais veloz."
        elif self.lose_reason == 'afogado':
            message = "Oh nao! Voce morreu afogado no lago."

        if message:
            # centraliza mensagem em relação ao título
            msg_x = 53
            msg_y = 58
            # sombra
            pyxel.text(msg_x + 1, msg_y + 1, message, 0)
            pyxel.text(msg_x, msg_y, message, 7)

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