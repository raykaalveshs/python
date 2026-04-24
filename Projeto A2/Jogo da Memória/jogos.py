import tkinter as tk
from PIL import Image, ImageTk
import os
import random
from tkinter import messagebox

# ===== CONFIG =====
TAMANHO = 100
COLUNAS = 4
ESPACO = 6  # espaço entre cartas

COR_FUNDO = "#FFE4EC"
COR_BOTAO = "#FFB6C1"
COR_HOVER = "#FFA6B5"
COR_CARTA = "#FFFFFF"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA = os.path.join(BASE_DIR, "img")

arquivos = sorted([f for f in os.listdir(PASTA) if f.lower().endswith(".png")])
imagens_caminho = [os.path.join(PASTA, f) for f in arquivos]

# ===== JANELA =====
janela = tk.Tk()
janela.title("Jogo da Memória")
janela.configure(bg=COR_FUNDO)

# ===== IMAGENS =====
imagens = {}
for caminho in imagens_caminho:
    img = Image.open(caminho).resize((TAMANHO, TAMANHO))
    imagens[caminho] = ImageTk.PhotoImage(img)

verso_img = ImageTk.PhotoImage(Image.new("RGB", (TAMANHO, TAMANHO), "#E0E0E0"))

# ===== VARIÁVEIS =====
botoes = []
cartas = []
primeiro = None
segundo = None
bloqueado = False
jogo_iniciado = False
tempo = 0
recorde = None
pares_encontrados = 0

# ===== LABELS =====
label_tempo = tk.Label(janela, text="Tempo: 0s", font=("Arial", 14), bg=COR_FUNDO)
label_tempo.grid(row=0, column=0, columnspan=COLUNAS, pady=(10, 0))

label_recorde = tk.Label(janela, text="Recorde: --", font=("Arial", 12), bg=COR_FUNDO)
label_recorde.grid(row=1, column=0, columnspan=COLUNAS, pady=(0, 10))

# ===== TIMER =====
def atualizar_tempo():
    global tempo
    if jogo_iniciado:
        tempo += 1
        label_tempo.config(text=f"Tempo: {tempo}s")
        janela.after(1000, atualizar_tempo)

# ===== FUNÇÕES =====
def iniciar_jogo():
    global jogo_iniciado, tempo, cartas, pares_encontrados

    cartas = imagens_caminho * 2
    random.shuffle(cartas)

    pares_encontrados = 0
    tempo = 0
    jogo_iniciado = True

    for i in range(len(botoes)):
        botoes[i].config(image=verso_img)
        botoes[i].image = verso_img

    atualizar_tempo()

def resetar_jogo():
    global jogo_iniciado, tempo, primeiro, segundo, bloqueado, pares_encontrados

    jogo_iniciado = False
    tempo = 0
    primeiro = None
    segundo = None
    bloqueado = False
    pares_encontrados = 0

    label_tempo.config(text="Tempo: 0s")

    for i in range(len(botoes)):
        img = imagens[imagens_caminho[i % len(imagens_caminho)]]
        botoes[i].config(image=img)
        botoes[i].image = img

def clicar(i):
    global primeiro, segundo, bloqueado

    if not jogo_iniciado or bloqueado:
        return

    if botoes[i].image != verso_img:
        return

    botoes[i].config(image=imagens[cartas[i]])
    botoes[i].image = imagens[cartas[i]]

    if primeiro is None:
        primeiro = i
    elif segundo is None:
        segundo = i
        verificar()

def verificar():
    global bloqueado, pares_encontrados

    bloqueado = True

    if cartas[primeiro] == cartas[segundo]:
        pares_encontrados += 1
        resetar_turno()

        if pares_encontrados == len(imagens_caminho):
            fim_de_jogo()
    else:
        janela.after(700, esconder)

def esconder():
    botoes[primeiro].config(image=verso_img)
    botoes[primeiro].image = verso_img

    botoes[segundo].config(image=verso_img)
    botoes[segundo].image = verso_img

    resetar_turno()

def resetar_turno():
    global primeiro, segundo, bloqueado
    primeiro = None
    segundo = None
    bloqueado = False

def fim_de_jogo():
    global jogo_iniciado, recorde

    jogo_iniciado = False

    if recorde is None or tempo < recorde:
        recorde = tempo
        label_recorde.config(text=f"Recorde: {recorde}s")

    messagebox.showinfo("Parabéns!", f"Você venceu em {tempo} segundos!")

# ===== BOTÕES (ESTILO) =====
def hover_on(e):
    e.widget["bg"] = COR_HOVER

def hover_off(e):
    e.widget["bg"] = COR_BOTAO

btn_start = tk.Button(
    janela,
    text="Iniciar",
    command=iniciar_jogo,
    bg=COR_BOTAO,
    activebackground=COR_HOVER,
    relief="flat",
    font=("Arial", 10, "bold")
)
btn_start.grid(row=2, column=0, columnspan=COLUNAS//2, sticky="ew", padx=10, pady=5)
btn_start.bind("<Enter>", hover_on)
btn_start.bind("<Leave>", hover_off)

btn_reset = tk.Button(
    janela,
    text="Resetar",
    command=resetar_jogo,
    bg=COR_BOTAO,
    activebackground=COR_HOVER,
    relief="flat",
    font=("Arial", 10, "bold")
)
btn_reset.grid(row=2, column=COLUNAS//2, columnspan=COLUNAS//2, sticky="ew", padx=10, pady=5)
btn_reset.bind("<Enter>", hover_on)
btn_reset.bind("<Leave>", hover_off)

# ===== TABULEIRO =====
for i in range(len(imagens_caminho) * 2):
    img = imagens[imagens_caminho[i % len(imagens_caminho)]]

    btn = tk.Button(
        janela,
        image=img,
        width=TAMANHO,
        height=TAMANHO,
        command=lambda i=i: clicar(i),
        bd=2,                     # borda
        relief="raised",          # efeito botão
        bg=COR_CARTA
    )

    btn.image = img
    btn.grid(
        row=(i // COLUNAS) + 3,
        column=i % COLUNAS,
        padx=ESPACO,
        pady=ESPACO
    )

    botoes.append(btn)

# ===== INICIAR =====
janela.mainloop()