import pyautogui
import time
import random
from datetime import datetime
import threading
import mss
import sys
import keyboard  # pip install keyboard

# --- Controle global para parar threads ---
parar = False

# Captura de pixel usando MSS (funciona com tela desligada)
def pegar_cor(x, y):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": 1, "height": 1}
        img = sct.grab(monitor)
        return img.pixel(0, 0)

# Função principal para cada navegador
def rotina_navegador(nome, cor_principal, pixel_principal,
                     cor_extra, cor_extra2, pixel_extra2, clique_extra2, pixel_extra, clique_extra,
                     pixel_reset, sequencia_cliques):
    global parar
    contador = 0
    while not parar:
        contador += 1
        hora_atual = datetime.now().strftime("[%H:%M:%S]")
        print(f"{hora_atual} [{nome}] Iniciando repetição nº {contador}")

        alvo = cor_principal
        corx, cory = pixel_principal

        alvo_extra = cor_extra
        extra_x, extra_y = pixel_extra

        alvo_extra2 = cor_extra2
        extra_x2, extra_y2 = pixel_extra2

        print(f"{hora_atual} [{nome}] Esperando pela cor {alvo} no pixel {pixel_principal}")
        tempo_inicial = time.time()

        while not parar:
            hora_atual = datetime.now().strftime("[%H:%M:%S]")
            cor = pegar_cor(corx, cory)
            cor_ex = pegar_cor(extra_x, extra_y)
            cor_ex2 = pegar_cor(extra_x2, extra_y2)

            if cor == alvo:
                delay = random.randint(1, 10)
                print(f"{hora_atual} [{nome}] Aguardando {delay} segundos antes de continuar...")
                time.sleep(delay)
                print(f"{hora_atual} [{nome}] Continuando...")
                break

            if time.time() - tempo_inicial > 300:
                print(f"{hora_atual} [{nome}] Tempo limite de 5 minutos atingido. "
                      f"Clicando no pixel de reset {pixel_reset} e reiniciando espera...")
                pyautogui.click(*pixel_reset)
                tempo_inicial = time.time()

            if cor_ex == alvo_extra:
                print(f"{hora_atual} [{nome}] Cor extra detectada! Clicando...")
                pyautogui.click(*clique_extra)

            if cor_ex2 == alvo_extra2:
                print(f"{hora_atual} [{nome}] Cor extra2 detectada! Clicando...")
                pyautogui.click(*clique_extra2)

            time.sleep(0.5)

        # --- Executa a sequência de cliques configurada ---
        for (espera, acao, valor) in sequencia_cliques:
            if parar:
                break
            time.sleep(espera)
            if acao == "scroll":
                pyautogui.scroll(valor)
            elif acao == "click":
                pyautogui.click(*valor)


# Configuração do navegador
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
        (3, "click", (1107, 947)),
        (2, "scroll", 0),
        (2, "scroll", 1500),
        (3, "click", (1777, 573)),
        (2, "scroll", 1500),
        (3, "click", (1006, 295)),
        (2, "scroll", 1500),
        (3, "click", (1054, 62)),
        (2, "scroll", 0),
        (3, "click", (188, 947)),
        (2, "scroll", 1500),
        (3, "click", (787, 575)),
        (2, "scroll", 1500),
        (3, "click", (53, 285)),
        (2, "scroll", 1500),
        (3, "click", (97, 62))
    ]
}


# Monitorar tecla ESC em paralelo (3 vezes em até 5s para sair)
def monitorar_tecla():
    global parar
    contador_esc = 0
    primeiro_tempo = None
    limite_tempo = 5  # segundos para apertar 3 vezes

    while True:
        if keyboard.is_pressed("esc"):
            agora = time.time()

            if contador_esc == 0:
                # Primeiro ESC
                primeiro_tempo = agora
                contador_esc = 1
            else:
                # Se passar do limite, reinicia contagem
                if agora - primeiro_tempo > limite_tempo:
                    contador_esc = 1
                    primeiro_tempo = agora
                else:
                    contador_esc += 1

            print(f"[!] ESC pressionado ({contador_esc}/3)")

            if contador_esc >= 3:
                print("\n[!] Tecla ESC pressionada 3 vezes em tempo válido. Encerrando execução...")
                parar = True
                sys.exit(0)

            # Evita contar várias vezes a mesma pressionada
            while keyboard.is_pressed("esc"):
                time.sleep(0.2)

        time.sleep(0.2)


# Thread do navegador
thread1 = threading.Thread(target=rotina_navegador, kwargs=config_navegador1)
thread1.start()

# Thread para monitorar ESC
thread_esc = threading.Thread(target=monitorar_tecla, daemon=True)
thread_esc.start()

thread1.join()