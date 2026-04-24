import tkinter
import os
import random
import tkinter.messagebox
from PIL import Image, ImageTk

# CONFIGURAÇÕES:

tamanho = 100
colunas = 4
espaco = 6 

cor_fundo = "#FFE4EC"
cor_botao = "#FFB6C1"
cor_hover = "#FFA6B5"
cor_carta = "#FFFFFF"

base_dir = os.path.dirname(os.path.abspath(__file__))
pasta = os.path.join(base_dir, "img")

arquivos = sorted([f for f in os.listdir(pasta) if f.lower().endswith(".png")])
imagens_caminho = [os.path.join(pasta, f) for f in arquivos]

# JANELA:

janela = tkinter.Tk()
janela.title("Jogo da Memória")
janela.configure(bg=cor_fundo)

# IMAGENS:

imagens = {}
for caminho in imagens_caminho:
    img = Image.open(caminho).resize((tamanho, tamanho))
    imagens[caminho] = ImageTk.PhotoImage(img)

verso_img = ImageTk.PhotoImage(Image.new("RGB", (tamanho, tamanho), "#F0F0F0"))

# VARIÁVEIS:

botoes = []
cartas = []
primeiro = None
segundo = None
bloqueado = False
jogo_iniciado = False
tempo = 0
recorde = None
pares_encontrados = 0

# LABELS:

label_tempo = tkinter.Label(janela, text="Tempo: 0s", font=("Arial", 14), bg=cor_fundo)
label_tempo.grid(row=0, column=0, columnspan=colunas, pady=(10, 0))

label_recorde = tkinter.Label(janela, text="Recorde: --", font=("Arial", 12), bg=cor_fundo)
label_recorde.grid(row=1, column=0, columnspan=colunas, pady=(0, 10))

# TIMER:

def atualizar_tempo():
    global tempo
    if jogo_iniciado:
        tempo += 1
        label_tempo.config(text=f"Tempo: {tempo}s")
        janela.after(1150, atualizar_tempo)

# FUNÇÕES:

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

    tkinter.messagebox.showinfo("Parabéns!", f"Você venceu em {tempo} segundos!")

# BOTÕES:

def hover_on(e):
    e.widget["bg"] = cor_hover

def hover_off(e):
    e.widget["bg"] = cor_botao

btn_start = tkinter.Button(
    janela,
    text="Iniciar",
    command=iniciar_jogo,
    bg=cor_botao,
    activebackground=cor_hover,
    relief="flat",
    font=("Arial", 10, "bold")
)

btn_start.grid(row=2, column=0, columnspan=colunas//2, sticky="ew", padx=10, pady=5)
btn_start.bind("<Enter>", hover_on)
btn_start.bind("<Leave>", hover_off)

btn_reset = tkinter.Button(
    janela,
    text="Resetar",
    command=resetar_jogo,
    bg=cor_botao,
    activebackground=cor_hover,
    relief="flat",
    font=("Arial", 10, "bold")
)

btn_reset.grid(row=2, column=colunas//2, columnspan=colunas//2, sticky="ew", padx=10, pady=5)
btn_reset.bind("<Enter>", hover_on)
btn_reset.bind("<Leave>", hover_off)

# TABULEIRO:

for i in range(len(imagens_caminho) * 2):
    img = imagens[imagens_caminho[i % len(imagens_caminho)]]

    btn = tkinter.Button(
        janela,
        image=img,
        width=tamanho,
        height=tamanho,
        command=lambda i=i: clicar(i),
        bd=2,                     # borda
        relief="raised",          # efeito botão
        bg=cor_carta
    )

    btn.image = img
    btn.grid(
        row=(i // colunas) + 3,
        column=i % colunas,
        padx=espaco,
        pady=espaco
    )

    botoes.append(btn)

# INICIAR:

janela.mainloop()