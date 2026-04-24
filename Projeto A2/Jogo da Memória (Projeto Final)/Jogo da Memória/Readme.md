# Jogo da Memória com Python

![Jogo](./jogo.png)

## Objetivo
Praticar lógica de programação, estruturas de repetição, listas e manipulação de dados. 

## Arquitetura do Projeto:

==========================================

### 1.0 - Importar bibliotecas
- tkinter: interface gráfica;
- PIL: manipular imagens;
- os: acessar arquivos do sistema;
- random: embaralhar elementos;
- messagebox: mostrar alertas.
__________________________________________

import tkinter as tk
from PIL import Image, ImageTk
import os
import random
from tkinter import messagebox

==========================================

### 2.0 - Configurações de Personalização
- Definir o tamanho das cartas (em pixels);
- Definir a quantidade de colunas (cartas) no tabuleiro;
- Definir o espaçamento entre as cartas (em pixels);
- Definir as cores (fundo, botão, hover e fundo das cartas).
__________________________________________

TAMANHO = 100
COLUNAS = 4
ESPACO = 6  # espaço entre cartas

COR_FUNDO = "#FFE4EC"
COR_BOTAO = "#FFB6C1"
COR_HOVER = "#FFA6B5"
COR_CARTA = "#FFFFFF"

==========================================

### 3.0 - Definir o caminho das imagens
- Criar uma variável que representa o diretório onde o código Python está localizado (BASE_DIR);
- Criar uma variável que combina o diretório do código com a pasta de imagens (PASTA);  
- Criar uma variável (arquivos) que liste todos os arquivos da pasta e filtre apenas aqueles com extensão ".png", organizando-os em ordem;
- Criar uma lista que armazena o caminho completo para cada imagem (imagens_caminho).
__________________________________________

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA = os.path.join(BASE_DIR, "img")

arquivos = sorted([f for f in os.listdir(PASTA) if f.lower().endswith(".png")])
imagens_caminho = [os.path.join(PASTA, f) for f in arquivos]

==========================================

### 4.0 - Criação da Janela (View)
Padrão: objeto.metodo(parametro=valor)
           ^
         janela

- Criar uma janela com o tkinter;
- Definir um título para a janela;
- Configurar a cor de fundo da interface.
__________________________________________

janela = tk.Tk()
janela.title("Jogo da Memória")
janela.configure(bg=COR_FUNDO)

==========================================

### 5.0 - Carregar as imagens

- Criar um dicionário (imagens) para armazenar as imagens carregadas;
- Criar um loop (for) que percorre cada item da lista "imagens_caminho";
- Criar uma variável (img) dentro do loop (for), responsável por abrir cada imagem e redimensioná-la utilizando o método "resize";
- Interligar o dicionário à variável "caminho" (imagens[caminho]), guardando a imagem já convertida para uso no Tkinter;
OBS: O Tkinter não entende que é uma imagem, então é necessário a conversão.
- Criar uma variável que crie uma nova imagem, a que será o verso da carta, ultilizando o mesmo TAMANHO e uma cor RGB.
__________________________________________

### imagens = {}

for caminho in imagens_caminho:
    img = Image.open(caminho).resize((TAMANHO, TAMANHO))
    imagens[caminho] = ImageTk.PhotoImage(img)

verso_img = ImageTk.PhotoImage(Image.new("RGB", (TAMANHO, TAMANHO), "#E0E0E0"))

==========================================

### 6.0 - Estado do Jogo

- Criar uma lista vazia para os botões na tela (botoes = []);
- Criar uma lista vazia para guardar as cartas do jogo, ou seja, as imagens embaralhadas (cartas = []);
- Criar variáveis para armazenar quando a primeira e a segunda carta estiverem selecionadas (primeiro = None e segundo = None);
- Criar uma variável que controla quando o usuário pode clicar nas cartas (bloqueado = False);
OBS: "bloqueado" controla se o jogador pode ou não clicar nas cartas.
Quando bloqueado = True:
o jogo ignora cliques (porque está verificando jogada)
Quando bloqueado = False:
o jogo aceita cliques normalmente.
- Criar uma variável que controla se o jogo foi iniciado (jogo_iniciado = False);
- Criar uma variável que conta, em segundos, o tempo do jogo (tempo = 0).
- Criar uma variável que conta, em segundos, o melhor recorde do usuário (recorde = None).
- Criar uma variável que armazena a quantidade de pares encontrados durante a partida (pares_encontrados = 0);
__________________________________________

botoes = []
cartas = []
primeiro = None
segundo = None
bloqueado = False
jogo_iniciado = False
tempo = 0
recorde = None
pares_encontrados = 0

