import pyxel

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
    
