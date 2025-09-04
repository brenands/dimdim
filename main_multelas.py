import pyautogui
import time
import random
from datetime import datetime
import mss
import sys
import keyboard
import threading

# --- Controle global para parar todas as ações ---
parar = False

# --- Função: captura a cor de um pixel específico ---
def pegar_cor(x, y):
    """
    Usa mss para capturar um único pixel na posição (x, y).
    Funciona mesmo com a tela desligada ou em segundo plano.
    Retorna uma tupla RGB: (R, G, B)
    """
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": 1, "height": 1}
        img = sct.grab(monitor)
        return img.pixel(0, 0)  # Retorna cor em formato RGB

# --- Função auxiliar: executa a sequência de cliques e scrolls ---
def executar_sequencia(config):
    """
    Executa a lista de ações definida em 'sequencia_cliques'.
    Exemplo: (espera, "click", (x, y)) ou (espera, "scroll", valor)
    """
    for (espera, acao, valor) in config["sequencia_cliques"]:
        if parar:
            return
        time.sleep(espera)
        if acao == "scroll":
            pyautogui.scroll(valor)
        elif acao == "click":
            pyautogui.click(*valor)

# --- Função principal: rotina para cada navegador ---
def rotina_navegador(config):
    """
    Executa a rotina completa de um navegador:
    1. Ativa a janela (clica na barra de tarefas)
    2. Verifica IMEDIATAMENTE se a cor extra está presente (popup/notificação)
    3. Se configurado, espera pela cor principal
    4. Executa a sequência de ações
    5. Retorna para o próximo navegador
    """
    global parar
    nome = config["nome"]
    contador = 0

    while not parar:
        contador += 1
        hora_atual = datetime.now().strftime("[%H:%M:%S]")
        print(f"{hora_atual} [{nome}] Iniciando repetição nº {contador}")

        # === 1. Ativa a janela do navegador (clica na barra de tarefas) ===
        pyautogui.click(*config["pixel_ativar"])
        time.sleep(1)  # tempo para garantir que a janela está ativa

        # === 2. Verificação IMEDIATA da cor extra (popup, notificação, erro, etc) ===
        alvo_extra = config["cor_extra"]
        extra_x, extra_y = config["pixel_extra"]

        cor_extra = pegar_cor(extra_x, extra_y)
        if cor_extra == alvo_extra:
            print(f"{hora_atual} [{nome}] Cor extra detectada ao ativar -> clicando em ({extra_x}, {extra_y})")
            pyautogui.click(extra_x, extra_y)
            time.sleep(1)  # pequeno delay para interface reagir

        # === 3. Verifica se deve esperar pela cor principal (só para Navegador 1) ===
        if config.get("esperar_cor", True):  # padrão: True
            alvo = config["cor_principal"]
            corx, cory = config["pixel_principal"]

            print(f"{hora_atual} [{nome}] Esperando pela cor {alvo} no pixel ({corx}, {cory})")
            tempo_inicial = time.time()

            while not parar:
                cor = pegar_cor(corx, cory)
                if cor == alvo:
                    delay = random.randint(1, 10)
                    print(f"{hora_atual} [{nome}] Cor detectada -> aguardando {delay}s antes de continuar...")
                    time.sleep(delay)
                    break  # sai do loop de espera

                # Timeout: se passar 5 minutos sem detectar a cor
                if time.time() - tempo_inicial > 300:  # 300 segundos = 5 minutos
                    print(f"{hora_atual} [{nome}] Tempo limite atingido -> clicando em reset {config['pixel_reset']}")
                    pyautogui.click(*config["pixel_reset"])
                    tempo_inicial = time.time()  # reinicia o cronômetro

                time.sleep(0.5)  # evita uso excessivo de CPU
        else:
            # === Modo direto: Navegador 2 não espera cor principal ===
            print(f"{hora_atual} [{nome}] Modo direto: pulando espera de cor principal e seguindo para ações.")
            time.sleep(2)  # pequeno delay para garantir estabilidade

        # === 4. Executa a sequência de cliques e scrolls ===
        executar_sequencia(config)

        # === 5. Finaliza esta execução e volta ao loop principal ===
        return  # Sai da função para o próximo navegador


