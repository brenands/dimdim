import pyautogui
import time
import random
from datetime import datetime
import mss
import sys
import keyboard
import threading

# --- Controle global ---
parar = False

# --- Contadores persistentes para cada navegador ---
contadores = {}

# --- Função: captura a cor de um pixel ---
def pegar_cor(x, y):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": 1, "height": 1}
        img = sct.grab(monitor)
        return img.pixel(0, 0)

# --- Função auxiliar: executa a sequência de cliques e scrolls ---
def executar_sequencia(config):
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
    global parar, contadores
    nome = config["nome"]

    # Inicializa o contador para este navegador, se ainda não existir
    if nome not in contadores:
        contadores[nome] = 0

    # Incrementa o contador
    contadores[nome] += 1
    contador = contadores[nome]
    hora_atual = datetime.now().strftime("[%H:%M:%S]")
    print(f"{hora_atual} [{nome}] Iniciando repetição nº {contador}")

    # === 1. Ativa a janela do navegador ===
    pyautogui.click(*config["pixel_ativar"])
    time.sleep(1)

    # === 2. Verificação IMEDIATA da cor extra (popup, notificação) ===
    alvo_extra = config["cor_extra"]
    extra_x, extra_y = config["pixel_extra"]

    cor_extra = pegar_cor(extra_x, extra_y)
    if cor_extra == alvo_extra:
        print(f"{hora_atual} [{nome}] Cor extra detectada ao ativar -> clicando em ({extra_x}, {extra_y})")
        pyautogui.click(extra_x, extra_y)
        time.sleep(1)

    # === 3. Verifica se deve esperar pela cor principal (só para Navegador 1) ===
    if config.get("esperar_cor", True):
        alvo = config["cor_principal"]
        corx, cory = config["pixel_principal"]

        print(f"{hora_atual} [{nome}] Esperando pela cor {alvo} no pixel ({corx}, {cory})")
        tempo_inicial = time.time()

        while not parar:
            cor = pegar_cor(corx, cory)
            if cor == alvo:
                delay = random.randint(1, 5)
                print(f"{hora_atual} [{nome}] Cor detectada -> aguardando {delay}s antes de continuar...")
                time.sleep(delay)
                break

            # Timeout de 5 minutos
            if time.time() - tempo_inicial > 300:
                print(f"{hora_atual} [{nome}] Tempo limite atingido -> clicando em reset {config['pixel_reset']}")
                pyautogui.click(*config["pixel_reset"])
                tempo_inicial = time.time()

            time.sleep(0.5)
    else:
        print(f"{hora_atual} [{nome}] Modo direto: pulando espera de cor principal.")
        time.sleep(2)

    # === 4. Executa a sequência de cliques e scrolls ===
    executar_sequencia(config)

    # === 5. Finaliza esta execução ===
    return  # Volta ao loop principal

# --- Sequência padrão de cliques (reutilizável) ---
sequencia_padrao = [
    (3, "click", (1503, 818)),   # Clique 1: ex. botão de ação
    (2, "scroll", 1500),         # Rola para cima (ajuste conforme necessário)
    (3, "click", (1531, 634)),   # Clique 2: outra interação
    (3, "click", (65, 100)),     # Clique 3: ex. atualizar página ou aba
]

# --- Configurações dos navegadores ---
config_navegador1 = {
    "nome": "Navegador 1",
    "cor_principal": (255, 203, 119),     # Cor a detectar (ex: botão habilitado)
    "pixel_principal": (1378, 426),       # Onde verificar a cor principal
    "cor_extra": (24, 51, 31),            # Cor do popup ou notificação
    "pixel_extra": (948, 850),            # Onde verificar a cor extra
    "clique_extra": (948, 850),           # Onde clicar se detectar cor extra
    "pixel_reset": (65, 100),            # Botão de reset (ex: recarregar)
    "sequencia_cliques": sequencia_padrao,
    "pixel_ativar": (214, 1050),          # Posição do ícone na barra de tarefas
    "esperar_cor": True                   # Sim, espera a cor principal
}

config_navegador2 = {
    "nome": "Navegador 2",
    "cor_principal": (255, 203, 119),     # Irrelevante (não usado)
    "pixel_principal": (1378, 426),       # Mantido por compatibilidade
    "cor_extra": (24, 51, 31),            # Mesma cor extra
    "pixel_extra": (948, 850),            # Mesmo local de verificação
    "clique_extra": (948, 850),           # Mesmo clique
    "pixel_reset": (65, 100),
    "sequencia_cliques": sequencia_padrao,
    "pixel_ativar": (260, 1050),           # Ícone do segundo navegador
    "esperar_cor": False                   # Não espera cor principal
}

config_navegador3 = {
    "nome": "Navegador 3",
    "cor_principal": (255, 203, 119),     # Irrelevante (não usado)
    "pixel_principal": (1378, 426),       # Mantido por compatibilidade
    "cor_extra": (24, 51, 31),            # Mesma cor extra
    "pixel_extra": (948, 850),            # Mesmo local de verificação
    "clique_extra": (948, 850),           # Mesmo clique
    "pixel_reset": (65, 100),
    "sequencia_cliques": sequencia_padrao,
    "pixel_ativar": (300, 1050),           # Ícone do segundo navegador
    "esperar_cor": False                   # Não espera cor principal
}

config_navegador4 = {
    "nome": "Navegador 4",
    "cor_principal": (255, 203, 119),     # Irrelevante (não usado)
    "pixel_principal": (1378, 426),       # Mantido por compatibilidade
    "cor_extra": (24, 51, 31),            # Mesma cor extra
    "pixel_extra": (948, 850),            # Mesmo local de verificação
    "clique_extra": (948, 850),           # Mesmo clique
    "pixel_reset": (65, 100),
    "sequencia_cliques": sequencia_padrao,
    "pixel_ativar": (350, 1050),           # Ícone do segundo navegador
    "esperar_cor": False                   # Não espera cor principal
}

config_navegador5 = {
    "nome": "Navegador 5",
    "cor_principal": (255, 203, 119),     # Irrelevante (não usado)
    "pixel_principal": (1378, 426),       # Mantido por compatibilidade
    "cor_extra": (24, 51, 31),            # Mesma cor extra
    "pixel_extra": (948, 850),            # Mesmo local de verificação
    "clique_extra": (948, 850),           # Mesmo clique
    "pixel_reset": (65, 100),
    "sequencia_cliques": sequencia_padrao,
    "pixel_ativar": (400, 1050),           # Ícone do segundo navegador
    "esperar_cor": False                   # Não espera cor principal
}

config_navegador6 = {
    "nome": "Navegador 6",
    "cor_principal": (255, 203, 119),     # Irrelevante (não usado)
    "pixel_principal": (1378, 426),       # Mantido por compatibilidade
    "cor_extra": (24, 51, 31),            # Mesma cor extra
    "pixel_extra": (948, 850),            # Mesmo local de verificação
    "clique_extra": (948, 850),           # Mesmo clique
    "pixel_reset": (65, 100),
    "sequencia_cliques": sequencia_padrao,
    "pixel_ativar": (440, 1050),           # Ícone do segundo navegador
    "esperar_cor": False                   # Não espera cor principal
}

# Lista de configurações (ordem de execução)
configs = [config_navegador1, config_navegador2, config_navegador3, config_navegador4, config_navegador5, config_navegador6]

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