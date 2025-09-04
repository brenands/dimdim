import pyautogui
import time
import random
from datetime import datetime
import threading

# Função para pegar cor de um pixel (com screenshot, funciona até com tela desligada)
def pegar_cor(x, y):
    # captura só 1 pixel da tela direto do buffer de vídeo
    return pyautogui.screenshot(region=(x, y, 1, 1)).getpixel((0, 0))

# Função principal para cada navegador
def rotina_navegador(nome, cor_principal, pixel_principal,
                     cor_extra, cor_extra2, pixel_extra2, clique_extra2, pixel_extra, clique_extra,
                     pixel_reset, sequencia_cliques):
    contador = 0
    while True:
        contador += 1
        hora_atual = datetime.now().strftime("[%H:%M:%S]")
        print(f"{hora_atual} [{nome}] Iniciando repetição nº {contador}")

        alvo = cor_principal
        corx, cory = pixel_principal

        alvo_extra = cor_extra
        extra_x, extra_y = pixel_extra

        alvo_extra2 = cor_extra2
        extra_x2, extra_y2 = pixel_extra2

        hora_atual = datetime.now().strftime("[%H:%M:%S]")
        print(f"{hora_atual} [{nome}] Esperando pela cor {alvo} no pixel {pixel_principal}")
        tempo_inicial = time.time()

        while True:
            cor = pegar_cor(corx, cory)
            cor_extra = pegar_cor(extra_x, extra_y)
            cor_extra2 = pegar_cor(extra_x2, extra_y2)

            # Se a cor principal aparecer
            if cor == alvo:
                delay = random.randint(1, 10)
                hora_atual = datetime.now().strftime("[%H:%M:%S]")
                print(f"{hora_atual} [{nome}] Aguardando {delay} segundos antes de continuar...")
                time.sleep(delay)
                print(f"{hora_atual} [{nome}] Continuando...")
                break

            # Se passar de 5 minutos (300s)
            if time.time() - tempo_inicial > 300:
                hora_atual = datetime.now().strftime("[%H:%M:%S]")
                print(f"{hora_atual} [{nome}] Tempo limite de 5 minutos atingido. "
                      f"Clicando no pixel de reset {pixel_reset} e reiniciando espera...")
                pyautogui.click(*pixel_reset)   # <-- pixel reset agora é único por navegador
                tempo_inicial = time.time()

            # Se a cor extra aparecer
            if cor_extra == alvo_extra:
                hora_atual = datetime.now().strftime("[%H:%M:%S]")
                print(f"{hora_atual} [{nome}] Cor extra detectada! Clicando no canto...")
                pyautogui.click(*clique_extra)

            # Se a cor extra2 aparecer
            if cor_extra2 == alvo_extra2:
                hora_atual = datetime.now().strftime("[%H:%M:%S]")
                print(f"{hora_atual} [{nome}] Cor extra detectada! Clicando no canto...")
                pyautogui.click(*clique_extra2)

            time.sleep(0.5)

        # --- Executa a sequência de cliques configurada ---
        for (espera, acao, valor) in sequencia_cliques:
            time.sleep(espera)
            if acao == "scroll":
                pyautogui.scroll(valor)
            elif acao == "click":
                pyautogui.click(*valor)


# Navegador 1
config_navegador1 = {
    "nome": "Navegador 1",
    "cor_principal": (255, 203, 119),
    "pixel_principal": (1023, 669),
    "cor_extra": (24, 51, 31),
    "pixel_extra": (1431, 748),
    "clique_extra": (1431, 748),
    "cor_extra2": (24, 51, 31),
    "pixel_extra2": (468, 748),
    "clique_extra2": (468, 748),
    "pixel_reset": (1633, 99),
    "sequencia_cliques": [
        (5, "scroll", 0),
        (5, "click", (1107, 947)),
        (5, "scroll", 1500),
        (5, "click", (1777, 573)),
        (5, "scroll", 1500),
        (5, "click", (1006, 295)),
        (5, "scroll", 1500),
        (5, "click", (1054, 62)),
        (5, "scroll", 0),
        (5, "click", (188, 947)),
        (5, "scroll", 1500),
        (5, "click", (787, 575)),
        (5, "scroll", 1500),
        (5, "click", (53, 285)),
        (5, "scroll", 1500),
        (5, "click", (97, 62))
    ]
}

thread1 = threading.Thread(target=rotina_navegador, kwargs=config_navegador1)

thread1.start()

thread1.join()