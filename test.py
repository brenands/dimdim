import pyautogui
import time
import random

contador = 0

# Função para pegar cor de um pixel (com screenshot, funciona até com tela desligada)
def pegar_cor(x, y):
    img = pyautogui.screenshot(region=(x, y, 1, 1))
    return img.getpixel((0, 0))

while True: 
    contador += 1 
    print(f"Iniciando repetição nº {contador}")
    alvo = (255, 203, 119)  # cor principal
    corx, cory = 1341, 455  # pixel principal

    # NOVO: alvo secundário
    alvo_extra = (24, 51, 31)   # <-- coloque aqui a cor que quer monitorar
    extra_x, extra_y = 955, 840     # <-- pixel para monitorar a cor
    clique_extra = (955, 840)     # <-- coordenada onde clicar se a cor aparecer

    print("Esperando pela cor", alvo, "no pixel", (corx, cory))
    tempo_inicial = time.time()
    
    while True:
        cor = pegar_cor(corx, cory)
        cor_extra = pegar_cor(extra_x, extra_y)  # checa também a cor extra

        # Se a cor principal aparecer
        if cor == alvo:
            delay = random.randint(10, 60)
            print(f"Aguardando {delay} segundos antes de continuar...")
            time.sleep(delay)
            print("Continuando...") 
            break

        # Se passar de 5 minutos (300s)
        if time.time() - tempo_inicial > 300:
            print("Tempo limite de 5 minutos atingido. Clicando no pixel de verificação e reiniciando espera...")
            pyautogui.click(95, 59)
            tempo_inicial = time.time()

        # Se a cor extra aparecer
        if cor_extra == alvo_extra:
            print("Cor extra detectada! Clicando no canto...")
            pyautogui.click(*clique_extra)

        time.sleep(0.5)

    # --- Sequência original ---
    time.sleep(5)
    pyautogui.scroll(1500)
    time.sleep(5)
    x, y = 1503, 826
    pyautogui.click(x, y)

    time.sleep(5)
    pyautogui.scroll(1500)
    time.sleep(5)
    x2, y2 = 1523, 639
    pyautogui.click(x2, y2)

    time.sleep(5)
    pyautogui.scroll(1500)
    time.sleep(5)
    x3, y3 = 269, 346
    pyautogui.click(x3, y3)
    time.sleep(5)
    pyautogui.scroll(1500)
    pyautogui.click(95, 59)
