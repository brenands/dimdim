import pyautogui
import time
import mss
import keyboard

def pegar_cor(x, y):
    """Captura a cor RGB de um pixel específico usando mss."""
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": 1, "height": 1}
        img = sct.grab(monitor)
        return img.pixel(0, 0)

# Posição do pixel que você quer testar
x, y = 867, 775

print("🚀 Script de leitura e clique no pixel iniciado!")
print(f"📍 Monitorando pixel: ({x}, {y})")
print("❌ Pressione ESC para parar.")

try:
    while True:
        # Verifica se o usuário pressionou ESC
        if keyboard.is_pressed("esc"):
            print("\n🛑 Encerrando...")
            break

        # Captura a cor
        cor = pegar_cor(x, y)

        # Mostra a cor no console
        print(f"🎨 Cor em ({x}, {y}): RGB{cor}")

        # Clica no pixel
        pyautogui.click(x, y)
        print(f"🖱️  Clique executado em ({x}, {y})")

        # Espera 2 segundos antes da próxima leitura
        time.sleep(2)

except KeyboardInterrupt:
    print("\n👋 Interrompido pelo usuário.")