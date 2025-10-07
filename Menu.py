import pyxel

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