# --- Sequência padrão de cliques (reutilizável) ---
sequencia_padrao = [
    (3, "click", (1503, 818)),   # Clique 1: ex. botão de ação
    (2, "scroll", 1500),         # Rola para cima (ajuste conforme necessário)
    (3, "click", (1531, 634)),   # Clique 2: outra interação
    (3, "click", (676, 101))     # Clique 3: ex. atualizar página ou aba
]

# --- Configurações dos navegadores ---
config_navegador1 = {
    "nome": "Navegador 1",
    "cor_principal": (255, 203, 119),     # Cor a detectar (ex: botão habilitado)
    "pixel_principal": (1378, 426),       # Onde verificar a cor principal
    "cor_extra": (24, 51, 31),            # Cor do popup ou notificação
    "pixel_extra": (952, 765),            # Onde verificar a cor extra
    "clique_extra": (952, 765),           # Onde clicar se detectar cor extra
    "pixel_reset": (1633, 99),            # Botão de reset (ex: recarregar)
    "sequencia_cliques": sequencia_padrao,
    "pixel_ativar": (214, 1050),          # Posição do ícone na barra de tarefas
    "esperar_cor": True                   # Sim, espera a cor principal
}

config_navegador2 = {
    "nome": "Navegador 2",
    "cor_principal": (255, 203, 119),     # Irrelevante (não usado)
    "pixel_principal": (1378, 426),       # Mantido por compatibilidade
    "cor_extra": (24, 51, 31),            # Mesma cor extra
    "pixel_extra": (952, 765),            # Mesmo local de verificação
    "clique_extra": (952, 765),           # Mesmo clique
    "pixel_reset": (1633, 99),
    "sequencia_cliques": sequencia_padrao,
    "pixel_ativar": (260, 1050),           # Ícone do segundo navegador
    "esperar_cor": False                   # Não espera cor principal
}

# Lista de configurações (ordem de execução)
configs = [config_navegador1, config_navegador2]

# --- Thread: monitora tecla ESC (2x em até 5 segundos para parar) ---
def monitorar_tecla():
    global parar
    contador_esc = 0
    primeiro_tempo = None
    limite_tempo = 5  # segundos

    while True:
        if keyboard.is_pressed("esc"):
            agora = time.time()

            if contador_esc == 0:
                primeiro_tempo = agora
                contador_esc = 1
            else:
                if agora - primeiro_tempo > limite_tempo:
                    # Reinicia contagem se passar do tempo
                    contador_esc = 1
                    primeiro_tempo = agora
                else:
                    contador_esc += 1

            print(f"[!] ESC pressionado ({contador_esc}/2)")

            if contador_esc >= 2:
                print("\n[!] Tecla ESC pressionada 2 vezes. Encerrando...")
                parar = True
                sys.exit(0)

            # Evita múltiplos registros enquanto a tecla está pressionada
            while keyboard.is_pressed("esc"):
                time.sleep(0.2)

        time.sleep(0.2)

# --- INÍCIO DO PROGRAMA ---
if __name__ == "__main__":
    # Inicia a thread de monitoramento de tecla (ESC)
    thread_esc = threading.Thread(target=monitorar_tecla, daemon=True)
    thread_esc.start()

    print("[INFO] Rotina iniciada. Pressione ESC duas vezes para parar.")

    # Loop principal: executa os navegadores em sequência
    while not parar:
        for config in configs:
            if parar:
                break
            rotina_navegador(config)  # Executa uma vez por navegador
            time.sleep(1.5)  # Pausa entre um e outro (evita sobreposição)