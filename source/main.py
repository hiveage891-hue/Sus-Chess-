import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()
root.title("Xadrez")

tamanhoCasa = 80
lado = tamanhoCasa * 8
assets = "assets/"

canvas = tk.Canvas(root, width=lado, height=lado)
canvas.pack()

tabuleiro = [[None for _ in range(8)] for _ in range(8)]
selecao = None
fotos = {}
movidos = set()


def carregar():
    pecas = [
        "peao-branco",
        "bispo-branco",
        "torre-branco",
        "cavalo-branco",
        "rei-branco",
        "rainha-branco",
        "peao-preto",
        "bispo-preto",
        "torre-preto",
        "cavalo-preto",
        "rei-preto",
        "rainha-preto",
    ]
    for p in pecas:
        img = Image.open(f"{assets}images/{p}.png").resize(
            (tamanhoCasa, tamanhoCasa), Image.Resampling.LANCZOS
        )
        fotos[p] = ImageTk.PhotoImage(img)


def inicializar():
    for i in range(8):
        tabuleiro[1][i] = "peao-preto"
        tabuleiro[6][i] = "peao-branco"
    ordem = ["torre", "cavalo", "bispo", "rainha", "rei", "bispo", "cavalo", "torre"]
    for i, p in enumerate(ordem):
        tabuleiro[0][i] = f"{p}-preto"
        tabuleiro[7][i] = f"{p}-branco"


def desenhar():
    canvas.delete("all")
    for l in range(8):
        for c in range(8):
            x1, y1 = c * tamanhoCasa, l * tamanhoCasa
            x2, y2 = x1 + tamanhoCasa, y1 + tamanhoCasa
            cor = "#eeeed2" if (l + c) % 2 == 0 else "#769656"
            if selecao == (l, c):
                cor = "yellow"
            canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="")
            peca = tabuleiro[l][c]
            if peca:
                canvas.create_image(x1, y1, image=fotos[peca], anchor="nw")


def validar_movimento(l1, c1, l2, c2):
    peca = tabuleiro[l1][c1]
    alvo = tabuleiro[l2][c2]
    dl, dc = l2 - l1, c2 - c1

    if not peca or "branco" not in peca:
        return False
    if alvo and "branco" in alvo:
        return False

    if "peao-branco" in peca:
        if dc == 0 and alvo is None:
            if dl == -1:
                return True
            if dl == -2 and l1 == 6 and tabuleiro[5][c1] is None:
                return True
        if abs(dc) == 1 and dl == -1 and alvo and "preto" in alvo:
            return True
        return False

    if "bispo-branco" in peca or "rainha-branco" in peca or "torre-branco" in peca:
        is_diag = abs(dl) == abs(dc)
        is_rect = dl == 0 or dc == 0

        if (
            ("bispo" in peca and not is_diag)
            or ("torre" in peca and not is_rect)
            or ("rainha" in peca and not (is_diag or is_rect))
        ):
            return False

        passo_l = 0 if dl == 0 else (1 if dl > 0 else -1)
        passo_c = 0 if dc == 0 else (1 if dc > 0 else -1)
        for i in range(1, max(abs(dl), abs(dc))):
            if tabuleiro[l1 + i * passo_l][c1 + i * passo_c] is not None:
                return False
        return True

    if "cavalo-branco" in peca:
        return (abs(dl) == 2 and abs(dc) == 1) or (abs(dl) == 1 and abs(dc) == 2)

    if "rei-branco" in peca:
        if abs(dl) <= 1 and abs(dc) <= 1:
            return True
        if dl == 0 and abs(dc) == 2 and l1 == 7 and (l1, c1) not in movidos:
            col_t = 7 if dc == 2 else 0
            if (7, col_t) not in movidos and tabuleiro[7][col_t] == "torre-branco":
                step = 1 if dc > 0 else -1
                if all(
                    tabuleiro[7][c1 + i * step] is None
                    for i in range(1, abs(col_t - c1))
                ):
                    return True
        return False
    return False


def clicar(event):
    global selecao
    c, l = event.x // tamanhoCasa, event.y // tamanhoCasa
    if selecao:
        l_ant, c_ant = selecao
        if validar_movimento(l_ant, c_ant, l, c):
            if "rei-branco" in tabuleiro[l_ant][c_ant] and abs(c - c_ant) == 2:
                c_t_ant = 7 if c > c_ant else 0
                c_t_nova = 5 if c > c_ant else 3
                tabuleiro[7][c_t_nova] = tabuleiro[7][c_t_ant]
                tabuleiro[7][c_t_ant] = None

            tabuleiro[l][c] = tabuleiro[l_ant][c_ant]
            tabuleiro[l_ant][c_ant] = None
            movidos.add((l_ant, c_ant))
            movidos.add((l, c))
        selecao = None
    else:
        if tabuleiro[l][c] and "branco" in tabuleiro[l][c]:
            selecao = (l, c)
    desenhar()


carregar()
inicializar()
desenhar()
canvas.bind("<Button-1>", clicar)
root.mainloop()
