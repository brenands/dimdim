import pyautogui
import time
import random
from datetime import datetime
import threading 
import logging
import mss
import numpy as np

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(threadName)s] %(message)s', datefmt='%H:%M:%S')

def pegar_cor(x, y):
    with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": 1, "height": 1}
            img = np.array(sct.grab(monitor))
            return tuple(img[0,0][:3])  # RGB

# Função principal para cada navegador
def rotina_navegador(nome, cor_principal, pixel_principal,
                     cor_extra, pixel_extra, clique_extra,
                     pixel_reset, sequencia_cliques, timeout=300, check_interval=0.5):
    contador = 0
    threading.current_thread().name = nome # Define o nome da thread para o logger

    while True:
        contador += 1
        logging.info(f"Iniciando repetição nº {contador}")

        # Desempacota as coordenadas para uso
        px, py = pixel_principal
        extra_x, extra_y = pixel_extra

        logging.info(f"Esperando pela cor {cor_principal} no pixel {pixel_principal}")
        tempo_inicial = time.time()

        while True:
            cor_atual = pegar_cor(px, py)

            # Se a cor principal aparecer
            if cor_atual == cor_principal:
                delay = random.randint(1, 10)
                logging.info(f"Cor principal detectada! Aguardando {delay} segundos antes de continuar...")
                time.sleep(delay)
                logging.info("Continuando...")
                break

            # Se passar de 5 minutos (300s)
            if time.time() - tempo_inicial > timeout:
                logging.warning(f"Tempo limite de {timeout}s atingido. Clicando no pixel de reset {pixel_reset}...")
                pyautogui.click(*pixel_reset)   # <-- pixel reset agora é único por navegador
                tempo_inicial = time.time()

            # # Se a cor extra aparecer
            # cor_extra_atual = pegar_cor(extra_x, extra_y)
            # if cor_extra_atual == cor_extra:
            #     logging.info("Cor extra detectada! Clicando no canto...")
            #     pyautogui.click(*clique_extra)

            time.sleep(check_interval)

        # --- Executa a sequência de cliques configurada ---
        for (espera, acao, valor) in sequencia_cliques:
            time.sleep(espera)
            if acao == "scroll":
                pyautogui.scroll(valor)
            elif acao == "click":
                pyautogui.click(*valor)

# ============================================================
# CONFIGURAÇÃO DOS DOIS NAVEGADORES
# ============================================================

# Navegador 1
config_navegador1 = {
    "nome": "Navegador 1",
    "cor_principal": (255, 203, 119),
    "pixel_principal": (1023, 669),
    "cor_extra": (24, 51, 31),
    "pixel_extra": (955, 840),
    "clique_extra": (955, 840),
    "pixel_reset": (1633, 99),
    "timeout": 300,  # Tempo em segundos para o reset
    "check_interval": 0.5, # Tempo entre verificações de cor
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

# Navegador 2 (EDITE AQUI COM SEUS PIXELS)
# config_navegador2 = {
#     "nome": "Navegador 2",
#     "cor_principal": (255, 203, 119),      # <-- coloque a cor alvo principal
#     "pixel_principal": (67, 694),     # <-- coordenada do pixel principal
#     "cor_extra": (24, 51, 31),       # <-- cor extra a monitorar
#     "pixel_extra": (955, 840),         # <-- coordenada do pixel extra
#     "clique_extra": (955, 840),       # <-- onde clicar se cor extra aparecer
#     "pixel_reset": (674, 101),      # <-- onde clicar se cor extra aparecer
#     "timeout": 300,
#     "check_interval": 0.5,
#     "sequencia_cliques": [
#         # Substitua com os cliques que quer para esse navegador
#         (5, "scroll", 1500),
#         (5, "click", (188, 947)),
#         (5, "scroll", 1500),
#         (5, "click", (787, 575)),
#         (5, "scroll", 1500),
#         (5, "click", (53, 285)),
#         (5, "scroll", 1500),
#         (0, "click", (97, 62))
#     ]
# }

# ============================================================
# RODAR OS DOIS NAVEGADORES EM PARALELO
# ============================================================
thread1 = threading.Thread(target=rotina_navegador, kwargs=config_navegador1, daemon=True)
# thread2 = threading.Thread(target=rotina_navegador, kwargs=config_navegador2, daemon=True)

thread1.start()
# thread2.start()

thread1.join()
# thread2.join()