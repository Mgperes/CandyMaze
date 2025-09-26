# 🎵 Guia de Áudio para Pyxel - CandyMaze

## 📋 **Sistema de Áudio Implementado**

### **🔊 Sons Configurados (VERSÃO SUAVE):**


2. **Som de Dano** (Canal 1) - **SUAVE**
   - Notas: F2-E2-D2-C2 (descendente suave)
   - Volumes: 3-2-2-1 (moderado para baixo)
   - Efeito: Melancólico mas não agressivo
   - Ativação: Quando a formiga ataca o personagem

3. **Som de Morte** (Canal 2) - **MELANCÓLICO**
   - Notas: G3-F3-E3-D3-C3 (oitava mais alta)
   - Volumes: 4-3-3-2-1 (decrescente suave)
   - Efeito: Triste mas não traumático
   - Ativação: Morte por afogamento ou perda de todas vidas

4. **Som de Vitória** (Canal 3) - **CELEBRAÇÃO DOCE**
   - Notas: C3-E3-G3-C4-G3-E3-C3 (melodia circular)
   - Volumes: 3-4-5-4-5-4-3 (curva suave)
   - Efeito: Alegria contida e harmoniosa
   - Ativação: Quando ganha o jogo

5. **Som de Menu** (Canal 4) - **CLICK SUTIL**
   - Notas: E3 (nota única)
   - Volume: 2 (muito baixo)
   - Efeito: Toque delicado
   - Ativação: Cliques em botões e menus

6. **Som Ambiente do Jogo** (Canal 5) - **TRANQUILIDADE**
   - Notas: C3-G3-A3-F3-E3-G3-C3-E3 (melodia relaxante)
   - Volumes: 2-2-2-2-2-2-2-2 (constante baixo)
   - Efeito: Serenidade e paz
   - Ativação: Durante o gameplay (loop)

7. **Som Ambiente do Menu** (Canal 6) - **RELAXAMENTO PROFUNDO**
   - Notas: C2-E2-G2-F2-E2-D2-C2-G2 (melodia grave e tranquila)
   - Volumes: 1-2-2-1-1-2-2-1 (muito suave)
   - Tom: Onda quadrada suave (S) para maior profundidade
   - Efeito: Relaxamento profundo e meditativo
   - Ativação: Na tela inicial (loop)

8. **Som de Água** (Canal 7) - **AVISO GENTIL**
   - Notas: G3-F3-E3 (descendente curto)
   - Volumes: 3-2-1 (fade suave)
   - Efeito: Alerta suave, não assustador
   - Ativação: Primeiro toque na água

9. **Som de Hover** (Canal 8) - **FEEDBACK MÍNIMO**
   - Notas: C4 (nota única)
   - Volume: 1 (quase inaudível)
   - Efeito: Feedback sutil de interface
   - Ativação: Mouse sobre botões do menu

---

## 🎼 **Como Funciona o Sistema de Áudio do Pyxel**

### **Estrutura Básica:**
```python
pyxel.sounds[canal].set(
    notes="C3E3G3",      # Notas musicais
    tones="TTT",         # Tipos de som
    volumes="432",       # Volume (0-7)
    effects="NNN",       # Efeitos especiais
    speed=20             # Velocidade de reprodução
)
```

### **📝 Parâmetros Explicados:**

#### **1. Notes (Notas)**
- **Formato**: `[Nota][Oitava]`
- **Notas**: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
- **Oitavas**: 0-4 (C4 é Dó central)
- **Pausas**: R (rest/pausa)
- **Exemplo**: `"C3E3G3C4"` = Dó-Mi-Sol-Dó (acorde)

#### **2. Tones (Tons)**
- **T** = Triangle (triangular - suave e musical)
- **S** = Square (quadrada - retro/8-bit)
- **P** = Pulse (pulso - variação da quadrada)
- **N** = Noise (ruído - para efeitos percussivos)

#### **3. Volumes**
- **Escala**: 0-7 (0 = silêncio, 7 = máximo)
- **Por nota**: Cada caractere representa o volume de uma nota
- **Exemplo**: `"7654321"` = Volume decrescente

#### **4. Effects (Efeitos)**
- **N** = None (sem efeito)
- **S** = Slide (deslizamento de frequência)
- **V** = Vibrato (oscilação)
- **F** = Fadeout (desvanecimento)

#### **5. Speed (Velocidade)**
- **Range**: 1-99
- **Maior valor** = mais rápido
- **Menor valor** = mais lento

---

## 🎮 **Como Adicionar Novos Sons**

### **1. Definir o Som:**
```python
# Som personalizado (canal 6)
pyxel.sounds[6].set(
    notes="C3D3E3F3G3",  # Escala ascendente
    tones="TTTTT",       # Tom triangular
    volumes="12345",     # Volume crescente
    effects="NNNNN",     # Sem efeitos
    speed=15             # Velocidade média
)
```

### **2. Tocar o Som:**
```python
# Tocar som uma vez
pyxel.play(canal, som_id)

# Tocar em loop
pyxel.play(canal, som_id, loop=True)

# Exemplo:
pyxel.play(0, 6)  # Toca som 6 no canal 0
```

