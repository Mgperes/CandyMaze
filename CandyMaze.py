import pyxel
from Menu import Start
from fase_1 import Fase1
from victory import VictoryScreen
from lose import LoseScreen

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
        pyxel.images[0].load(0, 0, "assets/background.png")
        pyxel.images[1].load(0, 0, "assets/itens.png")
        pyxel.images[2].load(0, 0, "assets/fundofase1.png")

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
                # Cria nova tela de derrota a cada derrota com o score atual e motivo
                self.lose_screen = LoseScreen(self.fase1.balas.score, self.fase1.lose_reason)
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