
import pyautogui
import time

def capturar_pixel_mouse():
	"""
	Captura a posição atual do mouse na tela.
	Retorna uma tupla (x, y).
	"""
	return pyautogui.position()

# Exemplo de uso:
if __name__ == "__main__":
	print("Posicione o mouse no ponto desejado em 5 segundos...")
	time.sleep(5)
	pos = capturar_pixel_mouse()
	print("Posição atual do mouse:", pos)