### **3. Verificar se Som Está Tocando:**
```python
if pyxel.play_pos(canal):
    print("Som está tocando")
else:
    print("Canal livre")
```

---

## 🎵 **Dicas para Criar Bons Sons**

### **📈 Sons de Sucesso:**
- Use tons **T** (triangular)
- Notas **ascendentes**
- Volumes **crescentes**
- Velocidade **média-alta**

### **💥 Sons de Impacto:**
- Use tons **N** (noise)
- Notas **graves** (C1, C2)
- Volumes **altos** (6-7)
- Efeitos **S** (slide)

### **🎶 Sons Musicais:**
- Use acordes (**C3E3G3** = Dó Maior)
- Combine tons **T** e **S**
- Volumes **moderados** (3-5)
- Velocidade **baixa-média**

### **🔄 Sons de Loop:**
- Mantenha **curtos** (4-8 notas)
- Volume **baixo** (1-3)
- Sem mudanças **bruscas**
- Use **S** ou **P** para retro

---

## 🎼 **Exemplos Práticos**

### **Som de Moeda Coletada:**
```python
pyxel.sounds[7].set(
    notes="C4E4G4C5",
    tones="TTTT",
    volumes="4567",
    effects="NNNN",
    speed=25
)
```

### **Som de Explosão:**
```python
pyxel.sounds[8].set(
    notes="G2F2E2D2C2",
    tones="NNNNN",
    volumes="76543",
    effects="SSSSS",
    speed=8
)
```

### **Som de Power-Up:**
```python
pyxel.sounds[9].set(
    notes="C3E3G3C4E4G4C5E5",
    tones="TTTTTTTT",
    volumes="23456765",
    effects="NNNNNNNN",
    speed=20
)
```

---

## 🔧 **Troubleshooting**

### **❌ Erros Comuns:**

1. **"Invalid sound note"**
   - Verifique se as oitavas estão entre 0-4
   - Use apenas notas válidas (C, C#, D, etc.)

2. **"String lengths must match"**
   - `notes`, `tones`, `volumes`, `effects` devem ter mesmo tamanho
   - Exemplo: 4 notas = 4 tons = 4 volumes = 4 efeitos

3. **Som não toca:**
   - Verifique se o canal não está ocupado
   - Use `pyxel.play_pos(canal)` para verificar

### **✅ Boas Práticas:**

- **Máximo 16 sons** simultâneos (pyxel.sounds[0-15])
- **4 canais** de reprodução (0-3)
- **Teste sempre** após mudanças
- **Volume baixo** para sons de fundo
- **Mantenha consistência** no estilo musical

---

## 🎮 **Sistema Atual do CandyMaze**

### **Mapeamento de Sons:**
- **Canal 0**: Som ambiente (loop)
- **Canal 1**: Sons de pulo
- **Canal 2**: Sons de dano/ataque
- **Canal 3**: Sons de morte/vitória

### **Canais Livres:**
- **Canais disponíveis**: Nenhum durante gameplay
- **Para novos sons**: Considere pausar ambiente ou usar canais alternativos

---

---

## 🍬 **Design Sonoro "Doce" - Filosofia de Áudio**

### **🎵 Características do Sistema Atual:**

#### **🌙 Suavidade Total:**
- **Volumes baixos**: Máximo de 5, maioria entre 1-3
- **Tons triangulares**: Predominância de ondas suaves (T)
- **Sem sons agressivos**: Eliminados ruídos e efeitos ásperos
- **Transições suaves**: Fade-in/fade-out naturais

#### **🎶 Melodias Relaxantes:**
- **Tela inicial**: Melodia grave e profundamente relaxante em loop
- **Durante o jogo**: Ambiente tranquilo e meditativo
- **Pulo**: SILENCIOSO (removido para evitar repetição)
- **Interações**: Feedback mínimo mas presente

#### **🧘 Experiência Zen:**
- **Não-intrusivo**: Sons complementam, não competem
- **Atmosfera calma**: Induz estado de relaxamento
- **Jogabilidade doce**: Áudio reforça tema "Candy"
- **Sem sobressaltos**: Mesmo eventos negativos são suaves

#### **💫 Benefícios da Abordagem Suave:**
- **Menos estresse**: Jogador permanece relaxado
- **Maior imersão**: Foco no gameplay, não no áudio
- **Experiência agradável**: Associação positiva com o jogo
- **Rejogabilidade**: Som não cansa nem irrita

---

## 🎮 **Mapeamento Completo de Canais**

### **Canal 0**: Ambiente Principal
- **Menu**: Som grave e relaxante de fundo
- **Jogo**: Melodia tranquila contínua

### **Canal 1**: Ações do Personagem  
- **Pulo**: REMOVIDO (silencioso)
- **Hover**: Feedback sutil de interface

### **Canal 2**: Eventos de Dano
- **Ataque formiga**: Som melancólico suave
- **Sem agressividade**: Mantém tom doce

### **Canal 3**: Eventos Especiais
- **Morte**: Melancolia suave
- **Água**: Aviso gentil
- **Vitória**: Celebração contida

---

**🍭 Agora seu CandyMaze tem uma experiência sonora verdadeiramente DOCE! 🎮✨**