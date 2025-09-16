import pyautogui
import time
import random
from datetime import datetime
import mss
import keyboard
import threading
import logging
import requests
import os
import ctypes

# --- Configuração de logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="[%H:%M:%S]"
)

# --- Controle global ---
parar = False
contadores = {}

# --- DISCORD WEBHOOK (substitui Telegram) ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/seu/link/aqui"  # 🔥 COLE SEU LINK AQUI!
CAMINHO_PRINT = "alerta_pixel_extra.png"

# --- Constantes globais ---
COR_PRINCIPAL = (255, 203, 119)
PIXEL_PRINCIPAL = (1378, 426)
COR_EXTRA = (24, 51, 31)
PIXEL_EXTRA = (948, 850)
CLIQUE_EXTRA = (948, 850)
PIXEL_RESET = (65, 100)
TIMEOUT_ESPERA = 300   # 5 minutos (só Navegador 1)
DELAY_RANDOM = (1, 5)  # delay após detectar cor principal

# --- Função: compara cores com tolerância ---
def cores_iguais(cor1, cor2, tol=15):
    return all(abs(a - b) <= tol for a, b in zip(cor1, cor2))

# --- Função: captura cor de um pixel ---
def pegar_cor(x, y):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": 1, "height": 1}
        img = sct.grab(monitor)
        return img.pixel(0, 0)

