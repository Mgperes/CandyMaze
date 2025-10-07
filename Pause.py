import pyxel

class Pause:
    def __init__ (self):
        self.tempo_pause = 0
        self.pausado = False

    def update_pause(self):
        if pyxel.btnp(pyxel.KEY_F):
            print(f"Tecla F pressionada! tempo_pause: {self.tempo_pause}")
            self.tempo_pause += 1
            if self.tempo_pause % 2 == 1:
                self.pausado = True
                pyxel.stop(0)
                pyxel.stop(1)
                pyxel.stop(2)
                pyxel.stop(3)
            else:
                self.pausado = False
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