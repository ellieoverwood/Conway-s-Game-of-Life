import pyautogui, random

for i in range(0, random.randint(50, 100)):
    pyautogui.moveTo(random.randint(-50, 300), random.randint(0, 500), random.randint(1, 2)) 
pyautogui.moveTo(0, 0, 1) 