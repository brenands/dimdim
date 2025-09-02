import pyautogui
import time

time.sleep(3)
corx, cory = 979, 535
cor = pyautogui.pixel(corx, cory)
print(cor)  