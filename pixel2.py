import pyautogui
import keyboard

print("🚀 Clique em qualquer lugar da tela e pressione a tecla 'p' para capturar o pixel.")
print("Pressione 'esc' para sair.\n")

while True:
    if keyboard.is_pressed("p"):
        x, y = pyautogui.position()  # Pega posição do mouse
        cor = pyautogui.screenshot().getpixel((x, y))  # Pega cor do pixel
        print(f"Pixel em ({x}, {y}) → RGB {cor}")
        while keyboard.is_pressed("p"):  # Espera soltar a tecla
            pass

    if keyboard.is_pressed("esc"):
        print("✅ Encerrado.")
        break