# --- Envia mensagem + foto para o Discord ---
def enviar_discord(mensagem, caminho_foto=None):
    try:
        data = {"content": mensagem}
        files = None

        if caminho_foto and os.path.exists(caminho_foto):
            with open(caminho_foto, 'rb') as f:
                files = {'file': ('alerta.png', f)}
                response = requests.post(DISCORD_WEBHOOK_URL, data=data, files=files, timeout=10)
        else:
            response = requests.post(DISCORD_WEBHOOK_URL, data=data, timeout=10)

        if response.status_code == 200:
            logging.info("📸 Alerta enviado para o Discord!")
        else:
            logging.error(f"❌ Falha ao enviar ao Discord: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"❌ Erro ao enviar para Discord: {e}")

# --- Executa sequência de cliques/scrolls ---
def executar_sequencia(config):
    for (espera, acao, valor) in config["sequencia_cliques"]:
        if parar:
            return
        time.sleep(espera)
        if acao == "scroll":
            pyautogui.scroll(valor)
        elif acao == "click":
            pyautogui.click(*valor)

# --- Função principal: rotina por navegador ---
def rotina_navegador(config):
    global parar, contadores
    nome = config["nome"]

    # Incrementa contador
    contadores[nome] = contadores.get(nome, 0) + 1
    contador = contadores[nome]
    logging.info(f"[{nome}] Iniciando repetição nº {contador}")

    # === 1. Ativa a janela do navegador ===
    logging.info(f"[{nome}] Ativando janela em {config['pixel_ativar']}")
    pyautogui.click(*config["pixel_ativar"])
    pyautogui.click(*config["pixel_ativar"])  # duplo clique para garantir foco
    time.sleep(1.5)

    # === 2. Monitoramento da COR EXTRA (todos os navegadores) ===
    logging.info(f"[{nome}] Iniciando verificação de cor extra...")
    tempo_inicial = time.time()

    while not parar:
        tempo_decorrido = time.time() - tempo_inicial

        # Define quanto tempo cada tipo de navegador espera
        if config["esperar_cor"]:  # Navegador 1: até 5 min
            tempo_maximo = TIMEOUT_ESPERA
        else:  # Outros: até 5 segundos
            tempo_maximo = 5

        # --- Verifica COR EXTRA ---
        cor_extra = pegar_cor(*config["pixel_extra"])
        if cores_iguais(cor_extra, config["cor_extra"]):
            logging.warning(f"[{nome}] ⚠️ Cor extra detectada em {config['pixel_extra']}! RGB: {cor_extra}")

            # Tira print
            screenshot = pyautogui.screenshot()
            screenshot.save(CAMINHO_PRINT)

            # Monta mensagem
            mensagem = (
                f"⚠️ **ALERTA DE PIXEL EXTRA!**\n"
                f"**Navegador:** {nome}\n"
                f"**Repetição:** {contador}\n"
                f"**Horário:** {datetime.now().strftime('%H:%M:%S')}\n"
                f"**Pixel:** {config['pixel_extra']}\n"
                f"**Cor detectada:** {cor_extra}"
            )

            # Envia para Discord
            enviar_discord(mensagem, CAMINHO_PRINT)

            # --- Reativa a janela DO MESMO NAVEGADOR (evita erro!) ---
            logging.info(f"[{nome}] Reativando janela antes do clique: {config['pixel_ativar']}")
            pyautogui.click(*config["pixel_ativar"])
            pyautogui.click(*config["pixel_ativar"])
            time.sleep(0.5)

            # Clica no pixel extra
            pyautogui.click(*config["clique_extra"])
            logging.info(f"[{nome}] Clique executado em {config['clique_extra']}")

            # Pausa pós-clique para interface reagir
            time.sleep(1.5)

            # Remove o print
            if os.path.exists(CAMINHO_PRINT):
                os.remove(CAMINHO_PRINT)

            # Reinicia o cronômetro para evitar múltiplos cliques
            tempo_inicial = time.time()
            continue  # volta ao loop

        # --- Verifica COR PRINCIPAL (só se esperar_cor=True) ---
        if config["esperar_cor"]:
            cor_principal = pegar_cor(*config["pixel_principal"])
            if cores_iguais(cor_principal, config["cor_principal"]):
                delay = random.uniform(*DELAY_RANDOM)
                logging.info(f"[{nome}] ✅ Cor principal detectada -> aguardando {delay:.1f}s")
                time.sleep(delay)
                break  # sai do loop → vai para sequência

            # Timeout: 5 minutos sem progresso
            if tempo_decorrido > TIMEOUT_ESPERA:
                logging.warning(f"[{nome}] ⏳ Timeout -> clicando em reset {config['pixel_reset']}")
                pyautogui.click(*config["pixel_reset"])
                tempo_inicial = time.time()

        # --- Saída para navegadores rápidos ---
        if not config["esperar_cor"] and tempo_decorrido >= 5:
            break

        time.sleep(0.5)  # pausa entre verificações

    # === 3. Executa a sequência de cliques ===
    logging.info(f"[{nome}] Executando sequência de cliques...")
    executar_sequencia(config)

# --- Cria configurações reutilizáveis ---
def criar_config(nome, pixel_ativar, esperar_cor=False):
    return {
        "nome": nome,
        "cor_principal": COR_PRINCIPAL,
        "pixel_principal": PIXEL_PRINCIPAL,
        "cor_extra": COR_EXTRA,
        "pixel_extra": PIXEL_EXTRA,
        "clique_extra": CLIQUE_EXTRA,
        "pixel_reset": PIXEL_RESET,
        "sequencia_cliques": [
            (3, "click", (1503, 818)),
            (2, "scroll", 1500),
            (3, "click", (1531, 634)),
            (3, "click", (65, 100)),
        ],
        "pixel_ativar": pixel_ativar,
        "esperar_cor": esperar_cor,
    }

# --- Lista de navegadores ---
configs = [
    criar_config("Navegador 1", (214, 1050), esperar_cor=True),
    criar_config("Navegador 2", (260, 1050)),
    criar_config("Navegador 3", (300, 1050)),
    criar_config("Navegador 4", (350, 1050)),
    criar_config("Navegador 5", (400, 1050)),
    criar_config("Navegador 6", (440, 1050)),
]

# --- Thread: monitora tecla ESC (2x em até 5s para parar) ---
def monitorar_tecla():
    global parar
    contador_esc = 0
    primeiro_tempo = None
    limite_tempo = 5

    while not parar:
        if keyboard.is_pressed("esc"):
            agora = time.time()
            if contador_esc == 0:
                primeiro_tempo = agora
                contador_esc = 1
            else:
                if agora - primeiro_tempo <= limite_tempo:
                    contador_esc += 1
                else:
                    contador_esc = 1
                    primeiro_tempo = agora

            logging.warning(f"[!] ESC pressionado ({contador_esc}/2)")

            if contador_esc >= 2:
                logging.warning("[!] Encerrando...")
                parar = True
                break

            while keyboard.is_pressed("esc"):
                time.sleep(0.2)

        time.sleep(0.2)

# --- INÍCIO DO PROGRAMA ---
if __name__ == "__main__":
    # Impede o sistema de suspender
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
        logging.info("Sistema configurado para não suspender.")
    except Exception as e:
        logging.warning(f"Falha ao bloquear suspensão: {e}")

    # Inicia thread de controle
    thread_esc = threading.Thread(target=monitorar_tecla, daemon=True)
    thread_esc.start()

    logging.info("✅ Rotina iniciada. Pressione ESC duas vezes para parar.")

    # Loop principal
    while not parar:
        for config in configs:
            if parar:
                break
            rotina_navegador(config)
            time.sleep(1.5)