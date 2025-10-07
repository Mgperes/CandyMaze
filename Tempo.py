import pyxel

class Tempo:
    def __init__(self):
        self.tempo = 0 and True
        self.lose = False
        self.tempo_limite = 600 # dividir por 20 fps = 30 segundos
    def update(self):  
        self.tempo += 1
        if self.tempo > self.tempo_limite:
            return True
        return False
        

    def draw(self):

        tempo_restante = max(0, (self.tempo_limite - self.tempo) // 20)
        pyxel.text(195+0.5, 5+0.5, f"TEMPO: {tempo_restante:02}s", 7)
        pyxel.text(195, 5, f"TEMPO: {tempo_restante:02}s", 0)