==========================================

### 7.0 - Labels

- Criar elementos de texto que exibem as seguintes informações:
Quanto tempo se passou desde o início da partida (label_tempo).
O menor tempo já alcançado pelo usuário, exibido como recorde (label_recorde);
- Configurar a aparência dos labels (texto, fonte e cor de fundo);
- Posicionar os labels na interface utilizando o método grid;

__________________________________________

label_tempo = tk.Label(janela, text="Tempo: 0s", font=("Arial", 14), bg=COR_FUNDO)
label_tempo.grid(row=0, column=0, columnspan=COLUNAS, pady=(10, 0))

label_recorde = tk.Label(janela, text="Recorde: --", font=("Arial", 12), bg=COR_FUNDO)
label_recorde.grid(row=1, column=0, columnspan=COLUNAS, pady=(0, 10))

===========================================

### 8.0 - Temporizador

- Criar uma função para exercer a função de temporizador (def atualizar_tempo():);
- Acessar a variável global "tempo" para poder alterá-la;
- Determinar que se o jogo começou (jogo_iniciado = True), a variável "tempo" ganha +1 segundo (tempo +=1);
- Atualizar o texto na "label_tempo";
- Criar um loop de tempo de 1000 milissegundos, usando o método "after" para chamar a função novamente.
__________________________________________

def atualizar_tempo():
    global tempo

    if jogo_iniciado:
        tempo += 1
        label_tempo.config(text=f"Tempo: {tempo}s")
        janela.after(1000, atualizar_tempo)

===========================================

### 9.0 - Clique nas Cartas

- Criar uma função responsável pela interação do usuário com as cartas (def clicar(i));
- Acessar as variáves globais: primeiro, segundo e bloqueado.
- Criar as seguintes condições:
Se o jogo não tiver sido iniciado ou estiver bloqueado, o clique deve ser ignorado;
Se a carta já estiver virada, não é possível clicar novamente;
- Acessar a imagem correspondente à carta clicada e exibí-la no botão
da tela;
- Criar uma condição para identificar qual carta foi clicada e armazenar essa informação (i);
__________________________________________

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

===========================================

### 10.0 - Verificar Pares

- Criar uma função que compara o par de cartas selecionadas pelo jogador (def verificar());
- Acessar as variáveis globais: bloqueado e pares_encontrados;
- Travar o jogo por um momento para fazer a comparação (bloqueado = True);
- Criar uma condição que compara as duas cartas:
Se a primeira e a segunda carta forem iguais: pares_encontrados += 1, a rodada chega ao fim e o usuário joga novamente;
- Criar uma condição que diz:
Se todos os pares na lista (imagens_caminho) forem encontrados, a função "fim_de_jogo()" é chamada, e o jogo acaba. 
Se não, depois de 700ms o programa chama a função "esconder()" utilizando o método after, e as cartas vão virar novamente. 
__________________________________________

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

===========================================

### 11.0 - Funções Complementares

1.0 Função de esconder os botões:
- Ela vira as duas cartas, exibindo seus versos, e depois reseta o turno.

2.0 - Função de Resetar Turno:
- Acessa as variáveis globais: primeiro, segundo e bloqueado;
- Diz que se nenhuma carta for selecionada, o usuário pode clicar novamente. 

3.0 - Função de Fim de Jogo:
- Acessa as variáveis globais: jogo_iniciado e recorde;
- Determina que: jogo_iniciado = False;
- Cria um laço condicional que diz:
Se não houver recorde, ou se o tempo for menor do que o recorde: recorde = tempo, e exibe uma mensagem com popup;
__________________________________________

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

===========================================

### 12.0 - Botões

- Criar botões de controle que são responsáveis por iniciar e reiniciar o jogo. Eles chamam funções específicas como iniciar_jogo() e resetar_jogo(), e também possuem efeitos visuais de hover para melhor experiência do usuário.
- Criar os botões do tabuleiro com laço de repetição, de acordo com a quantidade de imagens disponíveis. Cada botão representa uma carta do jogo e é responsável por exibir o verso ou a imagem da carta quando o jogador clica.

Esses botões armazenam sua própria imagem atual e chamam a função clicar(i), que controla toda a lógica de seleção e verificação de pares.
__________________________________________

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

- TABULEIRO:

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

===========================================

### 13.0 - Iniciar o “modo de funcionamento” da interface:

- Inserir no final do código.
Sem ele: a janela mal aparece, o programa fecha instantaneamente e nada responde (cliques, botões, etc.)
__________________________________________

janela.mainloop()

===========================================
