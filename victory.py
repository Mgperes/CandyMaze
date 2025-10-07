import pyxel, math
from Balas import Balas
from jujuba import Personagem



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
        """Calcula o score máximo possível baseado nas balas disponíveis, acredito que seja 1000"""
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
        # Fundo 
        for y in range(220):
            if y < 73:
                color = 12 # Azul claro
                pyxel.blt(0, 0, 2, 0, 20, 250, y) # Desenha o fundo que desenhamos
            elif y < 146:
                color = 14  # Rosa
                pyxel.line(0, y, 250, y, color)
            elif y < 206:
                color = pyxel.COLOR_DARK_BLUE
                pyxel.line(0, y, 250, y, color)
            else:
                color = 10  # Amarelo
                pyxel.line(0, y, 250, y, color)
        
        
        """-----------------------Animação de lagos-----------------
        
        Explicação:
        Cada lago tem sua própria velocidade e ciclo de animação, os lagos 1,2 e 3 desenham 10 sprites cada um, os lagos 4,5 e 6 desenham 9 sprites cada um, e os lagos 7,8 e 9 desenham 8 sprites cada um.
        
        hasattr(object, name) -> bool
        verifica se o objeto possui o atributo 'name', retornando True ou False.

        """

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


    #--------------------------------------------------------------------------------------------------------------
        # Animação de chão se formando (POR CIMA DOS LAGOS)
        x_chaoinicial1 = 115
        y_chaoinicial1 = 143
        W_chaolargura1 = 21
        x_chaoinicial2 = x_chaoinicial1
        y_chaoinicial2 = y_chaoinicial1
        W_chaolargura2 = 21

        
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
#------------------------------------------------------------------------------------------------------------
        
        # Título "Sweet Victory"
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
        
#------------------------------------------------------------------------------------------------------------
        
        # Coração  
        heart_x = 120
        heart_y = 90
        pyxel.blt(heart_x, heart_y, 1, 139, 9, 10, 7, 7)
        
        # Porta aberta
        door_x = 115
        door_y = 110
        pyxel.blt(door_x, door_y, 1, 170, 0, 21, 31, 7)
        

        
        
# -------------------personagem comemorando na posição fixa----------------------------------------
        
        #brilhos ao redor do personagem parado ou em movimento
        if not self.animacao_ativa:
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
            
            # Alterna entre pose de comemoração e pose padrão do personagem

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
        
            
        
        
#-------------- Instrução para jogar novamente (só mostra se animação não iniciou)---------------------
        if not self.animacao_ativa:
            instruction_text = "Press ENTER to play again!"
            text_x = 72
            text_y = 189
            
            # Efeito de piscar
            if self.animation_timer % 100 < 80:  # Visível na maior parte do tempo
                pyxel.text(text_x + 1, text_y + 1, instruction_text, 0)  # Sombra
                pyxel.text(text_x, text_y, instruction_text, 7)  # Texto branco
#############################################################################################
        
        # Moldura nas bordas da tela (só se animação não iniciou)
        if not self.animacao_ativa:
            pyxel.line(0, 5, 250, 5, 15)  
            pyxel.line(0, 215, 250, 215, 15)
            pyxel.rect(237, 10, 3, 3, 15)
            pyxel.rect(10, 10, 3, 3, 15)

# -----------------------Painel de Score----------------------------------------------
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
            
            # Score atual
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
                    pyxel.rectb(panel_x - 1, panel_y - 1, panel_w + 2, panel_h + 2, 10)  # Borda 

            # Efeito de brilho se score completo
            if self.percentual == 100:
                blink_frame = self.animation_timer % 60
                if blink_frame < 30:
                    pyxel.rectb(panel_x - 1, panel_y - 1, panel_w + 2, panel_h + 2, 10)  # Borda 

        pyxel.mouse(False)