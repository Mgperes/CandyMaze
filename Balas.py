import pyxel


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